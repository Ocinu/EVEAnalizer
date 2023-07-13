from . import keyboards as kb


def entrypoint(message, bot):
    start_command = message.text.split()
    return bot.send_message(
        message.from_user.id,
        text=start_command,
        parse_mode="HTML",
        reply_markup=kb.superuser_start_menu_markup(),
    )


def text_echo(message, bot):
    bot.send_message(message.from_user.id, message.text)


def callback_echo(call, bot):
    bot.send_message(call.from_user.id, call.data)
