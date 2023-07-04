import requests
from requests.auth import HTTPBasicAuth
import logging.config
from werkzeug.exceptions import UnprocessableEntity, NotFound, InternalServerError

from common.model.exceptions import UserAlreadyExistsException

logger = logging.getLogger('root')


def send_request(method: str, url, user_id: str = None, data=None, auth=None):
    logger.info('Send {} request: {}'.format(method, url))
    headers = {}
    if auth:
        basic_auth = HTTPBasicAuth(auth['username'], auth['password'])
    else:
        basic_auth = {}
    try:
        if user_id:
            headers.update({'x-request-user-id': user_id})
        if method.lower() == 'post':
            logger.info('Send {} request: {} data: {}'.format(method, url, data))
            response = requests.post(url, json=data, headers=headers, auth=basic_auth)
        elif method.lower() == 'delete':
            response = requests.delete(url, headers=headers, auth=basic_auth)
        elif method.lower() == 'patch':
            logger.info('Send {} request: {} data: {}'.format(method, url, data))
            response = requests.patch(url, json=data, headers=headers, auth=basic_auth)
        else:
            response = requests.get(url, headers=headers, auth=basic_auth)
        logger.debug('Response received {}: {}'.format(response.status_code, response.text))
        if 200 <= response.status_code < 205:
            result = response.json() if response.text != '' else None
        elif response.status_code == 403:
            raise PermissionError(response.text)
        elif response.status_code == 404:
            raise NotFound(response.text)
        elif response.status_code == 422:
            error = response.json()
            logger.info("Error is {}".format(error))
            if error.get('error_code', '') == 'user_already_exists':
                raise UserAlreadyExistsException()
            else:
                raise UnprocessableEntity(response.text)
        elif response.status_code == 500:
            raise InternalServerError(response.text)
        else:
            raise Exception(response.text)
    except BaseException:
        raise
    except PermissionError:
        raise
    return result
