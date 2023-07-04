import logging.config
from ..config import CLIENT_API_URL, BASIC_AUTH_CLIENT_USER, BASIC_AUTH_CLIENT_PASSWORD
from flask import current_app

from common.api import send_request


logger = logging.getLogger('root')


def get_auth():
    return {
        'username': current_app.config.get(BASIC_AUTH_CLIENT_USER),
        'password': current_app.config.get(BASIC_AUTH_CLIENT_PASSWORD),
    }


def get_user(server, user_id):
    server_api_url = current_app.config.get(CLIENT_API_URL).format(server)
    url = '{}/users/{}'.format(server_api_url, user_id)
    return send_request('GET', url, user_id, auth=get_auth())
