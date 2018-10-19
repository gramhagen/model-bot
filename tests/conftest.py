import pytest

from app_factory import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test"""
    # create the app with test config
    app = create_app(config_env='TestConfig')

    yield app


@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()
