# Generated by Django 4.1.2 on 2022-10-11 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_messagemodel_mailing_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientmodel',
            name='time_zone',
            field=models.CharField(default='Europe/Moscow', max_length=100),
        ),
    ]
