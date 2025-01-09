"""
@copyright: IBM
"""

import logging
import uuid

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

ALIAS_SVC = "/iam/access/v8/alias_service"
ALIAS_SETTINGS = "/iam/access/v8/alias_settings"

logger = logging.getLogger(__name__)

class AliasService(object):

    def __init__(self, base_url, username, password):
        super(AliasService, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_alias_association(self, username=None, federation_id=None, 
            type=None, aliases=[]):
        '''
        Create a new SAML alias service association.

        Args:
            username (:obj:`str`): The user to associate aliases with.
            federation_id (:obj:`str`): The federation. To specify a partner as well as a federation, include the partner ID after the federation ID, separated by a pipe: federation_id|partner_id
            type (:obj:`str`, optional): The type of the aliases. Valid values are "self", "partner", or "old". Defaults to "self".
            aliases (:obj:`list` of :obj:`str`): An array of aliases to associate with the user.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created alias association can be accessed from the
            response.id_from_location attribute
        '''
        data = DataObject()
        data.add_value_string("username", username)
        data.add_value_string("federation_id", federation_id)
        data.add_value_string("type", type)
        data.add_value_not_empty("aliases", aliases)

        response = self.client.post_json(ALIAS_SVC, data.data)
        response.success = response.status_code == 201
        return response

    def update_alias_association(self, id, username=None, federation_id=None, type=None, aliases=[]):
        '''
        Update an existing SAML alias service association.

        Args:
            id (:obj:`str`): The Verify Identity Access assigned id of the alias.
            username (:obj:`str`): The user to associate aliases with.
            federation_id (:obj:`str`): The federation. To specify a partner as well as a federation, include the partner ID after the federation ID, separated by a pipe: federation_id|partner_id
            type (:obj:`str`, optional): The type of the aliases. Valid values are "self", "partner", or "old". Defaults to "self".
            aliases (:obj:`list` of :obj:`str`): An array of aliases to associate with the user.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("username", username)
        data.add_value_string("federation_id", federation_id)
        data.add_value_string("type", type)
        data.add_value_not_empty("aliases", aliases)

        endpoint = ALIAS_SVC + '/{}'.format(id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204
        return response


    def list_alias_associations(self):
        '''
        Get a list of existing SAML alias service associations.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the aliases is returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = self.client.get_json(ALIAS_SVC)
        response.success = response.status_code == 200
        return response


    def delete_alias_association(self, id):
        '''
        Delete an existing SAML alias service association.

        Args:
            id (:obj:`str`): The Verify Identity Access assigned id of the alias.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the aliases is returned as JSON and can be accessed from
            the response.json attribute        
        '''
        endpoint = ALIAS_SVC + '/{}'.format(id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204
        return response

    def get_alias_settings(self):
        '''
        Get the current alias service settings

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the alias service settings are returned as JSON and can be accessed from
            the response.json attribute  

        '''
        response = self.client.get_json(ALIAS_SETTINGS)
        response.success = response.status_code == 200
        return response

    def update_alias_settings(self, db_type=None, ldap_connection=None, ldap_base_dn=None):
        '''
        Update the current alias service settings.
        
        Args:
            db_type: (:obj:`str`): The alias database type, JDBC or LDAP.
            ldap_connection (:obj:`str`): The LDAP server connection name.
            ldap_base_dn (:obj:`str`): The baseDN to search for the user entry.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("aliasDbType", db_type)
        ldap = DataObject()
        ldap.add_value_string("aliasLDAPConnection", ldap_connection)
        ldap.add_value_string("aliasLDAPBaseDN", ldap_base_dn)
        data.add_value_not_empty("properties", ldap.data)
        
        response = self.client.put_json(ALIAS_SETTINGS, data.data)
        response.success = response.status_code == 204
        return response
