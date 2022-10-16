import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from api import serializers, models
from api.Order import Order
from api.customBaseClassView import BaseAddUpdateClient, BaseGetDeleteClient, BaseDeleteUpdateMailing, \
    LargeResultsSetPagination
from api.tasks import send_data, additional_task
from config.celery import app
from config.settings import env, MESSAGE_CREATED


class ClientView(BaseGetDeleteClient):

    def get(self, request, id):
        client = self.get_queryset()
        if client:
            serializer = serializers.ClientSerializer(instance=client)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "not found"}, status=status.HTTP_400_BAD_REQUEST)


class ClientAddView(BaseAddUpdateClient):

    def post(self, request):
        serializer = serializers.ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientAddManyView(generics.GenericAPIView, CreateModelMixin):
    serializer_class = serializers.ClientSerializer
    queryset = models.ClientModel.objects.all()

    @swagger_auto_schema(
        operation_description="Массовая запись клиентов в формате [{\"key\":\"value\",...},{\"key\":\"value\", ...}]")
    def post(self, request):
        serializer = serializers.ClientSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientUpdateView(BaseAddUpdateClient):

    def put(self, request):
        client = self.get_queryset()
        serializer = serializers.ClientSerializer(data=request.data, instance=client)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDeleteView(BaseGetDeleteClient):

    def delete(self, request, id):
        client = self.get_queryset()
        if client:
            client.delete()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        return Response({"message": "unsuccess"}, status=status.HTTP_400_BAD_REQUEST)


class MailingView(generics.GenericAPIView):
    serializer_class = serializers.MailingDetailSerializer
    lookup_field = 'id'

    def get(self, request, id):
        mailing = self.get_queryset()
        if mailing:
            serializer = serializers.MailingDetailSerializer(instance=mailing)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "not found"}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        try:
            id = self.kwargs['id']
            mailing = models.MailingModel.objects.filter(pk=id).first()
            return mailing
        except KeyError:
            return None


class MailingListView(generics.ListAPIView):
    pagination_class = LargeResultsSetPagination
    serializer_class = serializers.MailingSerializer

    def get_queryset(self):
        try:
            mailing = models.MailingModel.objects.filter().order_by("id")
            return mailing
        except KeyError:
            return None


class MailingAddView(BaseDeleteUpdateMailing):

    def post(self, request):
        serializer = serializers.MailingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = models.MessageModel()
            message.created = datetime.datetime.now()
            message.mailing_num = serializer.data['id']
            message.status = MESSAGE_CREATED
            message.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MailingUpdateView(BaseDeleteUpdateMailing):

    def put(self, request, id):
        mailing = self.get_queryset()
        serializer = serializers.MailingSerializer(data=request.data, instance=mailing)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MailingDeleteView(BaseDeleteUpdateMailing):
    def delete(self, request, id):
        mailing = self.get_queryset()
        if mailing:
            mailing.delete()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        return Response({"message": "unsuccess"}, status=status.HTTP_400_BAD_REQUEST)


class TaskRunView(generics.GenericAPIView):

    @swagger_auto_schema(
        operation_description="Чтобы запустить задачу нужно передать id рассылку(mailing).")
    def get(self, request, id):
        if id > 0:
            task_id = self.task(id=int(id))
            if task_id != -1:
                return Response(data={"message": "Задача добавлена", "id": f'{task_id}'}, status=status.HTTP_200_OK)
        return Response(data={"message": "Задача не добавлена"}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return models.MailingModel.objects.filter(pk=self.kwargs['id']).first()

    def task(self, id: int = 0):
        mailing = self.get_queryset()
        if mailing:
            start_task = datetime.datetime.strptime(str(mailing.start_date), "%Y-%m-%d %H:%M:%S%z")
            finish_date = datetime.datetime.strptime(str(mailing.finish_date), "%Y-%m-%d %H:%M:%S%z")
            soft_time_limit = int((finish_date - start_task).total_seconds())
            base_url = env("SERVICE_SMS_BASE_URL")
            timeout = env("SERVICE_SMS_TIMEOUT")
            key = env("SERVICE_SMS_KEY")
            task_id = send_data.apply_async((base_url, key, mailing.id, timeout), eta=start_task,
                                            expires=finish_date,
                                            soft_time_limit=soft_time_limit)
            return task_id
        return -1


class TaskAbortView(generics.GenericAPIView):

    def delete(self, request, id):
        app.control.revoke(task_id=id, terminate=True)
        return Response(data={"message": "Задача отменена"}, status=status.HTTP_200_OK)


class OrderView(generics.GenericAPIView):

    def get(self, request):
        body = self.get_body()
        return Response(data=body)

    def get_body(self):
        order = Order()
        body = order.get_mailing()
        return body


class OrderDetailView(generics.GenericAPIView):
    lookup_field = 'id'

    def get(self, request, id):
        body = self.get_body()
        return Response(data=body)

    def get_body(self):
        order = Order()
        body = order.get_mailing_detail(id=self.kwargs["id"])
        return body
