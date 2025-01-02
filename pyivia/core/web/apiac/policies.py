"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

POLICY = "/wga/apiac/policy"

class Policies(object):

    def __init__(self, base_url, username, password):
        super(Policies, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, groups=[], attributes=[]):
        '''
        Create a new API Access Control policy.

        Args:
            name (:obj:`str`): name of new policy to be created.
            groups (:obj:`list` of :obj:`str`): The groups referenced by this policy.
            attributes (:obj:`list` of :obj:`str`): The attribute matches referenced by this policy.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created obligation can be accessed from the
            response.id_from_location attribute

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_not_empty("group", groups)
        data.add_value_not_empty("attributes", attributes)

        response = self.client.post_json(POLICY, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, name, groups=[], attributes=[]):
        '''
        Update a API Access Control policy.

        Args:
            name (:obj:`str`): Name of the API Access Control policy to be updated.
            groups (:obj:`list` of :obj:`str`): The groups referenced by this policy.
            attributes (:obj:`list` of :obj:`str`): The attribute matches referenced by this policy.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_not_empty("groups", groups)
        data.add_value_not_empty("attributes", attributes)

        endpoint = POLICY + "/{}".format(name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def get(self, name=None):
        '''
        Get an API Access Control policy.

        Args:
            name (:obj:`str`): Name of policy to be returned.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the policy is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = POLICY + "/{}".format(name)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def delete(self, name=None):
        '''
        Delete an API Access Control policy.

        Args:
            name (:obj:`str`): Name of policy to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = POLICY + "/{}".format(name)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        List all of the configured API Access Control policies.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        response = self.client.get_json(POLICY)
        response.success = response.status_code == 200

        return response
