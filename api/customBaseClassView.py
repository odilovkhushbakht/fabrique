from rest_framework import generics

from api import serializers, models


class BaseAddUpdateClientView(generics.GenericAPIView):
    serializer_class = serializers.ClientSerializer
    lookup_field = 'id'

    def get_queryset(self):
        try:
            id = self.request.data['id']
            client = models.ClientModel.objects.filter(pk=id)
            return client
        except KeyError:
            return None


class BaseGetDeleteUpdateClientView(BaseAddUpdateClientView):

    def get_queryset(self):
        try:
            id = self.kwargs['id']
            client = models.ClientModel.objects.filter(pk=id).first()
            return client
        except KeyError:
            return None
