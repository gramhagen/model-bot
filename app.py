"""WSGI Application"""

from app_factory import create_app

app = create_app(config_env='ProdConfig')
