import telebot
from django.db import connection

from .models import BotConfig


class BotConfigurator:
    def __init__(self):
        if (
            "Bot_botconfig" in connection.introspection.table_names()
            and BotConfig.objects.filter(is_active=True)
        ):
            config = BotConfig.objects.get(is_active=True)
            self.server_url = config.server_url
            self.bot = telebot.TeleBot(config.token, threaded=False)
        else:
            self.bot = telebot.TeleBot("123")

    def get_bot(self):
        return self.bot

    def get_server_url(self):
        return self.server_url

    def update(self, json_data):
        return telebot.types.Update.de_json(json_data)
