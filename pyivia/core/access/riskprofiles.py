"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


RISK_PROFILES = "/iam/access/v8/risk/profiles"

logger = logging.getLogger(__name__)


class RiskProfiles(object):

    def __init__(self, base_url, username, password):
        super(RiskProfiles, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_profile(self, description=None, name=None, active=None, attributes=None, predefined=False):
        '''
        Create a risk profile.

        Args:
            description (:obj:`str`): A description associated with the risk profile.
            name (:obj:`str`): A unique name of the risk profile.
            active (bool): Indicate if this is the active risk profile.
            attributes (:obj:`list` of :obj:`dict`):Array of attributes comprising this risk profile and the weight 
                                                value of each attribute which is used in determining the risk score.
                                                eg::

                                                    [
                                                        {"weight":50,
                                                         "attributeID":"28"
                                                        },
                                                        {"weight":10,
                                                         "attributeID":"34"
                                                        }
                                                    ]

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created risk profile can be accessed from the 
            response.id_from_location attribute.

        '''
        data = DataObject()
        data.add_value_string("description", description)
        data.add_value_string("name", name)
        data.add_value("active", active)
        data.add_value("attributes", attributes)
        data.add_value("predefined", predefined)

        response = self.client.post_json(RISK_PROFILES, data.data)
        response.success = response.status_code == 201

        return response


    def update_profile(self, _id, description=None, name=None, active=None, attributes=None, predefined=False):
        '''
        Update an existing risk profile.

        Args:
            _id (:obj:`str`): The id of the risk profile to be updated.
            description (:obj:`str`): A description associated with the risk profile.
            name (:obj:`str`): A unique name of the risk profile.
            active (bool): Indicate if this is the active risk profile.
            attributes (:obj:`list` of :obj:`dict`):Array of attributes comprising this risk profile and the weight 
                                                value of each attribute which is used in determining the risk score.
                                                eg::

                                                    [
                                                        {"weight":50,
                                                         "attributeID":"28"
                                                        },
                                                        {"weight":10,
                                                         "attributeID":"34"
                                                        }
                                                    ]

            predefined (`bool`, optional): Is this risk profile pre-defined by Verify Identity Access.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("description", description)
        data.add_value_string("name", name)
        data.add_value_boolean("active", active)
        data.add_value_not_empty("attributes", attributes)
        data.add_value_boolean("predefined", predefined)


        response = self.client.post_json(RISK_PROFILES, data.data)
        response.success = response.status_code == 204

        return response


    def list_profiles(self):
        '''
        List all of the configured risk profiles.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the risk profiles are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        response = self.client.get_json(RISK_PROFILES)
        response.success = response.status_code == 200

        return response


    def get_profile(self, _id):
        '''
        Get the configuration of a specific risk profile

        Args:
            _id (:obj:`str`): The id of the risk profile to return.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the risk profiles are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = "{}/{}".format(RISK_PROFILES, _id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def delete_profile(self, _id):
        '''
        Delete an existing risk profile.

        Args:
            _id (:obj:`str`): The id of the risk profile to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "{}/{}".format(RISK_PROFILES, _id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 204

        return response
