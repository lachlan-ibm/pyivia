""""
@copyright: IBM
"""

import logging
import urllib

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

URL_MAPPING = "/wga/dynurl_config"

class URLMapping(object):

    def __init__(self, base_url, username, password):
        super(URLMapping, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, dynurl_config_data=None):
        """
        Create a new URL mapping policy

        Args:
            name (:obj:`str`): The name of the new URL mapping rule.
            dynurl_config_data (:obj:`str`): The serialized contents of the new policy file.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("dynurl_config_data", dynurl_config_data)

        response = self.client.post_json(URL_MAPPING, data.data)
        response.success = response.status_code == 200
        return response


    def update(self, rule_id=None, dynurl_config_data=None):
        """
        Update a URL mapping policy file with new contents

        Args:
            rule_id (:obj:`str`): The unique id of the new URL mapping rule.
            dynurl_config_data (:obj:`str`): The serialized contents of the new policy file.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        data = DataObject()
        data.add_value("dynurl_config_data", dynurl_config_data)
        endpoint = URL_MAPPING + "/{}".format(rule_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204
        return response


    def delete(self, rule_id=None):
        """
        Delete a URL mapping policy.

        Args:
            rule_id (:obj:`str`): The unique id of the URL mapping rule to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = URL_MAPPING + "/{}".format(rule_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, rule_id):
        """
        Get a URL mapping policy.

        Args:
            rule_id (:obj:`str`): The unique id of the policy to return.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the URL mapping policy is returned as JSON and can be accessed from
            the response.json attribute

        """
        endpoint = URL_MAPPING + "/{}".format(rule_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def get_template(self):
        """
        Get the template URL mapping policy.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the template URL mapping policy is returned as JSON and can be accessed from
            the response.json attribute

        """
        endpoint = "/isam/wga_templates/dynurl_template"
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def list(self):
        """
        Get a list of template URL mapping policy files.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the URL mapping policy files are returned as JSON and can be accessed from
            the response.json attribute

        """
        response = self.client.get_json(URL_MAPPING)
        response.success = response.status_code == 200
        return response
