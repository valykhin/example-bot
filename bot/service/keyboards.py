from telebot import types
import logging.config


logging.config.fileConfig('logging.conf')

logger = logging.getLogger('root')

crossIcon = u"\u274C"

menu_commands = ['/servers 🖥', '/configs 📁', '/subscriptions 📬']


def create_app_keyboard():
    return create_keyboard(menu_commands)


def create_keyboard(available_commands):
    commands_count = len(available_commands)
    row_width = 2
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    commands_in_row = []
    for i in range(0, commands_count, 1):
        commands_in_row.append(types.KeyboardButton(available_commands[i]))
    keyboard.add(*commands_in_row, row_width=row_width)
    keyboard.add(types.KeyboardButton('/start'))
    return keyboard


def create_menu(available_commands, rows=1):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = rows
    for command in available_commands:
        for row in range(0, rows):
            markup.add(types.InlineKeyboardButton(command['label'], callback_data=command['data']))
    return markup


def create_text_menu(available_commands, rows=1):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = rows
    for command in available_commands:
        for row in range(0, rows):
            markup.add(types.KeyboardButton(text=command['label']))
    return markup


def create_one_time_menu(available_commands, row_width=2):
    commands_count = len(available_commands)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width, one_time_keyboard=True)
    commands_in_row = []
    for i in range(0, commands_count, 1):
        commands_in_row.append(types.KeyboardButton(available_commands[i]))
    keyboard.add(*commands_in_row, row_width=row_width)
    return keyboard
