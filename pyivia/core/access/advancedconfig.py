"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


OVERRIDE_CONFIGS = "/iam/access/v8/override-configs"

logger = logging.getLogger(__name__)


class AdvancedConfig(object):

    def __init__(self, base_url, username, password):
        super(AdvancedConfig, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def list_properties(self, sort_by=None, count=None, start=None, filter=None):
        '''
        Get a list of all the advanced configuration parameters

        Args:
            sort_by (:obj:`str`, optional): Attribute to sort results by.
            count (:obj:`str`, optional): Maximum number of results to fetch.
            start (:obj:`str`, optional): Pagination offset of returned results.
            filter (:obj:`str`): Attribute to filter results by

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the Advanced Configuration Properties are returned as JSON and can be accessed from
            the response.json attribute

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("count", count)
        parameters.add_value_string("start", start)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(OVERRIDE_CONFIGS, parameters.data)
        response.success = response.status_code == 200

        return response


    def update_property(self, id, value=None, sensitive=False):
        '''
        Update an AAC advanced configuration property.

        Args:
            id (:obj:`str`): The id of the property to be updated.
            value (:obj:`str`): The new value of the configuration property.
            sensitive (`bool`, optional): Flag to indicate if value should be 
                                          obfuscated from logs/audit records. Default is ``false``.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("value", value)
        data.add_value_boolean("sensitive", sensitive)

        endpoint = "%s/%s" % (OVERRIDE_CONFIGS, id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response