from rest_framework import status
from rest_framework.response import Response

from api import serializers
from api.customBaseClassView import BaseAddUpdateClientView, BaseGetDeleteUpdateClientView


class ClientView(BaseGetDeleteUpdateClientView):

    def get(self, request, id):
        client = self.get_queryset()
        if client:
            serializer = serializers.ClientSerializer(instance=client, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "not found"}, status=status.HTTP_400_BAD_REQUEST)


class ClientAddView(BaseAddUpdateClientView):

    def post(self, request):
        serializer = serializers.ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientUpdateView(BaseAddUpdateClientView):

    def put(self, request):
        client = self.get_queryset()
        serializer = serializers.ClientSerializer(data=request.data, instance=client)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDeleteView(BaseGetDeleteUpdateClientView):

    def delete(self, request, id):
        client = self.get_queryset()
        if client:
            client.delete()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        return Response({"message": "unsuccess"}, status=status.HTTP_400_BAD_REQUEST)
