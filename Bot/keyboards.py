from telebot import types


def superuser_start_menu_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("test", callback_data="test"))
    return markup
