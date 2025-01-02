"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


CAPABILITIES = "/isam/capabilities"

logger = logging.getLogger(__name__)


class Licensing(object):

    def __init__(self, base_url, username, password):
        super(Licensing, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def activate_module(self, code):
        """
        Apply a licensing code to activate a module.

        Args:
            code (:obj:`str`): The new activation code. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        data.add_value_string("code", code)

        endpoint = CAPABILITIES + "/v1"

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def get_activated_module(self, module_id):
        """
        Get a specific active offering.

        Args:
            module_id (:obj:`str`): ID of the specified Activation offering.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the active module configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = "%s/%s/v1" % (CAPABILITIES, module_id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_activated_modules(self):
        """
        Get a list of all of the active modules

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the active module configurations are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = CAPABILITIES + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def import_activation_code(self, file_path):
        """
        Import an activation code from a file.

        Args:
            file_path (:obj:`str`): Absolute path to file containing the activation code.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the active module is returned as JSON and can be accessed from
            the response.json attribute
        """
        response = Response()

        try:
            with open(file_path, 'rb') as code:
                data = DataObject()
                data.add_value_string("name", "activation")

                files = {"filename": code}

                endpoint = CAPABILITIES + "/v1"

                response = self.client.post_file(
                    endpoint, data=data.data, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response
