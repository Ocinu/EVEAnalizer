from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import dispatcher as dp
from .bot import BotConfigurator

tBot = BotConfigurator()
bot = tBot.get_bot()


@csrf_exempt
def get_hook(request):
    if request.META["CONTENT_TYPE"] == "application/json":
        json_data = request.body.decode("utf-8")
        update = tBot.update(json_data)
        bot.process_new_updates([update])
        return HttpResponse(status=200)
    else:
        raise PermissionDenied


@bot.message_handler(commands=["start"])
def start_command(message):
    dp.entrypoint(message, bot)


@bot.message_handler(content_types=["text"])
def text_messages(message):
    dp.text_echo(message, bot)


@bot.callback_query_handler(func=lambda call: True)
def callback_queries(call):
    dp.callback_echo(call, bot)
