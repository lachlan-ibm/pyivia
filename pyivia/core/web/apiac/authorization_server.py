"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

API_AUTHZ_SERVER = "/isam/authzserver/"

class AuthorizationServer(object):

    def __init__(self, base_url, username, password):
        super(AuthorizationServer, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_server(self, inst_name, hostname=None, auth_port=None, admin_port=None, domain=None, admin_id=None, 
               admin_pwd=None, addresses=[], ssl=None, ssl_port=None, keyfile=None, keyfile_label=None):
        '''
        Create new API authorization server.

        Args:
            inst_name (:obj:`str`): Name of the instance to be created.
            hostname (:obj:`str`): The host name of the local host. This name is used when constructing the 
                                   authorization server name.
            auth_port (`int`): The port on which authorization requests will be received.
            admin_port (`int`): The port on which Verify Identity Access authorization server administration requests will be received.
            domain (:obj:`str`): The Verify Identity Access authorization server domain.
            admin_id (:obj:`str`, optional): The Verify Identity Access authorization server's administrator name. This parameter is optional 
                                             and will be set to "sec_master" if not specified.
            admin_pwd (:obj:`str`): The Verify Identity Access authorization server's administrator password.
            addresses (:obj:`list` of :obj:`str`): A list of local addresses on which the authorization server will 
                                                   listen for requests.
            ssl (:obj:`str`): Whether or not to enable SSL between the Verify Identity Access authorization server and 
                                                   the LDAP server. "yes" | "no".
            ssl_port (`int`): The SSL port on which the LDAP server will be contacted.
            keyfile (:obj:`str`): The name of the keyfile that will be used when communicating with the LDAP server 
                                  over SSL.
            keyfile_label (:obj:`str`): The label of the certificate within the keyfile to use.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("inst_name", inst_name)
        data.add_value_string("hostname", hostname)
        data.add_value_string("authport",auth_port)
        data.add_value_string("adminport", admin_port)
        data.add_value_string("domain", domain)
        data.add_value_string("admin_id", admin_id)
        data.add_value_string("admin_pwd", admin_pwd)
        data.add_value_not_empty("addresses", addresses)
        data.add_value_string("ssl", ssl)
        data.add_value_string("ssl_port", ssl_port)
        data.add_value_string("keyfile", keyfile)
        data.add_value_string("keyfile_label", keyfile_label)

        endpoint = API_AUTHZ_SERVER + "v1"
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def update_server(self, inst_name, admin_id=None, admin_pwd=None, operation='renew'):
        '''
        Update an API authorization server. This can be used to update the certificate used to communicate with
        the Verify Identity Access authorization server.
        
        Args:
            inst_name (:obj:`str`): Name of the authorization server to update.
            admin_id (:obj:`str`): The Verify Identity Access authorization server's administrator name.
            admin_pwd (:obj:`str`): Secret to authenticate as ``admin_id``.
            operation (:obj:`str`): A flag that is used to indicate the operation to perform. This value is set to 
                                    "renew" for the renew operation.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("admin_id", admin_id)
        data.add_value_string("admin_pwd", admin_pwd)
        data.add_value_string("operation", operation)

        endpoint = API_AUTHZ_SERVER + '{}/v1'.format(inst_name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete_server(self, inst_name, admin_id=None, admin_pwd=None, operation='unconfigure', force=None):
        """
        Delete a configured API Authorization Server.

        Args:
            inst_name (:obj:`str`): Name of the authorization server to update.
            admin_id (:obj:`str`): The Verify Identity Access authorization server's administrator name.
            admin_pwd (:obj:`str`): Secret to authenticate as ``admin_id``.
            operation (:obj:`str`): A flag that is used to indicate the operation to perform. Accepted value is 
                                    "unconfigure".
            force (:obj:`str`): Whether or not to force the unconfiguration of the instance in the event the policy 
                                server is unreachable. "yes" | "no"

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = API_AUTHZ_SERVER + "{}/v1".format(inst_name)
        data = DataObject()
        data.add_value_string("admin_id", admin_id)
        data.add_value_string("admin_pwd", admin_pwd)
        data.add_value_string("operation", operation)
        data.add_value_string("force", force)
        response = self.client.delete_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def list_servers(self):
        """
        Get a list of all the configured API Authorization Servers.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful a list of the configured API Authorization Servers is returned as JSON
            and can be accessed from the ``response.json`` property.

        """
        endpoint = API_AUTHZ_SERVER + "/v1"
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def add_configuration_stanza_entry(self, instance, stanza=None, entries=[]):
        """
        Add an entry to the configuration properties file of an API Authorization Server.

        Args:
            instance (:obj:`str`): The API Authorization server instance to modify.
            stanza (:obj:`str`): The stanza to modify.
            entries (:obj:`list` of :obj:`dict`): List of entries to add to the stanza. Dictionary is in the
                                                  format::

                                                            [
                                                                {"entryName": "value"},
                                                                {"anotherEntryName": "theValue"}
                                                            ]

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = API_AUTHZ_SERVER + "{}/configuration/stanza/{}/entry_name/v1".format(instance, stanza)
        data = DataObject()
        data.add_value_not_empty("entries", entries)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_configuration_stanza_entry(self, instance, stanza=None, entry_id=None, value=None):
        """
        Remove an entry from a stanza properties file for an API Authorization Server.

        Args:
            instance (:obj:`str`): The API Authorization server instance to modify.
            stanza (:obj:`str`): The stanza to modify.
            entry_id (:obj:`str`): The entry to remove.
            value (:obj:`str`): The value of the configuration entry to remove.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = API_AUTHZ_SERVER + "{}/configuration/stanza/{}/entry_name/{}/value/{}/v1".format(instance, stanza,
                                                                                                   entry_id, value)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def update_configuration_stanza_entry(self, instance, stanza=None, entry_id=None, value=None):
        """
        Update an entry in a stanza properties file for an API Authorization Server.

        Args:
            instance (:obj:`str`): The API Authorization server instance to modify.
            stanza (:obj:`str`): The stanza to modify.
            entry_id (:obj:`str`): The entry to be updated.
            value (:obj:`str`): The new value of the configuration entry.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = API_AUTHZ_SERVER + "{}/configuration/stanza/{}/entry_name/{}/v1".format(instance, stanza,
                                                                                            entry_id)
        data = DataObject()
        data.add_value_string("value", value)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response

    def get_configuration_stanza_entry(self, instance, stanza=None, entry_id=None):
        """
        Get the value of an entry in a stanza properties file for an API Authorization Server.

        Args:
            instance (:obj:`str`): The API Authorization server instance to return.
            stanza (:obj:`str`): The stanza to get.
            entry_id (:obj:`str`): The entry to get.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful then the entry value is returned as JSON and is available in the 
            ``response.json`` property.

        """
        endpoint = API_AUTHZ_SERVER + "{}/configuration/stanza/{}/entry_name/{}/v1".format(instance, stanza, entry_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def add_configuration_stanza(self, instance, stanza=None):
        """
        Add a stanza to the properties file for an API Authorization Server.

        Args:
            instance (:obj:`str`): The API Authorization server instance to modify.
            stanza (:obj:`str`): The stanza to add.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = API_AUTHZ_SERVER + "{}/configuration/stanza/{}/v1".format(instance, stanza)
        response = self.client.post_json(endpoint)
        response.success = response.status_code == 200

        return response

    def delete_configuration_stanza(self, instance, stanza=None):
        """
        Delete a stanza from the properties file for an API Authorization Server.

        Args:
            instance (:obj:`str`): The API Authorization server instance to modify.
            stanza (:obj:`str`): The stanza to remove.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = API_AUTHZ_SERVER + "{}/configuration/stanza/{}/v1".format(instance, stanza)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def list_configuration_stanza(self, instance):
        """
        Get a list of stanza's from the properties file for an API Authorization Server.

        Args:
            instance (:obj:`str`): The API Authorization server instance to return.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful then the list of stanza are returned as JSON and is available in the 
            ``response.json`` property.

        """
        endpoint = API_AUTHZ_SERVER + "{}/configuration/stanza".format(instance)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response
