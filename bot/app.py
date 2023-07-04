import telebot
from telegram.ext import DispatcherHandlerStop
from telegram import ParseMode
from telebot.types import CallbackQuery
from datetime import datetime, timezone
import logging.config

from localised_messages import get_message
from service import keyboards, users as users_service
from commands import user_settings as user_settings_commands
import config
from error_handler import error_handler, error_handler_from_user
from commands.common import bot_stop


logger = logging.getLogger('bot')

is_running = False
telegram_user_id = None
user = None
deep_link_action_state = None

# MAIN VARIABLES
BOT_TOKEN = config.BOT_TOKEN
bot_telegram_user_id = BOT_TOKEN.split(':')[0]

# bot
bot = telebot.TeleBot(BOT_TOKEN)

# Chat constants
LANG = 'ru'


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    global is_running, telegram_user_id, user
    lc = None
    if not is_running:
        try:
            user = None
            telegram_user_id = str(message.from_user.id)
            logger.info('Received start message from {} in chat {}'.format(telegram_user_id, message.chat.id))
            user = set_user_if_not_exists(user, message)
            lc = user.get('settings').get('language_code') if user is not None else 'en'
            bot.send_message(message.chat.id, get_message(lc).WELCOME_MESSAGE)
            bot.send_message(message.chat.id, text=get_message(lc).CHOOSE_COMMANDS,
                             reply_markup=keyboards.create_app_keyboard())
            deep_link_action(message, user)
        except DispatcherHandlerStop:
            logger.info('Handler stopped because waiting for user {} consent'.format(telegram_user_id))
        except Exception as error:
            error_handler(bot, message, error, get_message(lc).COMMON_ERROR_MESSAGE)
        finally:
            is_running = False
            telegram_user_id = None
            user = None


@bot.message_handler(commands=['help'])
def list_subscriptions_handler(message):
    global is_running, telegram_user_id, user
    if not is_running:
        try:
            user = None
            telegram_user_id = str(message.from_user.id)
            logger.info('Received help command message from {}'.format(telegram_user_id, message.chat.id))
            user = set_user_if_not_exists(user, message)
            lc = user.get('settings').get('language_code')
            bot.send_message(message.chat.id, get_message(lc).HELP_MESSAGE)
        except DispatcherHandlerStop:
            logger.info('Handler stopped because user {} did not give consent'.format(telegram_user_id))
        finally:
            is_running = False
            telegram_user_id = None
            user = None


@bot.message_handler(regexp='/create_user')
def list_subscriptions_handler(message):
    global is_running, telegram_user_id, user
    lc = None
    if not is_running:
        try:
            user = None
            telegram_user_id = str(message.from_user.id)
            logger.info('Received invite command message from {}'.format(telegram_user_id, message.chat.id))
            user = set_user_if_not_exists(user, message)
            lc = user.get('settings').get('language_code')
            text = message.text
            invitation_id = text[text.index('_')+1:]
            server_commands.apply_invitation(bot, message, invitation_id, user)
        except DispatcherHandlerStop:
            logger.info('Handler stopped because user {} did not give consent'.format(telegram_user_id))
        except Exception as error:
            error_handler(bot, message, error, get_message(lc).SERVERS_INVITE_SERVER_ERROR)
        finally:
            is_running = False
            telegram_user_id = None
            user = None


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    global is_running, telegram_user_id, user
    lc = None
    if not is_running:
        try:
            user = None
            telegram_user_id = str(message.from_user.id)
            logger.info('Received invite command message from {}'.format(telegram_user_id, message.chat.id))
            bot_stop(bot, message)
        except DispatcherHandlerStop:
            logger.info('Handler stopped because user {} did not give consent'.format(telegram_user_id))
        except Exception as error:
            error_handler(bot, message, error, get_message(lc).COMMON_ERROR_MESSAGE)
        finally:
            is_running = False
            telegram_user_id = None
            user = None


@bot.callback_query_handler(func=lambda call: True)
def callback_query(query):
    global telegram_user_id, user
    lc = None
    user = None
    telegram_user_id = str(query.message.from_user.id)
    if telegram_user_id == bot_telegram_user_id:
        logger.info('Message received from us. Settings chat as user id.')
        telegram_user_id = str(query.message.chat.id)
    user = set_user_if_not_exists(user, query.message)
    lc = user.get('settings').get('language_code')
    logger.info("Callback query handler data is {}".format(query.data))
    # server
    if query.data == "action":
        try:
            logger.info("Add action")
        except Exception as error:
            error_handler(bot, query.message, error, get_message(lc).USER_SETTINGS_UPDATE_ERROR)
    elif query.data.startswith("another_action"):
        logger.info("Add another action")
    else:
        bot.send_message(query.message.chat.id, get_message(lc).MENU_OPTION_IS_NOT_AVAILABLE_YET)


@bot.pre_checkout_query_handler(func=lambda call: True)
def pre_checkout_query(query):
    global telegram_user_id, user
    lc = None
    user = None
    telegram_user_id = str(query.from_user.id)
    if telegram_user_id == bot_telegram_user_id:
        logger.info('Message received from us. Settings chat as user id.')
    user = set_user_if_not_exists(user, query.message)
    lc = user.get('settings').get('language_code')
    logger.info("Pre checkout callback query handler data is {}".format(query))
    try:
        good_id = query.invoice_payload
        price = 5000
        amount = int(price * 100)
        # server
        if query.total_amount == amount:
            bot.answer_pre_checkout_query(
                pre_checkout_query_id=query.id,
                ok=True,
                error_message=None
            )
        else:
            bot.answer_pre_checkout_query(
                pre_checkout_query_id=query.id,
                ok=False,
                error_message=get_message(lc).COMMON_ERROR_MESSAGE
            )
    except Exception as error:
        error_handler_from_user(bot, telegram_user_id, error, get_message(lc).COMMON_ERROR_MESSAGE)


@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    global telegram_user_id, user
    lc = None
    user = None
    telegram_user_id = str(message.from_user.id)
    if telegram_user_id == bot_telegram_user_id:
        logger.info('Message received from us. Settings chat as user id.')
    user = set_user_if_not_exists(user, message)
    lc = user.get('settings').get('language_code')
    logger.info("Received successful payment message: {}".format(message))
    received_successful_payment = message.successful_payment
    bot.send_message(message.from_user.id, get_message(lc).SUC
                     .format(received_successful_payment.provider_payment_charge_id))
    try:
        subscription_id = received_successful_payment.invoice_payload
        receipt = {'total_amount': received_successful_payment.total_amount,
                   'currency': received_successful_payment.currency,
                   'invoice_payload': received_successful_payment.invoice_payload,
                   'provider_payment_charge_id': received_successful_payment.provider_payment_charge_id,
                   'telegram_payment_charge_id': received_successful_payment.telegram_payment_charge_id,
                   'date': datetime.now(timezone.utc).isoformat(),
                   'telegram_user_id': str(message.from_user.id),
                   'telegram_chat_id': str(message.chat.id),
                   }
        bot.send_message(message.from_user.id, get_message(lc).USERS_CREATE_CONFIG)
    except Exception as error:
        error_handler_from_user(bot, telegram_user_id, error, get_message(lc).SUBSCRIPTIONS_CREATE_SUBSCRIPTION_ERROR)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    global telegram_user_id, user
    lc = None
    user = None
    telegram_user_id = str(message.from_user.id)
    if telegram_user_id == bot_telegram_user_id:
        logger.info('Message received from us. Settings chat as user id.')
    user = set_user_if_not_exists(user, message, False)
    lc = user.get('settings').get('language_code')
    text = message.text.lower()
    chat_id = message.chat.id
    logger.info('Received message from {} to chatting: {}'.format(user.get('id'), text))
    try:
        if text == "привет" or text == "hi":
            bot.send_message(chat_id, get_message(lc).CHAT_HI)
        elif text == "как дела?" or text == get_message(lc).CHAT_HOW_ARE_YOU:
            bot.send_message(chat_id, get_message(lc).CHAT_HOW_ARE_YOU_ANSWER)
        elif text == "help" or text == "помощь":
            bot.send_message(chat_id, get_message(lc).HELP_MESSAGE)
        else:
            bot.send_message(chat_id, get_message(lc).UNKNOWN_CHAT_MESSAGE, reply_markup=keyboards.create_app_keyboard())
    except Exception as error:
        error_handler(bot, message, error, get_message(lc).COMMON_ERROR_MESSAGE)
    finally:
        telegram_user_id = None
        user = None


def set_user_if_not_exists(_user, message, is_consent_accept_required=True, next_handler=start_handler):
    logger.info('Set user {} if not exists'.format(telegram_user_id))
    lc = message.from_user.language_code
    try:
        result = users_service.get_or_create_user(telegram_user_id, lc) if user is None else _user
        logger.debug("User profile is {}".format(result))
        if is_consent_accept_required:
            logger.info("Check if consent is accepted")
            check_if_agreements_accepted(result, message, next_handler)
        logger.info('Set user {} as {}'.format(telegram_user_id, result.get('id')))
        return result
    except DispatcherHandlerStop:
        raise DispatcherHandlerStop
    except Exception as error:
        error_handler_from_user(bot, str(telegram_user_id), error,
                                get_message(lc).USER_SETTINGS_UPDATE_ERROR)


def check_if_agreements_accepted(_user, message, next_handler):
    is_accepted = _user.get('settings').get('is_consent_accepted')
    if is_accepted is False:
        save_deep_link_action(message)
        user_settings_commands.ask_consent(message, bot, _user, next_handler)
        raise DispatcherHandlerStop()


def deep_link_action(message, _user):
    logger.info('Executing deep_link_action for user {}'.format(_user.get('id')))
    global deep_link_action_state
    start_param = get_deep_link_action(message)
    if start_param:
        logger.info('Executing deep_link_action start_param is {}'.format(start_param))
        deep_link_action_state = None
        query = CallbackQuery(id=0, chat_instance=message.chat, data=start_param, from_user=message.from_user,
                              message=message, json_string='')
        callback_query(query)


def get_deep_link_action(message):
    global deep_link_action_state
    start_param = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else deep_link_action_state
    return start_param


def save_deep_link_action(message):
    global deep_link_action_state
    deep_link_action_state = get_deep_link_action(message)


bot.polling(none_stop=True)
