"""Wrapper for slack client"""
from slackclient import SlackClient


class SlackClientWrapper:
    """Slack Client Wrapper"""

    slack_client = None
    token = None

    def __init__(self, token):
        self.slack_client = SlackClient(token=token)
        self.token = token

    def post_message(self, channel, text, user, attachments):

        self.slack_client.api_call(
            'chat.postMessage',
            token=self.token,
            channel=channel,
            text=text,
            user=user,
            attachments=attachments,
            as_user=True)
