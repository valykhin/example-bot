import json
import logging.config
import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint


from core.app import commands
from .main import init_app
from .config import LOGGER_CONFIGURATION_FILE
from .extensions import db, migrate, bcrypt, metrics, scheduler, auth

from .main.controller.users import users_api

from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

from .config import BASIC_AUTH_PROMETHEUS_USER, BASIC_AUTH_PROMETHEUS_PASSWORD, \
    BASIC_AUTH_CLIENT_USER, BASIC_AUTH_CLIENT_PASSWORD, BASIC_AUTH_CORE_USER, BASIC_AUTH_CORE_PASSWORD

from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from common.dto.user import users_dto, user_dto

users = {}


def create_app(test_config=None):
    app = init_app(os.getenv('APP_ENV') or 'prod')
    logging.config.fileConfig(app.config.get(LOGGER_CONFIGURATION_FILE))

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    users.update(users_init(app))

    return app


def register_extensions(app):
    bcrypt.init_app(app)
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    metrics.init_app(app)
    scheduler.init_app(app)
    scheduler.start()


def register_blueprints(app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    swagger_blueprint = Blueprint('swagger', __name__, url_prefix='/')
    swagger_blueprint.register_blueprint(create_swagger(app))
    swagger_blueprint.register_blueprint(create_swagger_ui(app))

    blueprint.register_blueprint(users_api)

    app.register_blueprint(blueprint)
    app.register_blueprint(swagger_blueprint)


def register_commands(app):
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)


def create_swagger(app):
    swagger_api = Blueprint('swagger', __name__)

    @swagger_api.route('/swagger', methods=('GET',))
    @auth.login_required
    def create_swagger_spec():
        return json.dumps(get_apispec(app).to_dict())

    return swagger_api


def create_swagger_ui(app):
    swagger_url = '/docs'
    api_url = '/swagger'

    swagger_ui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={
            'app_name': 'Core'
        }
    )
    return swagger_ui_blueprint


def get_apispec(app):
    spec = APISpec(
        title="Core",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )
    spec.components.schema("User", schema=UserDto())
    spec.components.schema("UserList", schema=UserDto(many=True))
    load_docstrings(spec, app)
    return spec


def load_docstrings(spec, app):
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


def users_init(app):
    with app.app_context():
        _users = {
            current_app.config.get(BASIC_AUTH_CORE_USER):
                generate_password_hash(current_app.config.get(BASIC_AUTH_CORE_PASSWORD)),
            current_app.config.get(BASIC_AUTH_CLIENT_USER):
                generate_password_hash(current_app.config.get(BASIC_AUTH_CLIENT_PASSWORD)),
            current_app.config.get(BASIC_AUTH_PROMETHEUS_USER):
                generate_password_hash(current_app.config.get(BASIC_AUTH_PROMETHEUS_PASSWORD)),
        }
    return _users


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
