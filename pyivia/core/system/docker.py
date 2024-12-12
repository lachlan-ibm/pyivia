"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


DOCKER = "/docker"

logger = logging.getLogger(__name__)


class Docker(object):

    def __init__(self, base_url, username, password):
        super(Docker, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def publish(self):
        """
        Publish the current configuration snapshot.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the snapshot id is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = DOCKER + "/publish"

        response = self.client.put_json(endpoint)
        response.success = response.status_code == 201

        return response


    def stop(self):
        """
        Stop the configuration container

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        endpoint = DOCKER + '/stop'

        response = self.client.put_json(endpoint)
        response.success = response.status_code == 204

        return response
