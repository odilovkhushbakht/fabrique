# Generated by Django 4.1.2 on 2022-10-08 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_messagemodel_mailing_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagemodel',
            name='mailing_num',
            field=models.IntegerField(default=0),
        ),
    ]
