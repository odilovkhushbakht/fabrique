from rest_framework import serializers

from api import models


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientModel
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MailingModel
        fields = '__all__'
        # fields = ('id', 'start_date', 'finish_date', 'text', 'custom_filter')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MessageModel
        fields = '__all__'
