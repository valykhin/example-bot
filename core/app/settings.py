import os
import core.app.config as config


class Config(object):
    """Base configuration."""
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://core:vp.pwd.4.core@localhost:5432/core')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGER_CONFIGURATION_FILE = os.environ.get('LOGGER_CONFIGURATION_FILE', 'app/logging.conf')
    CLIENT_HOST = "45.67.230.163:8000"
    CLIENT_API_URL = os.environ.get("CLIENT_API_URL", "http://{}/api")
    BASIC_AUTH_PROMETHEUS_USER = os.environ.get(config.BASIC_AUTH_PROMETHEUS_USER, "prometheus")
    BASIC_AUTH_PROMETHEUS_PASSWORD = os.environ.get(config.BASIC_AUTH_PROMETHEUS_PASSWORD, "typxsyCstN")
    BASIC_AUTH_CLIENT_USER = os.environ.get(config.BASIC_AUTH_CLIENT_USER, "client")
    BASIC_AUTH_CLIENT_PASSWORD = os.environ.get(config.BASIC_AUTH_CLIENT_PASSWORD, "69CUF5gm8I")
    BASIC_AUTH_CORE_USER = os.environ.get(config.BASIC_AUTH_CORE_USER, "core")
    BASIC_AUTH_CORE_PASSWORD = os.environ.get(config.BASIC_AUTH_CORE_PASSWORD, "KP6fRbz96q")


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True


class TestConfig(Config):
    """Test configuration."""
    ENV = 'test'
    TESTING = True
    DEBUG = True


config_by_name = dict(
    dev=DevConfig,
    test=TestConfig,
    prod=ProdConfig
)
