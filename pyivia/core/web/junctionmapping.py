""""
@copyright: IBM
"""

import logging
import urllib

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

JUNCTION_MAPPING = "/wga/jmt_config"

class JunctionMapping(object):

    def __init__(self, base_url, username, password):
        super(JunctionMapping, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, jmt_config_data=None):
        '''
        Create a WebSEAL Junction mapping rule.

        Args:
            name (:obj:`str`): The name of the junction mapping rule to be created
            jmt_config_data (:obj:`str`): contents of junction mapping table

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created junction mapping can be accessed from the
            response.id_from_location attribute
        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("jmt_config_data", jmt_config_data)

        response = self.client.post_json(JUNCTION_MAPPING, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, rule_id=None, jmt_config_data=None):
        '''
        Update a WebSEAL Junction mapping rule.

        Args:
            rule_id (:obj:`str`): The unique id of the junction mapping rule to be modified
            jmt_config_data (:obj:`str`): contents of junction mapping table

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        data = DataObject()
        data.add_value("jmt_config_data", jmt_config_data)
        endpoint = JUNCTION_MAPPING + "/{}".format(rule_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self, rule_id=None):
        '''
         Delete a WebSEAL Junction mapping rule.

        Args:
            rule_id (:obj:`str`): The unique id of the junction mapping rule to be deleted

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        endpoint = JUNCTION_MAPPING + "/{}".format(rule_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, rule_id):
        '''
        Get a WebSEAL Junction mapping rule.

        Args:
            rule_id (:obj:`str`): The unique id of the junction mapping rule to be returned

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the junction mapping rule is returned as JSON and can be accessed from
            the response.json attribute
        '''
        endpoint = JUNCTION_MAPPING + "/{}".format(rule_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_template(self):
        '''
        Get the JMT configuration file template

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the junction mapping rule template is returned as JSON and can be accessed from
            the response.json attribute
        '''
        endpoint = "/isam/wga_templates/jmt_template"
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        Get  a list of the configured WebSEAL Junction mapping rules.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the junction mapping rules are returned as JSON and can be accessed from
            the response.json attribute
        '''
        response = self.client.get_json(JUNCTION_MAPPING)
        response.success = response.status_code == 200

        return response
