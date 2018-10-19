from flask import current_app, g

from clients.datastore import DataStoreClient
from clients.slackwrapper import SlackClientWrapper
from clients.tfserving import TFServingClient
from clients.sklearnclient import SklearnClient


def get_slack_client():
    if 'slack_client' not in g:
        g.slack_client = SlackClientWrapper(token=current_app.config['BOT_TOKEN'])
    return g.slack_client


def get_datastore_client():
    if 'datastore_client' not in g:
        g.datastore_client = DataStoreClient(**current_app.config['DATASTORE_CFG'])
    return g.datastore_client


def get_prediction_client():
    if 'prediction_client' not in g:
        if current_app.config['PREDICTION_CLIENT'] == 'tensorflow':
            g.prediction_client = TFServingClient(**current_app.config['PREDICTION_CFG'])
        else:
            g.prediction_client = SklearnClient(**current_app.config['PREDICTION_CFG'])
    return g.prediction_client
