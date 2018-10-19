# -*- coding: utf-8 -*-
"""DataStore Client"""

import uuid
from datetime import datetime

import requests


class DataStoreClient:
    """Data Store Client"""

    headers = None
    url = None

    def __init__(self, url, token, payload_type, payload_version):
        """Initialize clients"""
        self.headers = {'Authorization': 'Bearer {}'.format(token)}
        self.url = url
        self.payload_type = payload_type
        self.payload_version = payload_version

    def post(self, session_id, data_type, data):
        """Send request to service

        Args:
            session_id (str): unique for session
            data_type (str): one of [user_input, prediction, feedback]
            data (dict): data to send
        Returns:
            (dict): response
        """

        # TODO: check data type and data validity
        data = dict(envelope=dict(payloadProtocolVersion=self.payload_version,
                                  payloadType=self.payload_type,
                                  time=datetime.utcnow().isoformat('T')[:-3] + 'Z',
                                  uniqueId=uuid.uuid4().hex,
                                  protocolVersion="1.0"),
                    payload=dict(sessionId=session_id,
                                 dataType=data_type,
                                 data=data))

        response = requests.post(url=self.url, headers=self.headers, json=data)

        if response.status_code != 200:
            raise Exception('Received error storing data: {}'.format(response.content))
