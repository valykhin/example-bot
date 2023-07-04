import json
from werkzeug.exceptions import InternalServerError, HTTPException
import logging

logger = logging.getLogger('root')


def handle_exception(e):
    logger.error(e)
    if isinstance(e, HTTPException):
        exception = e
        response = e.get_response()
    else:
        exception = InternalServerError(str(e))
        response = exception.get_response()
    data = {
        "code": exception.code,
        'error_code': exception.error_code if hasattr(exception, 'error_code') else exception.name.lower().replace(' ',
                                                                                                                   '_'),
        "name": exception.name,
        "description": exception.description,
    }
    response.data = json.dumps(data)
    response.content_type = "application/json"
    return response
