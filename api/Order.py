from django.db.models import Q, Count
from django.forms import model_to_dict

from api import models
from config.settings import MESSAGE_SUCCESS, MESSAGE_CREATED, MESSAGE_UNSUCCESS


class BaseOrder():

    def get_mailing(self):
        pass

    def get_mailing_detail(self, id: int):
        pass


class Order(BaseOrder):

    def get_mailing(self):
        result = {}
        mailing = list(models.MailingModel.objects.filter().values("id", "text"))
        total_sent = 0
        total_quantity_success = 0
        total_quantity_unsuccess = 0
        for item in mailing:
            message_success = models.MessageModel.objects.filter(mailing_num=item["id"], status=MESSAGE_SUCCESS)
            message_success = message_success.values("id", "sent", "status")
            message_unsuccess = models.MessageModel.objects.filter(mailing_num=item["id"], status=MESSAGE_UNSUCCESS)
            message_unsuccess = message_unsuccess.values("id", "sent", "status")

            quantity_success = len(message_success)
            quantity_unsuccess = len(message_unsuccess)
            total_message = []
            total_message.extend(message_success)
            total_message.extend(message_unsuccess)

            item["success"] = quantity_success
            item["unsuccess"] = quantity_unsuccess
            item["sent"] = total_message

            total_quantity_success += quantity_success
            total_quantity_unsuccess += quantity_unsuccess
            total_sent += quantity_success + quantity_unsuccess

        result["quantity_mailing"] = len(mailing)
        result["total_sent"] = total_sent
        result["total_success"] = total_quantity_success
        result["total_unsuccess"] = total_quantity_unsuccess
        result["mailing"] = mailing
        return result

    def get_mailing_detail(self, id: int):
        mailing = models.MailingModel.objects.filter(pk=id).values().first()
        result = {}
        if mailing == None:
            return result
        # message_success1 = models.MessageModel.objects.values("status").filter(mailing_num=mailing["id"]).annotate()
        # print(message_success1)

        message_success = self.get_detail_message(mailing_id=mailing["id"], status=MESSAGE_SUCCESS)
        message_unsuccess = self.get_detail_message(mailing_id=mailing["id"], status=MESSAGE_UNSUCCESS)

        quantity_success = len(message_success)
        quantity_unsuccess = len(message_unsuccess)
        total_message = []
        total_message.extend(message_success)
        total_message.extend(message_unsuccess)
        total_sent = quantity_success + quantity_unsuccess

        # result["quantity_sent"]=
        result["total_sent"] = total_sent
        result["total_success"] = quantity_success
        result["total_unsuccess"] = quantity_unsuccess
        result["mailing"] = mailing
        result["sent"] = total_message
        return result

    def get_detail_message(self, mailing_id: int = 0, status: str = ""):
        message = models.MessageModel.objects.filter(mailing_num=mailing_id, status=status)
        message = list(message.values())
        client_list_id = []

        for item in message:
            client_list_id.append(item["client_num"])

        client = models.ClientModel.objects.in_bulk(client_list_id)

        for item in message:
            client_tmp = client[item["client_num"]]
            item["client"] = model_to_dict(client_tmp)
            del item["mailing_num"]
            del item["client_num"]

        return message
