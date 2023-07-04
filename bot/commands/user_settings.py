import logging.config

from bot.localised_messages import get_message
from bot.error_handler import error_handler
from bot.service.users import update_user_settings
from bot.service import keyboards

logger = logging.getLogger('root')


def ask_consent(message, robot, user, next_handler=None):
    lc = None
    try:
        logger.info('Received ask_consent message for user {}'.format(str(user.get('id'))))
        lc = user.get('settings').get('language_code')
        msg = robot.send_message(message.chat.id, get_message(lc).USER_AGREEMENTS_MESSAGE,
                                 reply_markup=keyboards.create_text_menu([{'label': get_message(lc).YES},
                                                                          {'label': get_message(lc).NO}]))
        robot.register_next_step_handler(msg, set_consent, robot, user, next_handler)
    except Exception as error:
        error_handler(robot, message, error, get_message(lc).USER_SETTINGS_UPDATE_ERROR)


def set_consent(message, robot, user, next_handler):
    lc = None
    try:
        logger.info('Received set_consent message from user {}'.format(user.get('id')))
        lc = user.get('settings').get('language_code')
        answer = message.text
        if answer not in [get_message(lc).YES, get_message(lc).NO]:
            msg = robot.send_message(message.chat.id, get_message(lc).USER_AGREEMENTS_NOT_VALID_ANSWER)
            robot.register_next_step_handler(msg, ask_consent, robot, user)
            return
        if answer == get_message(lc).YES:
            update_user_settings(user.get('id'), {'is_consent_accepted': True})
            robot.send_message(message.chat.id, get_message(lc).USER_AGREEMENTS_SUCCESS)
            next_handler(message)
    except Exception as error:
        error_handler(robot, message, error, get_message(lc).USER_SETTINGS_UPDATE_ERROR)
