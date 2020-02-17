"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


DOCKER = "/docker"

logger = logging.getLogger(__name__)


class Docker(object):

    def __init__(self, base_url, username, password):
        super(Docker, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def publish(self):

        endpoint = DOCKER + "/publish"

        response = self.client.put_json(endpoint)
        response.success = response.status_code == 201

        return response


    def stop(self):
        endpoint = DOCKER + '/stop'

        response = self.client.put_json(endpoint)
        response.success = response.status_code == 204

        return response
