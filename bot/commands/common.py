import logging.config

from bot.localised_messages import DefaultMessages

logger = logging.getLogger('root')


def get_command_value(data):
    return data[data.index("-")+1:]


def value_is_valid(robot, message, value, handler, *args):
    if not all(c in DefaultMessages.COMPATIBLE_CHARS for c in value):
        return


def bot_stop(robot, message):
    robot.restrict_chat_member(message.chat.id, message.from_user.id, None,
                               can_send_messages=False,
                               can_send_media_messages=False,
                               can_send_polls=False,
                               can_send_other_messages=False,
                               can_add_web_page_previews=False,
                               can_change_info=False,
                               can_invite_users=False,
                               can_pin_messages=False)
