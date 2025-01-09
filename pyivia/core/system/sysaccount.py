""""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


SYSACCOUNT = '/sysaccount'
SYSACCOUNT_USERS = SYSACCOUNT + '/users'
SYSACCOUNT_GROUPS = SYSACCOUNT + '/groups'

logger = logging.getLogger(__name__)


class SysAccount(object):

    def __init__(self, base_url, username, password):
        super(SysAccount, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_users(self):
        """
        Get a list of all the current management interface user accounts.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the user accounts are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = SYSACCOUNT_USERS + '/v1'
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_user(self, user):
        """
        Get details of a particular user

        Args:
            user (:obj:`str`): The name of the user to list details for.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the user's details are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = SYSACCOUNT_USERS + '/' + user + '/v1'
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def update_user(self, user, password=None):
        """
        Update the user's password

        Args:
            user (:obj:`str`): The name of the user to change the password for.
            password (:obj:`str`): The new password for the user. This can contain any ASCII characters.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        data.add_value_string('password', password)

        endpoint = SYSACCOUNT_USERS + '/' + user + '/v1'
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def create_user(self, user=None, password=None, groups=[]):
        """
        Create a new management interface user

        Args:
            user (:obj:`str`): The name of the new user. The name can contain any ASCII characters but leading 
                            and trailing white space will be trimmed.
            password (:obj:`str`): The password for the new user. This can contain any ASCII characters.
            groups (:obj:`list` of :obj:`str`): A list of groups the new user will belong to.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the new user is returned as JSON and can be accessed from
            the response.json attribute
        """
        data = DataObject()
        data.add_value_string('id', user)
        data.add_value_string('password', password)
        if groups:
            groups_data = DataObject()
            for group in groups:
                groups_data.add_value('id', group)
            data.add_value_not_empty('groups', groups_data.data)
        endpoint = SYSACCOUNT_USERS + '/v1'
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_user(self, user):
        """
        Delete a user from the management interface

        Args:
            user (:obj:`str`): The name of the user to delete.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        endpoint = SYSACCOUNT_USERS + '/' + user + '/v1'
        response = self.client.delete_json(endpoint)

        response.success = response.status_code == 204

        return response


    def get_groups(self):
        """
        Get a list of the management interface groups

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the list of groups is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = SYSACCOUNT_GROUPS + '/v1'
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_group(self, group=None):
        """
        Get the details of a group

        Args:
            group (:obj:`str`): The name of the group to list details for.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the groups details are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = SYSACCOUNT_GROUPS + '/groups/{}/v1'.format(group)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def add_user(self, group=None, user=None):
        """
        Add a user to a group

        Args:
            group (:obj:`str`): The name of the group the user will be added to.
            user (:obj:`str`): The name of the user to be added to the group.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the updated group is returned as JSON and can be accessed from
            the response.json attribute
        """
        data = DataObject()
        data.add_value_string("id", group)
        endpoint = SYSACCOUNT_GROUPS + '/{}/groups/v1'.format(user)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def remove_user(self, group=None, user=None):
        """
        Remove a user from a group.

        Args:
            group (:obj:`str`): The name of the group the user will be removed from.
            user (:obj:`str`): The name of the user to be removed from the group.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        endpoint = SYSACCOUNT_GROUPS + '/users/{}/groups/{}/v1'.format(user, group)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def create_group(self, group=None):
        """
        Create a new management interface group

        Args:
            group (:obj:`str`): The name of the group the user will be added to. The name can contain any ASCII 
                            characters but leading and trailing white space will be trimmed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the group is returned as JSON and can be accessed from
            the response.json attribute
        """
        data = DataObject()
        data.add_value_string("id", group)
        endpoint = SYSACCOUNT_GROUPS +'/v1'
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_group(self, group=None):
        """
        Delete a group from the management interface

        Args:
            group (:obj:`str`): The name of the group to delete.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        endpoint = SYSACCOUNT_GROUPS + '/{}/v1'.format(group)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def update_admin_password(self, old_password=None, password=None):
        """
        Update the password for the current user account.

        Args:
            old_password (:obj:`str`): The current password for the user. 
            password (:obj:`str`): The new password for the user. This can contain any ASCII characters.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        endpoint = SYSACCOUNT + '/self/v1'
        data = DataObject()
        data.add_value_string('old_password', old_password)
        data.add_value_string('password', password)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response
