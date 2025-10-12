"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


FIXPACKS = "/fixpacks"

logger = logging.getLogger(__name__)


class Fixpacks(object):

    def __init__(self, base_url, username, password):
        super(Fixpacks, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def install_fixpack(self, file_path) -> Response:
        """
        Install a signed fixpack.

        Args:
            file_path (:obj:`str`): Absolute path to fixpack to be uploaded to an appliance.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        response = Response()

        try:
            with open(file_path, 'rb') as fixpack:
                data = DataObject()
                data.add_value_string("type", "application/octect-stream")

                files = {"file": fixpack}

                endpoint = FIXPACKS

                response = self.client.post_file(
                    endpoint, data=data.data, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def list_fixpacks(self):
        """
        List the installed fixpacks.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the installed fixpacks are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = FIXPACKS

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_fips_mode(self):
        """
        Get the FIPS compliance mode of an appliance.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the FIPS settings is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = FIXPACKS + "/fipsmode"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def rollback_fixpack(self):
        """
        Roll back the most recently installed fixpack

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        endpoint = FIXPACKS

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
