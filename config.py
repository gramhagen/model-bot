import logging


class Config(object):
    DEBUG = False
    TESTING = False

    LOG_LEVEL = logging.DEBUG


class ProdConfig(Config):

    APP_TOKEN = "APP_TOKEN"
    BOT_TOKEN = "BOT_TOKEN"
    BOT_ID = "BOT_ID"

    DATASTORE_CFG = dict(url='', token='', payload_type='', payload_version='')
    PREDICTION_CLIENT = 'sklearn'
    PREDICTION_CFG = dict(host='', port='', model_type='', model_version='', labels='', pad_len='', pad_tok='')

    LOG_LEVEL = logging.ERROR


class TestConfig(Config):
    TESTING = True

    APP_TOKEN = "APP_TOKEN"
    BOT_TOKEN = "BOT_TOKEN"
    BOT_ID = "BOT_ID"

    DATASTORE_CFG = dict(url='', token='', payload_type='', payload_version='')
    PREDICTION_CLIENT = 'sklearn'
    PREDICTION_CFG = dict(host='', port='', model_type='', model_version='', labels='', pad_len='', pad_tok='')
