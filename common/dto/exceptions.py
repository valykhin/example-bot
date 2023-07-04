from flask import jsonify
from werkzeug.exceptions import HTTPException


def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}


USER_NOT_FOUND = template(['User not found'], code=404)
USER_ALREADY_REGISTERED = template(['User already registered'], code=422)
UNKNOWN_ERROR = template([], code=500)
NODE_NOT_FOUND = template(['Node not found'], code=404)
VALIDATION_ERROR = template(['Validation error'], code=422)


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def user_not_found(cls):
        return cls(**USER_NOT_FOUND)

    @classmethod
    def user_already_registered(cls):
        return cls(**USER_ALREADY_REGISTERED)

    @classmethod
    def unknown_error(cls):
        return cls(**UNKNOWN_ERROR)

    @classmethod
    def article_not_found(cls):
        return cls(**NODE_NOT_FOUND)

    @classmethod
    def validation_error(cls):
        return cls(**VALIDATION_ERROR)


class UserAlreadyExistsException(HTTPException):
    code = 422
    error_code = 'user_already_exists'
    description = (
        "User already exists."
    )

    def __init__(
        self,
        description: str = None,
    ) -> None:
        super().__init__()
        if description:
            self.description = description
    pass
