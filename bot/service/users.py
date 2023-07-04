import logging.config

from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from common.dto.user import users_dto, user_dto
from bot.api import core


def list_users(telegram_id):
    users = users_dto.load(core.list_users(telegram_id))
    return users


def get_or_create_user(telegram_id, language_code):
    response = core.create_user(telegram_id, language_code)
    user = user_dto.load(response)
    return user


def update_user_settings(user_id, settings):
    user = user_dto.load(core.patch_user(user_id, {'settings': settings}))
    return user
