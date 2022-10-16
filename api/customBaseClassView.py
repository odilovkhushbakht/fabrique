from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from api import serializers, models


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BaseAddUpdateClient(generics.GenericAPIView):
    serializer_class = serializers.ClientSerializer
    lookup_field = 'id'

    def get_queryset(self):
        try:
            id = self.request.data['id']
            client = models.ClientModel.objects.filter(pk=id).first()
            return client
        except KeyError:
            return None


class BaseGetDeleteClient(BaseAddUpdateClient):

    def get_queryset(self):
        try:
            id = self.kwargs['id']
            client = models.ClientModel.objects.filter(pk=id).first()
            return client
        except KeyError:
            return None


class BaseDeleteUpdateMailing(generics.GenericAPIView):
    serializer_class = serializers.MailingSerializer
    lookup_field = 'id'

    def get_queryset(self):
        try:
            id = self.kwargs['id']
            mailing = models.MailingModel.objects.filter(pk=id).first()
            return mailing
        except KeyError:
            return None
