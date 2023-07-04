import pytest


from core.app import create_app
from core.app.settings import TestConfig


@pytest.fixture(scope='function')
def app():
    return create_app(TestConfig)
