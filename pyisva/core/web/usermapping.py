""""
@copyright: IBM
"""

import logging
import urllib

from pyisva.util.model import DataObject
from pyisva.util.restclient import RESTClient

logger = logging.getLogger(__name__)

USER_MAP_CDAS = "/wga/user_map_cdas"

class UserMapping(object):

    def __init__(self, base_url, username, password):
        super(UserMapping, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, content=None):
        """
        Create a new user mapping policy file.

        Args:
            name (:obj:`str`): The name of the new policy.
            content (:obj:`str`): The serialised policy contents

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the user mapping policy id is returned as JSON and can be accessed from
            the response.json attribute

        """
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("content", dynurl_config_data)

        response = self.client.post_json(USER_MAP_CDAS, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, _id=None, content=None):
        """
        Update a new user mapping policy file.

        Args:
            name (:obj:`str`): The name of the new policy.
            content (:obj:`str`): The new serialised policy contents

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        """
        data = DataObject()
        data.add_value("content", dynurl_config_data)
        endpoint = USER_MAP_CDAS + "/{}".format(_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self, _id=None):
        """
        Delete a user mapping policy file.

        Args:
            _id (:obj:`str`): The id of the policy to be removed

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = USER_MAP_CDAS + "/{}".format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, _id):
        """
        Get a rate limiting policy.

        Args:
            _id (:obj:`str`): The unique id of the policy to return.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the user mapping policy is returned as JSON and can be accessed from
            the response.json attribute

        """
        endpoint = USER_MAP_CDAS + "/{}".format(_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def get_template(self):
        """
        Get the tempalte user mapping policy file.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the template user mapping policy is returned as JSON and can be accessed from
            the response.json attribute

        """
        endpoint = "/isam/wga_templates/username_mapping_template"
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def list(self):
        """
        Get a list of the user mapping policy files.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the user mapping policy file names are returned as JSON and can be accessed from
            the response.json attribute

        """
        response = self.client.get_json(USER_MAP_CDAS)
        response.success = response.status_code == 200
        return response
