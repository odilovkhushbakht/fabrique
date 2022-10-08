from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api import serializers, models
from api.customBaseClassView import BaseAddUpdateClient, BaseGetDeleteClient, BaseDeleteUpdateMailing


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ClientView(BaseGetDeleteClient):

    def get(self, request, id):
        client = self.get_queryset()
        if client:
            serializer = serializers.ClientSerializer(instance=client, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "not found"}, status=status.HTTP_400_BAD_REQUEST)


class ClientAddView(BaseAddUpdateClient):

    def post(self, request):
        serializer = serializers.ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientUpdateView(BaseAddUpdateClient):

    def put(self, request):
        client = self.get_queryset()
        serializer = serializers.ClientSerializer(data=request.data, instance=client)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDeleteView(BaseGetDeleteClient):

    def delete(self, request, id):
        client = self.get_queryset()
        if client:
            client.delete()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        return Response({"message": "unsuccess"}, status=status.HTTP_400_BAD_REQUEST)


class MailingView(generics.ListAPIView):
    pagination_class = LargeResultsSetPagination
    serializer_class = serializers.MailingSerializer

    def get_queryset(self):
        try:
            mailing = models.MailingModel.objects.filter()
            return mailing
        except KeyError:
            return None


class MailingAddView(BaseDeleteUpdateMailing):

    def post(self, request):
        serializer = serializers.MailingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MailingUpdateView(BaseDeleteUpdateMailing):

    def put(self, request):
        mailing = self.get_queryset()
        serializer = serializers.MailingSerializer(data=request.data, instance=mailing)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MailingDeleteView(BaseDeleteUpdateMailing):
    def delete(self, request, id):
        mailing = self.get_queryset()
        if mailing:
            mailing.delete()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        return Response({"message": "unsuccess"}, status=status.HTTP_400_BAD_REQUEST)
