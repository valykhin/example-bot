import logging.config
from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from marshmallow import ValidationError

from core.app import auth
from ..dto.exceptions import InvalidUsage
from ..dto.user import user_dto, users_dto
from ..service import users as users_service

users_api = Blueprint('users', __name__)
logger = logging.getLogger('core')


@users_api.route('/users', methods=('GET',))
@marshal_with(users_dto)
@auth.login_required
def get_user_list():
    """
       ---
       get:
         summary: Get users list
         responses:
           '200':
             description: Get active users list
             content:
               application/json:
                 schema: UserList
         tags:
           - users
       """
    logger.info("Received {} request: {}".format(request.method, request.path))
    args = request.args
    telegram_id = args.get('telegram_id', None)
    users = users_service.get_users(telegram_id)
    return users


@users_api.route('/users', methods=('POST',))
@use_kwargs(user_dto)
@marshal_with(user_dto)
@auth.login_required
def create_user(**kwargs):
    """
       ---
       post:
         summary: Create user
         responses:
           '200':
             description: Create new user
             content:
               application/json:
                 schema: User
         tags:
           - users
       """
    logger.info("Received {} request: {}".format(request.method, request.path))
    json_input = request.get_json()
    try:
        data = user_dto.load(json_input)
    except ValidationError as err:
        logger.error("Error {}: {}".format(type(err), err.messages))
        raise InvalidUsage.validation_error()
    user = users_service.create_user(data)
    return user


@users_api.route('/users/<user_id>', methods=('GET',))
@marshal_with(user_dto)
@auth.login_required
def get_user(user_id):
    """
       ---
       get:
         summary: Get user by id
         responses:
           '200':
             description: Get active user by id
             content:
               application/json:
                 schema: User
         tags:
           - users
       """
    logger.info("Received {} request: {}".format(request.method, request.path))
    user = users_service.get_user(user_id)
    return user


@users_api.route('/users/<user_id>', methods=('DELETE',))
@marshal_with(user_dto)
@auth.login_required
def delete_user(user_id=""):
    """
       ---
       delete:
         summary: Delete user by id
         responses:
           '200':
             description: Delete active user by id
             content:
               application/json:
                 schema: User
         tags:
           - users
       """
    logger.info("Received {} request: {}".format(request.method, request.path))
    user = users_service.delete_user(user_id)
    return user


@users_api.route('/users/<user_id>', methods=('PATCH',))
@marshal_with(user_dto)
@auth.login_required
def patch_user(user_id):
    """
       ---
       patch:
         summary: Update user by id
         responses:
           '200':
             description: Patch user by id
             content:
               application/json:
                 schema: User
         tags:
           - users
       """
    logger.info("Received {} request: {}".format(request.method, request.path))
    json_input = request.get_json()
    try:
        data = user_dto.load(json_input, partial=True)
    except ValidationError as err:
        logger.error("Error {}: {}".format(type(err), err.messages))
        raise InvalidUsage.validation_error()
    user = users_service.patch_user(user_id, data)
    return user
