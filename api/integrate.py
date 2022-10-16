import asyncio
import datetime
from abc import ABC, abstractmethod

import aiohttp
from asgiref.sync import sync_to_async

from api.models import MessageModel
from config.settings import MESSAGE_SUCCESS, MESSAGE_UNSUCCESS, MESSAGE_CREATED


class MailingService(ABC):

    def __init__(self, base_url: str = '', key: str = '', timeout: int = 5) -> None:
        self.__base_url = base_url
        self.__key = key
        self.__timeout = timeout

    def get_base_url(self) -> str:
        return self.__base_url

    def set_base_url(self, url: str = ''):
        self.__base_url = url

    def get_key(self) -> str:
        return self.__key

    def set_key(self, key: str = ''):
        self.__key = key

    def get_timeout(self) -> int:
        return int(self.__timeout)

    def set_timeout(self, timeout: int = 0):
        self.__timeout = timeout

    @abstractmethod
    def send(self, service_data):
        pass


class SmsService(MailingService):

    def send(self, service_data):
        self.service_data = service_data
        asyncio.run(self._start())

    async def _start(self):
        queue = asyncio.Queue()
        tasks = []

        for item in self.service_data["status_list"]:
            body = {
                'id': item["mailing_num"],
                'phone': item["phone"],
                'text': self.service_data["mailing"]["text"]
            }
            url = f'{self.get_base_url()}{item["mailing_num"]}'

            task = asyncio.create_task(self._send_request(url=url, data=body.copy(), message_id=item["id"]))
            tasks.append(task)

            if len(tasks) == 9:
                await queue.join()
                await asyncio.gather(*tasks)
                await asyncio.sleep(3)
                tasks.clear()
        else:
            await queue.join()
            await asyncio.gather(*tasks)

    async def _send_request(self, url: str = '', data: dict = {}, message_id: int = 0):
        header = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': self.get_key()
        }
        timeout = self.get_timeout()
        status = MESSAGE_UNSUCCESS
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(url=url, headers=header, json=data)
        # {'id': 1, 'created': datetime.datetime(2022, 10, 16, 8, 56, 18, 32417, tzinfo=datetime.timezone.utc), 'sent': datetime.datetime(2022, 10, 16, 8, 56, 18, 32421, tzinfo=datetime.timezone.utc), 'client_num': 1, 'mailing_num': 2, 'status': 'Создано', 'phone': '79194740886', 'operator_code': 919, 'tag': 'mts', 'time_zone': 'Europe/Moscow'}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, headers=header, json=data, timeout=timeout) as response:
                    if response.status >= 200 and response.status < 300:
                        status = MESSAGE_SUCCESS
        except aiohttp.ClientTimeout as e:
            print("ClientError or ClientTimeout", e)
            print("сервис не работает или время ожидание превышено")

        def update():
            MessageModel.objects.filter(pk=message_id).update(sent=datetime.datetime.now(), status=status)
            # sql = f"UPDATE api_messagemodel SET sent='{datetime.datetime.now()}', status='{status}' WHERE id={message_id}"
            # sql = sql.replace("\n", "")
            # with connection.cursor() as cursor:
            #     cursor.execute(sql)
            #     cursor.fetchone()

        await sync_to_async(update)()

        return


class SmsServiceRepeat(SmsService):

    async def _start(self):
        queue = asyncio.Queue()
        tasks = []

        for item in self.service_data["client"]:
            body = {
                'id': item["mailing_num"],
                'phone': item["phone"],
                'text': item["text"]
            }
            url = f'{self.get_base_url()}{item["mailing_num"]}'

            task = asyncio.create_task(self._send_request(url=url, data=body.copy(), message_id=item["id"]))
            tasks.append(task)

            if len(tasks) == 9:
                await queue.join()
                await asyncio.gather(*tasks)
                await asyncio.sleep(3)
                tasks.clear()
        else:
            await queue.join()
            await asyncio.gather(*tasks)
