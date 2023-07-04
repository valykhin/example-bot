from pathlib import Path
import sys
import logging
import config

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from common.api import send_request

logger = logging.getLogger('root')

CORE_SERVER_API_URL = config.CORE_SERVER_API_URL

auth = {
    'username': config.BASIC_AUTH_CORE_USER,
    'password': config.BASIC_AUTH_CORE_PASSWORD,
}


def list_users(telegram_id):
    url = '{}/users?telegram_id={}'.format(CORE_SERVER_API_URL, telegram_id)
    return send_request('GET', url, str(telegram_id), auth=auth)


def create_user(telegram_id, language_code='en'):
    url = '{}/users'.format(CORE_SERVER_API_URL)
    user = {'telegram_id': str(telegram_id),
            'settings': {'language_code': language_code}}
    return send_request('POST', url, str(telegram_id), user, auth=auth)


def patch_user(user_id, data):
    url = '{}/users/{}'.format(CORE_SERVER_API_URL, user_id)
    return send_request('PATCH', url, str(user_id), data, auth=auth)
