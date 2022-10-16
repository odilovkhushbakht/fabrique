from django.db import models
from django.utils import timezone


class ClientModel(models.Model):
    # message_child = models.IntegerField()
    phone = models.CharField(default=79999999999, max_length=11)
    operator_code = models.IntegerField(default=919)
    tag = models.CharField(max_length=20, default='tag')
    time_zone = models.CharField(default='Europe/Moscow', max_length=100)


class MailingModel(models.Model):
    # message_parent = models.IntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    finish_date = models.DateTimeField(default=timezone.now)
    text = models.TextField(default='text message')
    custom_filter = models.CharField(default='operator_code', max_length=20)


class MessageModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    sent = models.DateTimeField(default=timezone.now)
    client_num = models.IntegerField(default=0)
    mailing_num = models.IntegerField(default=0)
    status = models.CharField(default="Отправлено", max_length=50)
