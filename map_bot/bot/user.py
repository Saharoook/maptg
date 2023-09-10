import logging
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from bot.models import TgUser, Point
from django.db import Error
from telebot import types
from bot.tasks import send_message


logging.basicConfig(level=logging.WARNING, filename="logs/user.log",
                    format="%(asctime)s %(levelname)s %(message)s")


class User:

    def __init__(self, message):

        self.user = None
        self.verify(message)
        self.keyboard = None

        if self.user is not None:
            self.keyboard = self.keyboard_definition()
            self.update_username(message)

    def is_exist(self):
        return True if self.user is not None else False

    def is_admin(self):
        return self.user.admin_check

    def hello_message(self):
        if self.user.admin_check:
            return f'Добро пожаловать, {self.user.nick_name}'
        else:
            return ('Бот поможет найти нужные места на карте и проложить к ним маршрут\n'
                    'Для получения возможности добавлять точки, '
                    'вы можете обратиться в поддержку обратитесь в поддержку')

    def verify(self, message):
        try:
            self.user = TgUser.objects.get(tg_id=message.chat.id)

        except MultipleObjectsReturned as error:
            logging.warning(error)
            send_message.delay(message.chat.id, 'Есть несколько аккаунтов с вашим ID. Обратитесь к администратору',
                               False)
            logging.warning(f'Multiple accounts {error}')
            self.user = None

        except ObjectDoesNotExist as error:
            logging.info(f'rejected request {error}')
            self.user = None

        except Exception as ex:
            logging.warning(f'From verify, unresolved exception: {ex}')
            self.user = None

    def update_username(self, message):

        try:
            self.user.nick_name = message.from_user.username
            self.user.save()
        except Error as err:
            logging.warning(err)
