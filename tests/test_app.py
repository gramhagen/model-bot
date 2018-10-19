import json

from app_factory import create_app


def test_config():
    """Test create_app"""
    assert not create_app().testing
    assert create_app('TestConfig').testing


def test_invalid_token(client):
    response = client.post('/modelbot/events', json={'token': ''})
    assert response.data == b'Invalid Token'
    assert response.status_code == 401


def test_challenge(client):
    json_data = dict(token='APP_TOKEN', type='url_verification', challenge='challenge')
    response = client.post('/modelbot/events', json=json_data)
    assert json.loads(response.data) == dict(challenge='challenge')
