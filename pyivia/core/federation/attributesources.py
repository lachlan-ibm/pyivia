"""
@copyright: IBM
"""

import logging
import uuid

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

ATTRIBUTE_SOURCES = "/mga/attribute_sources/"

logger = logging.getLogger(__name__)

class AttributeSources(object):

    def __init__(self, base_url, username, password):
        super(AttributeSources, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_attribute_source(self, attribute_name=None, attribute_type=None, attribute_value=True, properties=None):
        """
        Create a new attribute source

        Args:
            attribute_name (:obj:`str`): The name of the attribute.
            attribute_type (:obj:`str`): The type of the attribute source. Valid types are: credential, value, ldap.
            attribute_value (:obj:`str`): The value of the source attribute.
            properties (:obj:`list` of :obj:`dict`): The properties associated with an attribute source.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created attribute source can be accessed from the
            response.id_from_location attribute

        """
        data = DataObject()
        data.add_value_string("name", attribute_name)
        data.add_value_string("type", attribute_type)
        data.add_value_string("value", attribute_value)
        data.add_value("properties", properties)

        response = self.client.post_json(ATTRIBUTE_SOURCES, data.data)
        response.success = response.status_code == 201
        return response


    def update_attribute_source(self, attribute_id, attribute_name=None, attribute_type=None, 
                                attribute_value=True, properties=None):
        """
        Update an existing attribute source

        Args:
            attribute_id (:obj:`str`): The verify identity access assigned id of the attribute.
            attribute_name (:obj:`str`): The updated name of the attribute.
            attribute_type (:obj:`str`): The type of the attribute source. Valid types are: credential, value, ldap.
            attribute_value (:obj:`str`): The value of the source attribute.
            properties (:obj:`list` of :obj:`str`): The properties associated with an attribute source.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created attribute source can be accessed from the
            response.id_from_location attribute

        """
        data = DataObject()
        data.add_value_string("name", attribute_name)
        data.add_value_string("type", attribute_type)
        data.add_value_string("value", attribute_value)
        data.add_value("properties", properties)

        endpoint = "%s/%s" % (ATTRIBUTE_SOURCES, attribute_id)
        response = self.client.post_json(ATTRIBUTE_SOURCES, data.data)
        response.success = response.status_code == 204
        return response


    def delete_attribute_source(self, attribute_name=None):
        """
        Delete a configured attribute source

        Args:
            attribute_name (:obj:`str`): The name of the attribute to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = "%s/%s" % (ATTRIBUTE_SOURCES, attribute_name)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204
        return response

    def get_attribute_source(self, attribute_name=None):
        """
        Get a configured attribute source

        Args:
            attribute_name (:obj:`str`): THe name of the attribute to get config for.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the attribute source is returned as JSON and can be accessed from
            the response.json attribute

        """
        endpoint = "%s/%s" % (ATTRIBUTE_SOURCES, attribute_name)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def list_attribute_sources(self):
        """
        Get a list of the configured attribute sources

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the attribute sources are returned as JSON and can be accessed from
            the response.json attribute

        """
        response = self.client.get_json(ATTRIBUTE_SOURCES)
        response.success = response.status_code == 200
        return response
