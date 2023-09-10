import logging
import random
from django.core.management import BaseCommand
from bot.user import User
from bot.tasks import send_message
from bot.tasks import bot
from bot.models import TgUser, Tokens
from map_bot.settings import BOT_URL
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


logging.basicConfig(level=logging.WARNING, filename="logs/bot.log",
                    format="%(asctime)s %(levelname)s %(message)s")


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            bot.enable_save_next_step_handlers(delay=2)
            bot.load_next_step_handlers()
            bot.infinity_polling()
            # restart()

        except Exception as ex:
            logging.critical(ex)


def restart():
    sas = TgUser.objects.filter(nick_name='exsilem')
    sas.delete()
    print(sas)


@bot.message_handler(commands=['start'])
def start_message(message):

    if not message.from_user.is_bot:

        user = User(message)

        if user.is_exist():
            send_message.delay(message.chat.id, user.hello_message(), user.is_admin())

        else:
            text = str(message.text).replace('/start ', '')

            if text != '':
                token = search_token(text)

                if token is not None:
                    create_user(token, message)
                    start_message(message)


# add_point = types.KeyboardButton('add point')
# change_point = types.KeyboardButton('change point')
# my_points = types.KeyboardButton('my points')
# invite_admin = types.KeyboardButton('invite admin')
# invite_user = types.KeyboardButton('invite user')
# support = types.KeyboardButton('support')


@bot.message_handler(content_types=['text'])
def branch_distributor(message):

    user = User(message)

    if user.is_exist():
        if user.is_admin():
            if message.text == 'invite admin':
                invite(user, True)
            if message.text == 'invite user':
                invite(user, False)


def search_token(possible_token):

    try:
        token = Tokens.objects.filter(activated=False)
        token = token.get(token=possible_token)

    except MultipleObjectsReturned as mor:
        logging.warning(f'Multiple tokens {mor}')

    except Exception as error:
        logging.warning(f'General token errors {error}')

    else:
        return token


def create_user(token: Tokens, message):
    try:
        user = TgUser()
        user.tg_id = message.chat.id
        user.nick_name = message.from_user.username
        user.admin_check = token.admin_check
        user.save()

        token = Tokens.objects.get(token=token.token)
        token.activated = True
        token.joined_user = user
        token.save()

    except Exception as error:
        logging.warning(f'Token registration failed {error, token.token}')


def token_generation():

    # Token generation
    token = ''.join([random.choice('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ') for i in range(25)])

    try:
        # Try to find generated token in DB
        Tokens.objects.get(token=token)

    except MultipleObjectsReturned:
        # if the token already exists
        token_generation()

    except ObjectDoesNotExist:
        # if the token does not exist return generated token
        return token


def add_token(row_token, user, flag):
    try:
        token = Tokens()
        token.token_creator = user.user
        token.token = row_token
        token.admin_check = flag
        token.save()

    except Exception as unknown_error:
        logging.warning(unknown_error)
        send_message.delay(user.user.tg_id, 'Что-то пошло не так', user.is_admin())


def invite(user, flag):
    token = token_generation()
    add_token(token, user, flag)
    send_message.delay(user.user.tg_id, f'Отправьте ссылку человеку, которого хотите добавить\n'
                                        f'{BOT_URL}?start={token}', user.is_admin())




