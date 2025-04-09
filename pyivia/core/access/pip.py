"""
@copyright: IBM
"""

import logging
import json

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


POLICY_INFO_POINT = "/iam/access/v8/pips"

logger = logging.getLogger(__name__)


class PIP(object):

    def __init__(self, base_url, username, password):
        super(PIP, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_pip(self, name=None, description=None, type=None, attributes=[], properties=[]):
        '''
        Create a new Policy Information Point.

        Args:
            name (:obj:`str`): A unique name for the policy information point. This name is used as the Issuer for custom attributes whose value is returned by this policy information point.
            description (:obj:`str`, optional): A description of the policy information point.
            type (:obj:`str`): The policy information point type for this policy information point. valid values are "Database", "FiberLink MaaS360", "JavaScript", "RESTful Web Service", "LDAP", and "QRadar User Behavior Analytics".
            attributes (:obj:`list` of :obj:`dict`): A list of custom attributes whose values are retrieved from select portions of the response from this policy information point.
            properties (:obj:`list` of :obj:`dict`): Configurable properties defining this policy information point. These entries are specific to the policy information point type.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created PIP can be accessed from the
            response.id_from_location attribute.

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("type", type)
        data.add_value_not_empty("attributes", attributes)
        data.add_value_not_empty("properties", properties)

        response = self.client.post_json(POLICY_INFO_POINT, data.data)
        response.success = response.status_code == 201
        return response


    def update_pip(self, pip_id, name=None, description=None, type=None, attributes=[], properties=[]):
        '''
        Update an existing Policy Information Point.

        Args:
            pip_id (:obj:`str`): The Verify Identity Access assigned identifier of the PIP.
            name (:obj:`str`): A unique name for the policy information point. This name is used as the Issuer for custom attributes whose value is returned by this policy information point.
            description (:obj:`str`, optional): A description of the policy information point.
            type (:obj:`str`): The policy information point type for this policy information point. valid values are "Database", "FiberLink MaaS360", "JavaScript", "RESTful Web Service", "LDAP", and "QRadar User Behavior Analytics".
            attributes (:obj:`list` of :obj:`dict`): A list of custom attributes whose values are retrieved from select portions of the response from this policy information point.
            properties (:obj:`list` of :obj:`dict`): Configurable properties defining this policy information point. These entries are specific to the policy information point type.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("type", type)
        data.add_value_not_empty("attributes", attributes)
        data.add_value_not_empty("properties", properties)

        endpoint = "{}/{}".format(POLICY_INFO_POINT, pip_id)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204
        return response


    def get_pip(self, pip_id):
        '''
        Get the configuration for a specific PIP.

        Args:
            pip_id (:obj:`str`): The Verify Identity Access assigned identifier of the PIP.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the PIP configuration is returned as JSON and
            can be accessed via the response.json property. 

        '''
        endpoint = '{}/{}'.format(POLICY_INFO_POINT, pip_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_pips(self, sort_by=None, filter=None):
        '''
        Get a list of all the configured PIPs.

        Returns:
            obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the PIP configuration is returned as JSON and
            can be accessed via the response.json property.
        
        '''
        endpoint = POLICY_INFO_POINT
        if sort_by:
            endpoint += '?sortBy={}'.format(sort_by)
        if filter:
            if '?' in endpoint:
                endpoint += '&filter={}'.format(filter)
            else:
                endpoint += '?filter={}'.format(filter)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def delete_pip(self, pip_id):
        '''
        Delete a configured PIP.

        Args:
            pip_id (:obj:`str`): The Verify Identity Access assigned identifier of the pip.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.
            
        '''
        endpoint = '{}/{}'.format(POLICY_INFO_POINT, pip_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204
        return response
