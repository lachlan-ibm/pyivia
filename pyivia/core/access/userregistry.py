"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


USER_REGISTRY = "/mga/user_registry"

logger = logging.getLogger(__name__)


class UserRegistry(object):

    def __init__(self, base_url, username, password):
        super(UserRegistry, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def update_user_password(self, username, password=None):
        '''
        Update the password for a user in the AAC runtime server user registry.

        Args:
            username (:obj:`str`): User to update password for.
            password (:obj:`str`): New password for user.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("password", password)

        endpoint = "%s/users/%s/v1" % (USER_REGISTRY, username)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


class UserRegistry10020(UserRegistry):

    def __init__(self, base_url, username, password):
        super(UserRegistry10020, self).__init__(base_url, username, password)
        self.client = RESTClient(base_url, username, password)


    def create_group(self, _id=None, users=None):
        '''
        Create a new AAC Runtime group and populate it with users.

        Args:
            _id (:obj:`str`): A unique name for the new group.
            users (:obj:`list` of :obj:`str`, optional): List of users to add to group.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created group is returned as JSON and can be accessed from the
            response.JSON attribute.

        '''
        data = DataObject()
        data.add_value_string("id", _id)
        data.add_value("users", users)

        endpoint = USER_REGISTRY + "/groups/v1"
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_group(self, group_id):
        '''
        Delete a group from the AAC runtime user registry.

        Args:
            group_id (:obj:`str`): The id of the group to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "{}/groups/{}/v1".format(USER_REGISTRY, group_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def create_user(self, user_id, password=None, groups=None):
        '''
        Create a new AAC Runtime user.

        Args:
            _id (:obj:`str`): The unique id of the new user.
            password (:obj:`str`): Password for the user.
            groups (:obj:`list` of :obj:`str`): List of groups to add user to.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created user is returned as JSON and can be accessed from the
            response.JSON attribute

        '''
        data = DataObject()
        data.add_value_string("id", user_id)
        data.add_value_string("password", password)
        data.add_value("groups", groups)

        endpoint = USER_REGISTRY + "/users/v1"
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_user(self, user_id):
        '''
        Delete a user from the AAC runtime user registry.

        Args:
            user_id (:obj:`str`): The id of the user to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "{}/users/{}/v1".format(USER_REGISTRY, user_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def add_user_to_group(self, user_id=None, group=None):
        '''
        Add a AAC Runtime registry user to an existing group.

        Args:
            user_id (:obj:`str`): The id of the user being modified.
            group (:obj:`str`): The id of the group the user is being added to.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the modified group is returned as JSON and can be accessed from the
            response.JSON attribute.

        '''
        data = DataObject()
        data.add_value_string("id", group)

        endpoint = "{}/users/{}/groups/v1".format(USER_REGISTRY, user_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def remove_user_from_group(self, user_id=None, group=None):
        '''
        Remove a AAC Registry user from a group.

        Args:
            user_id (:obj:`str`): The id of the user being modified.
            group_id (:obj:`str`): The id of the group the user is being removed from.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("id", group)

        endpoint = "{}/users/{}/groups/v1".format(USER_REGISTRY, user_id)
        response = self.client.delete_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def get_user(self, user_id):
        '''
        Get a user from the AAC runtime user registry.

        Args:
            user_id (:obj:`str`): The id of the user.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the user's properties is returned as JSON and can be accessed from the
            response.JSON attribute.

        '''
        endpoint = "{}/users/{}/v1".format(USER_REGISTRY, user_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_group(self, group_id):
        '''
        Get a group from the AAC runtime user registry.

        Args:
            group_id (:obj:`str`): The id of the group.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the user's properties is returned as JSON and can be accessed from the
            response.JSON attribute.

        '''
        endpoint = "{}/groups/{}/v1".format(USER_REGISTRY, group_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_groups(self):
        '''
        List the groups in the AAC runtime user registry.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the list of users is returned as JSON and can be accessed from the
            response.JSON attribute.

        '''
        endpoint = "{}/groups/v1".format(USER_REGISTRY)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_users(self):
        '''
        List the users in the AAC runtime user registry.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the list of groups is returned as JSON and can be accessed from the
            response.JSON attribute.

        '''
        endpoint = "{}/users/v1".format(USER_REGISTRY)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response
