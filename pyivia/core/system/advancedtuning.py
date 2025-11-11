""""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


ADVANCED_PARAMETERS = "/core/adv_params"

logger = logging.getLogger(__name__)


class AdvancedTuning(object):

    def __init__(self, base_url, username, password):
        super(AdvancedTuning, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_parameter(self, key=None, value=None, comment=None):
        """
        Create a new Advanced Tuning Parameter

        Args:
            key (:obj:`str`): The name of the advanced tuning parameter.
            value (:obj:`str`): The value of the advanced tuning parameter.
            comment (:obj:`str`, optional): A description for the advanced tuning parameter.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created mechanism can be acess from the 
                        response.id_from_location attribute
        """
        data = DataObject()
        data.add_value_string("key", key)
        data.add_value_string("value", value)
        data.add_value_string("comment", comment)
        data.add_value("_isNew", True)

        response = self.client.post_json(ADVANCED_PARAMETERS, data.data)
        response.success = response.status_code == 201

        return response

    def update_parameter(self, atp_id=None, key=None, value=None, comment=None):
        """
        Update an existing advanced tuning parameter

        Args:
            atp_id (:obj:`str`): Unique id of the advanced tuning parameter.
            key (:obj:`str`): The name of the advanced tuning parameter.
            value (:obj:`str`): The value of the advanced tuning parameter.
            comment (:obj:`str`, optional): A description for the advanced tuning parameter.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        data.add_value_string("key", key)
        data.add_value_string("value", value)
        data.add_value_string("comment", comment)
        endpoint = ADVANCED_PARAMETERS+"/"+str(atp_id)
        response = self.client.put_json(endpoint, data.data)

        response.success = response.status_code == 200

        return response

    def list_parameters(self):
        """

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the tuning parameters are returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(ADVANCED_PARAMETERS)
        response.success = response.status_code == 200

        if response.success and response.json:
            response.json = response.json.get("tuningParameters", [])

        return response

    def delete_parameter(self, atp_id=None):
        """
        Delete an Advanced Tuning Parameter.

        Args:
            atp_ip (:obj:`str`): Unique id of the advanced tuning parameter.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        endpoint = ADVANCED_PARAMETERS + "/{}".format(atp_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
