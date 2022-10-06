from django.db import models


class ClientModel(models.Model):
    # message_child = models.IntegerField()
    phone = models.CharField(default=79999999999, max_length=11)
    operator_code = models.IntegerField(default=919)
    tag = models.CharField(max_length=20, default='tag')
    time_zone = models.CharField(default='UTC', max_length=10)
