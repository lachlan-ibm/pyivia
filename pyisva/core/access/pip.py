"""
@copyright: IBM
"""

import logging
import json

from pyisva.util.model import DataObject
from pyisva.util.restclient import RESTClient


POLICY_INFO_POINT = "/iam/access/v8/pips"

logger = logging.getLogger(__name__)


class PIP(object):

    def __init__(self, base_url, username, password):
        super(MappingRules, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_pip(self, name=None, description=None, type=None, attributes=[], properties=[]):
        '''
        Create a new Policy Information Point

        Args:
            name (:obj:`str`):
            description (:obj:`str`, optional): 
            type (:obj:`str`):
            attributes (:obj:`list` of :obj:`dict`):

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created pip can be acess from the
            response.id_from_location attribute        

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("type", type)
        data.add_value("attributes", attributes)
        data.add_value("properties", properties)

        response = self.client.post_json(POLICY_INFO_POINT, data.data)
        response.success = response.status_code == 201
        return response


    def update_pip(self, _id, name=None, description=None, type=None, attributes=[], properties=[]):
        '''
        Update an exisint Policy Information Point.

        Args:
            _id (:obj:`str`):
            name (:obj:`str`):
            description (:obj:`str`, optional): 
            type (:obj:`str`):
            attributes (:obj:`list` of :obj:`dict`):

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        '''
                data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("type", type)
        data.add_value("attributes", attributes)
        data.add_value("properties", properties)

        endpoint = POLICY_INFO_POINT + '/{}'.format(_id)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204
        return response


    def get_pip(self, _id):
        '''
        Get the configuration for a specific PIP.

        Args:
            _id (:obj:`str`): The Verify Access assigned identifier of the pip.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the pip configuration is returned as JSON and
            can be accessed via the response.json property. 

        '''
        endpoint = POLICY_INFO_POINT + '/{}'.format(_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_pips(self, sort_by=None, filter=None):
        '''
        Get a list of all the configured PIPs.

        Returns:
            obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the pip configuration is returned as JSON and
            can be accessed via the response.json property. 
        '''
        endpoint = POLICY_INFO_POINT
        if sort_by:
            endpoint += '?sortBy={}'.format(sort_by)
        if filter:
            if endpoint contains '?':
                endpoint += '&filter={}'.format(filter)
            else:
                endpoint += '?filter={}'.format(filter)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def delete_pip(self, _id):
        '''
        Delete a configured PIP.

        Args:
            _id (:obj:`str`): The Verify Access assigned identifier of the pip.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute
            
        '''
        endpoint = POLICY_INFO_POINT + '/{}'.format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204
        return response