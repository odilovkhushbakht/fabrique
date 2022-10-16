from rest_framework import serializers

from api import models


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientModel
        fields = '__all__'


class ListClientSerializer(serializers.ModelSerializer):
    clients = serializers.SerializerMethodField()

    def get_clients(self, obj):
        data = ClientSerializer(obj.card.all(), many=True).data
        return data

    class Meta:
        model = models.ClientModel
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MailingModel
        fields = '__all__'


class MailingDetailSerializer(MailingSerializer):
    additional = serializers.SerializerMethodField()

    def get_additional(self, obj):
        try:
            message = models.MessageModel.objects.get(pk=obj.id)
            return MessageSerializer(instance=message).data
        except models.MessageModel.DoesNotExist:
            return {}


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MessageModel
        fields = '__all__'
