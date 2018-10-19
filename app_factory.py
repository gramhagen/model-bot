import json
import uuid

from flask import Flask, request, current_app

from clients import get_slack_client, get_datastore_client, get_prediction_client


def build_attachments(probabilities, callback_id):
    """Helper method to build slack interactive message attachments

    Args:
        probabilities (dict): class: probability
        callback_id (str): unique id for callback
    Retuns:
        (dict): attachments data structure
    """
    attachments = []
    for key, value in probabilities.items():
        action = dict(name='name',
                      type='button',
                      text='{key} : {value:.2f}%'.format(key=key.title(), value=value * 100),
                      value=key)
        attachments.append(dict(fallback='',
                                callback_id=callback_id,
                                color='#3AA3E3',
                                attachment_type='default',
                                actions=[action]))

    attachments.sort(key=lambda x: x['actions'][0]['value'])
    attachments.append(dict(fallback='',
                            callback_id=callback_id,
                            color='#3AA3E3',
                            attachment_type='default',
                            actions=[dict(name='name',
                                          type='button',
                                          text='None of the Above',
                                          value='other')]))

    return attachments


def create_app(config_env='ProdConfig'):

    app = Flask(__name__)
    app.config.from_object('config.{}'.format(config_env))
    app.logger.setLevel(app.config['LOG_LEVEL'])

    @app.route('/modelbot/events', methods=['POST'])
    def events():
        """
        This function verifies the app for slack integration and handles all interaction with slack and model serving

        Returns:
            HTTP Response (tuple): (str: JSON response, int: HTTP status code)
        """
        try:
            # extract form or json payload
            data = json.loads(request.data or request.form.getlist('payload')[0])
            app.logger.info('Received data: %s', data)
        except:
            return 'Invalid request', 404

        if data.get('token') != current_app.config['APP_TOKEN']:
            return 'Invalid Token', 401

        slack_client = get_slack_client()
        datastore_client = get_datastore_client()
        predict_client = get_prediction_client()

        if data['type'] == 'url_verification':
            return json.dumps(dict(challenge=data['challenge'])), 200

        elif data['type'] == 'event_callback':
            event_data = data['event']

            if event_data['user'] == app.config['BOT_ID']:
                # don't respond to message from the bot itself
                return 'OK', 200

            # remove bot reference and clean up string
            user_text = (event_data['text']
                         .replace('<@{}>'.format(app.config['BOT_ID']), '')
                         .strip()
                         .encode('utf-8'))

            # create unique session id
            session_id = uuid.uuid4().hex

            # store the message details
            user_input_payload = dict(
                eventType=event_data['type'],
                userId=event_data['user'],
                channelId=event_data['channel'],
                teamId=data['team_id'],
                text=user_text,
                timestamp=event_data['event_ts'])
            app.logger.debug('Datastore - sending user input data: %s', user_input_payload)
            datastore_client.post(session_id=session_id, data_type='user_input', data=user_input_payload)
            app.logger.debug('Datastore - user input data sent')

            # get predictions from prediction service
            app.logger.debug('Prediction - predicting input: %s', user_text)
            prediction = predict_client.predict(text=user_text)
            app.logger.debug('Prediction - result: %s', prediction)

            prediction_payload = dict(
                model_type=prediction['model_type'],
                model_version=prediction['model_version'],
                predicted_name=prediction['prediction'],
                probabilities=prediction['probabilities'],
                tokens=prediction['tokens']
            )
            app.logger.debug('Datastore - sending prediction data: %s', prediction_payload)
            datastore_client.post(session_id=session_id, data_type='prediction', data=prediction_payload)
            app.logger.debug('Datastore - prediction data sent')

            text = 'Okay, I heard: {}\nPlease select the correct response from the buttons below.'.format(user_text)
            attachments = build_attachments(probabilities=prediction['probabilities'], callback_id=session_id)
            slack_client.post_message(channel=event_data['channel'],
                                      text=text,
                                      user=event_data['user'],
                                      attachments=attachments)

            return 'OK', 200

        elif data['type'] == 'interactive_message':
            selection = data['actions'][0]['value']
            payload = dict(userId=data['user']['id'],
                           channelId=data['channel']['id'],
                           teamId=data['team']['id'],
                           selectedName=selection,
                           timestamp=data['message_ts'])
            datastore_client.post(session_id=data['callback_id'], data_type='feedback', data=payload)

            return '{}, got it. Thanks!'.format(selection.title()), 200

        else:
            return 'Invalid data type', 400

    return app
