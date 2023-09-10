from map_bot.celery import app
from map_bot.settings import TELEGRAM_API_KEY
from telebot import TeleBot


bot = TeleBot(TELEGRAM_API_KEY)


@app.task
def send_message(chat_id, text, admin_check):
    from .markups import admin_markup, user_markup
    bot.send_message(chat_id, text, reply_markup=admin_markup) if admin_check else (
        bot.send_message(chat_id, text, reply_markup=user_markup))
