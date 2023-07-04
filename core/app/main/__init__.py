from flask import Flask

from ..settings import config_by_name
from ..error_handler import handle_exception


def init_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.url_map.strict_slashes = False
    app.register_error_handler(Exception, handle_exception)
    return app



