""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

RSA_CONFIG = "/wga/rsa_config"

class RSA(object):

    def __init__(self, base_url, username, password):
        super(RSA, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, server_config_file=None):
        response = Response()
        endpoint = RSA_CONFIG + "/server_config"
        try:
            with open(server_config_file, "r") as server_config:
                files = {"server_config": server_config}
                response = self.client.post_file(endpoint, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def get(self):
        response = self.client.get_json(RSA_CONFIG)
        response.success = response.status_code == 200

        return response


    def test(self, username=None, password=None):
        endpoint = RSA_CONFIG + "/test"

        data = DataObject()
        data.add_value_string("username", username)
        data.add_value_string("password", password)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self):
        endpoint = RSA_CONFIG + "/server_config"
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def delete_node_secret(self):
        endpoint = RSA_CONFIG + "/nose_secret"
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
