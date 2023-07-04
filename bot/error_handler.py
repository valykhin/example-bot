import html
import logging.config
from telebot.types import Message

from bot.service import keyboards
logger = logging.getLogger('root')

SUPPORT_CHAT_ID = 127487825


def error_handler(robot, msg: Message, exception, user_friendly_error_message=None) -> None:
    logger.error(msg="Exception while handling communication:", exc_info=exception)
    message = (
        f"An exception was raised while handling communication\n"
        "</pre>\n\n"
        f"<pre>chat = {html.escape(str(msg.from_user.id))}</pre>\n\n"
        f"<pre>user = {html.escape(str(msg.chat.id))}</pre>\n\n"
        f"<pre>{html.escape(str(exception))}</pre>"
        f"<pre>message = {html.escape(str(msg))}</pre>\n\n"
    )
    # robot.send_message(SUPPORT_CHAT_ID, text=message, parse_mode=ParseMode.HTML)
    if user_friendly_error_message:
        robot.send_message(msg.chat.id, user_friendly_error_message, reply_markup=keyboards.create_app_keyboard())


def error_handler_from_user(robot, from_user_id: str, exception, user_friendly_error_message=None) -> None:
    logger.error(msg="Exception while handling communication:", exc_info=exception)
    message = (
        f"An exception was raised while handling communication\n"
        "</pre>\n\n"
        f"<pre>chat = {html.escape(str(from_user_id))}</pre>\n\n"
        f"<pre>user = {html.escape(str(from_user_id))}</pre>\n\n"
        f"<pre>{html.escape(str(exception))}</pre>"
    )
    # robot.send_message(SUPPORT_CHAT_ID, text=message, parse_mode=ParseMode.HTML)
    if user_friendly_error_message:
        robot.send_message(from_user_id, user_friendly_error_message, reply_markup=keyboards.create_app_keyboard())
