from datetime import datetime

from bot.localised_messages import get_message


def format_datetime(date, lc):
    return datetime.strftime(date, get_message(lc).COMPATIBLE_DATETIME_FORMAT)


def format_date(date, lc):
    return datetime.strftime(date, get_message(lc).COMPATIBLE_DATE_FORMAT)
