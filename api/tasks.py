import datetime

from billiard.exceptions import SoftTimeLimitExceeded
from celery.contrib.abortable import AbortableTask
from django.db import connection

from api.integrate import SmsService, SmsServiceRepeat
from api.models import MailingModel, ClientModel, MessageModel
from config.celery import app
from config.settings import MESSAGE_UNSUCCESS, TASK_FINISHED, CLIENT_LIST_EMPTY, MAILING_LIST_EMPTY, \
    TASK_TIME_AND_GLASS, MESSAGE_CREATED


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_list_mailing_unsuccess():
    sql = f"SELECT api_messagemodel.id,api_messagemodel.created,api_messagemodel.sent,api_messagemodel.status,api_messagemodel.mailing_num, api_clientmodel.phone,api_mailingmodel.text FROM api_messagemodel JOIN api_clientmodel ON api_clientmodel.id=api_messagemodel.client_num JOIN api_mailingmodel ON api_mailingmodel.id=api_messagemodel.mailing_num WHERE api_messagemodel.status='{MESSAGE_UNSUCCESS}' OR api_messagemodel.status='{MESSAGE_CREATED}'"
    sql = sql.replace("\n", "")

    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = dictfetchall(cursor)

    return result


def create_list_status(mailing_id: int = 0, client_list: list = []):
    tmp_list = []

    for client in client_list:
        tmp_list.append(
            MessageModel(
                created=datetime.datetime.now(),
                sent=datetime.datetime.now(),
                client_num=client["id"],
                mailing_num=mailing_id, status=MESSAGE_CREATED
            )
        )

    message_list = MessageModel.objects.bulk_create(tmp_list)
    message_str_id = ""

    for item in message_list:
        message_str_id = f"{message_str_id}{item.id},"
    else:
        message_str_id = f"{message_str_id}{item.id}"
    message_str_id = message_str_id.replace("\n", "")

    sql = f"SELECT api_messagemodel.id,api_messagemodel.created,api_messagemodel.sent,api_messagemodel.status,api_messagemodel.mailing_num, api_clientmodel.phone FROM api_messagemodel JOIN api_clientmodel ON api_clientmodel.id=api_messagemodel.client_num WHERE api_messagemodel.id in({message_str_id}) AND api_messagemodel.status='{MESSAGE_CREATED}'"

    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = dictfetchall(cursor)

    return result


@app.task(bind=True, base=AbortableTask)
def send_data(self, base_url: str = '', key: str = '', mailing_id: int = 0, timeout: int = 50):
    print("Запуск задач")
    result = TASK_FINISHED
    mailing = MailingModel.objects.filter(pk=mailing_id).values().first()
    client = list(ClientModel.objects.filter(tag=mailing["custom_filter"]).values())

    if len(client) == 0:
        print(CLIENT_LIST_EMPTY)
        return result
    if len(mailing) == 0:
        print(MAILING_LIST_EMPTY)
        return result

    mailing_id = mailing["id"]
    status_list = create_list_status(mailing_id=mailing_id, client_list=client)

    try:
        service_data = {
            "mailing": mailing,
            "status_list": status_list
        }
        sms_service = SmsService(base_url=base_url, key=key, timeout=timeout)
        sms_service.send(service_data=service_data.copy())
    except SoftTimeLimitExceeded:
        result = TASK_TIME_AND_GLASS
    return result


@app.task()
def additional_task(base_url: str = '', key: str = '', timeout: int = 50):
    result = TASK_FINISHED
    client = get_list_mailing_unsuccess()

    if len(client) == 0:
        print(CLIENT_LIST_EMPTY)
        return result

    try:
        service_data = {
            "client": client
        }
        sms_service = SmsServiceRepeat(base_url=base_url, key=key, timeout=timeout)
        sms_service.send(service_data=service_data.copy())
    except SoftTimeLimitExceeded:
        result = TASK_TIME_AND_GLASS

    return result
