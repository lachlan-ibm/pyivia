"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

SCHEMA_ISAM_USER = "urn:ietf:params:scim:schemas:extension:isam:1.0:User"
SCIM_CONFIGURATION = "/mga/scim/configuration"
SCIM_CONFIGURATION_GENERAL = "/mga/scim/configuration/general"

logger = logging.getLogger(__name__)


class SCIMConfig(object):

    def __init__(self, base_url, username, password):
        super(SCIMConfig, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_config(self):
        '''
        Get the current SCIM configuration profile.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the SCIM profile is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        response = self.client.get_json(SCIM_CONFIGURATION)
        response.success = response.status_code == 200

        return response


    def get_schema(self, schema_name):
        '''
        Get the current SCIM configuration for a specific schema.

        Args:
            schema_name (:obj:`str`): The name of the SCIM schema to fetch configuration for.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the SCIM schema profile is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = "%s/%s" % (SCIM_CONFIGURATION,schema_name)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def update(self, data):
        '''
        Update the SCIM configuration profile. This method could be better.
        '''
        response = self.client.put_json(SCIM_CONFIGURATION, data)
        response.success = response.status_code == 200

        return response


    def update_schema(self, schema_name, data):
        '''
        Update the configuration profile of a SCIM schema.

        Args:
            schema_name (:obj:`str`): The name of the SCIM schema to update.
            data (:obj:`dict`): The updated configuration profile.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = "%s/%s" % (SCIM_CONFIGURATION,schema_name)

        response = self.client.put_json(endpoint, data)
        response.success = response.status_code == 200

        return response


    def update_general_config(self, admin_group="adminGroup", enable_header_authentication=True, enable_authz_filter=True,
            max_user_responses=None, attribute_modes=[]):
        '''
        Update the general configuration settings of the SCIM profile.

        Args:
            admin_group (:obj:`str`, optional): The name of the group used to identify SCIM admin users. 
                                                Default is "adminGroup".
            enable_header_authentication (bool, optional): Whether or not SCIM header authentication is enabled. 
                                                Default is ``true``.
            enable_authz_filter (bool, optional): Whether or not the authorization filter is enabled.
            max_user_response (int, optional): The maximum number of entries that can be returned from a single call to the /User endpoint.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("admin_group", admin_group)
        data.add_value_string("enable_header_authentication", enable_header_authentication)
        data.add_value_string("enable_authz_filter", enable_authz_filter)
        data.add_value("max_user_responses", max_user_responses)
        data.add_value_not_empty("attribute_modes", attribute_modes)

        response = self.client.put_json(SCIM_CONFIGURATION_GENERAL, data.data)
        response.success = response.status_code == 200

        return response

    def get_general_config(self):
        '''
        Get the general SCIM configuration settings:

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the general SCIM properties are returned as JSON and can be accessed from
            the response.json attribute.
        '''
        response = self.client.get_json(SCIM_CONFIGURATION_GENERAL)
        response.success = response.status_code == 200

        return response


    def update_attribute_mode(self, schema_name, scim_attribute, scim_subattribute=None, mode=None):
        '''
        Update the attribute model used for SCIM attribute mapping.

        Args:
            schema_name (:obj:`str`): Name of ths SCIM schema to update attribute modes for.
            scim_attribute (:obj:`str`): Name of the SCIM attribute to update mode for.
            scim_subattribute (:obj:`str`, optional): If the SCIM attribute is a multi-valued attribute this is the second 
                                level attribute name.
            mode (:obj:`str`): New mode for the SCIM attribute. Valid values are: "readonly", "writeonly", "readwrite", 
                                "adminwrite" or "immutable".

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

        '''

        data = DataObject()
        data.add_value_string("mode", mode)

        endpoint = "%s/attribute_modes/%s/%s" % (
            SCIM_CONFIGURATION_GENERAL, schema_name, scim_attribute)
        if scim_subattribute:
            endpoint = "%s/%s" % (endpoint, scim_subattribute)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response

    def update_isam_user(self, ldap_connection=None, isam_domain=None, update_native_users=None):
        '''
        Update SCIM user mappings for basic and full Verify Identity Access users.

        Args:
            ldap_connection (:obj:`str`): The name of the ldap server connection to the Verify Identity Access user registry.
            isam_domain (:obj:`str`): The name of the Verify Identity Access domain.
            update_native_users (bool): Whether the UID of native users should be updated with the Verify Identity Access user 
                                        identity when an Verify Identity Access user is created.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the updated SCIM user configuration is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        data = DataObject()
        data.add_value_string("ldap_connection", ldap_connection)
        data.add_value_string("isam_domain", isam_domain)
        data.add_value("update_native_users", update_native_users)

        endpoint = ("%s/%s" % (SCIM_CONFIGURATION, SCHEMA_ISAM_USER))

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response
        
class SCIMConfig9050(SCIMConfig):
    def __init__(self, base_url, username, password):
        super(SCIMConfig, self).__init__()
        self.client = RESTClient(base_url, username, password)
        
    def update_isam_user(self, ldap_connection=None, isam_domain=None, update_native_users=None,
            connection_type=None):
        '''
        Update SCIM user mappings for basic and full Verify Identity Access users.

        Args:
            ldap_connection (:obj:`str`): The name of the ldap server connection to the Verify Identity Access user registry.
            isam_domain (:obj:`str`): The name of the Verify Identity Access domain.
            connection_type (:obj:`str`): Indicates the type of ldap server connection. Valid values are "ldap" and
                                        "isamruntime".
            update_native_users (bool): Whether the UID of native users should be updated with the Verify Identity Access user 
                                        identity when an Verify Identity Access user is created.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the updated SCIM user configuration is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        data = DataObject()
        data.add_value_string("ldap_connection", ldap_connection)
        data.add_value_string("isam_domain", isam_domain)
        data.add_value_string("connection_type", connection_type)
        data.add_value("update_native_users", update_native_users)

        endpoint = ("%s/%s" % (SCIM_CONFIGURATION, SCHEMA_ISAM_USER))

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200
        return response
