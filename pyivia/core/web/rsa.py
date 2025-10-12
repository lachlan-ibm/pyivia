""""
@copyright: IBM
"""

import logging
import urllib

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

RSA_CONFIG = "/wga/rsa_config"

class RSA(object):

    def __init__(self, base_url, username, password):
        super(RSA, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, server_config_file=None, server_options_file=None):
        """
        Configure WebSEAL to use a RSA token server for authentication.

        Args:
            server_config_file (:obj:`str`): Full path to RSA SecurID toke server configuration file.
            server_options_file (:obj:`str`, optional): Full path to the server configuration options file to upload.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        response = Response()
        if not server_config_file or not server_options_file:
            response.success = False
            return response

        endpoint = RSA_CONFIG + "/server_config"
        try:
            files = {"server_config": open(server_config_file, "rb")}
            if server_options_file:
                files.update({"server_opts_file": open(server_options_file, 'rb')})
            response = self.client.post_file(endpoint, files=files)
            response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def get(self):
        """
        Get the RSA configuration file.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the rate limiting policy is returned as JSON and can be accessed from
            the response.json attribute

        """
        response = self.client.get_json(RSA_CONFIG)
        response.success = response.status_code == 200

        return response


    def test(self, username=None, password=None):
        """
        Test the RSA SecurID configuration.

        Args:
            username (:obj:`str`): The username to authenticate as
            password (:obj:`str`): The passcode of the user to authenticate with

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = RSA_CONFIG + "/test"

        data = DataObject()
        data.add_value_string("username", username)
        data.add_value_string("password", password)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self):
        """
        Delete the RSA SecurID configuration

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = RSA_CONFIG + "/server_config"
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def delete_node_secret(self):
        """
        Delete the local secret for the  RSA token server.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = RSA_CONFIG + "/nose_secret"
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
