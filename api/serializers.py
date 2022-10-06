from rest_framework import serializers

from api import models


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientModel
        fields = '__all__'
