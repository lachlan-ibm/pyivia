""""
@copyright: IBM
"""

import logging
import urllib

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

FSSO_CONFIG = "/wga/fsso_config"

class FSSO(object):

    def __init__(self, base_url, username, password):
        super(FSSO, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, fsso_config_data=None):
        """
        Create a Federated Single Sign On configuration.

        Args:
            name (:obj:`str`): The name of the FSSO config.
            fsso_config_data (:obj:`str`): The serialized FSSO configuration data.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created FSSO config can be accessed from the
            response.id_from_location attribute.
        """
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("fsso_config_data", fsso_config_data)

        response = self.client.post_json(FSSO_CONFIG, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, fsso_id=None, fsso_config_data=None):
        """
        Update a Federated Single Sign On configuration.

        Args:
            fsso_id (:obj:`str`): The name of the FSSO config.
            fsso_config_data (:obj:`str`): The serialized FSSO configuration data.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.
        """
        data = DataObject()
        data.add_value("fsso_config_data", fsso_config_data)
        endpoint = FSSO_CONFIG + "/{}".format(fsso_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self, fsso_id=None):
        """
        Update a Federated Single Sign On configuration.

        Args:
            fsso_id (:obj:`str`): The name of the FSSO config.
            fsso_config_data (:obj:`str`): The serialized FSSO configuration data.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.
        """
        endpoint = FSSO_CONFIG + "/{}".format(fsso_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, fsso_id):
        '''
        Get a FSSO configuration.

        Args:
            fsso_id (:obj:`str`): The id of the FSSO config to return.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the FSSO configuration is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = FSSO_CONFIG + "/{}".format(fsso_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        Return list of all FSSO configurations.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the FSSO configurations are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        response = self.client.get_json(FSSO_CONFIG)
        response.success = response.status_code == 200

        return response
