""""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


MANAGEMENT_AUTHORIZATION = "/authorization"
MANAGEMENT_AUTHORIZATION_ROLES = MANAGEMENT_AUTHORIZATION + "/roles"
MANAGEMENT_AUTHORIZATION_FEATURES = MANAGEMENT_AUTHORIZATION + "/features"

logger = logging.getLogger(__name__)


class ManagementAuthorization(object):

    def __init__(self, base_url, username, password):
        super(ManagementAuthorization, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def enable(self, enforce=False):
        """
        Enable role based authorization.

        Args:
            enforce (`bool`): Is the authorization policy enabled and enforcing? 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        data.add_value_boolean("enforcing", enforce)
        endpoint = MANAGEMENT_AUTHORIZATION + '/config/v1'
        response = self.client.put_json(endpoint, data.data)
        response.success = True if response.status_code == 200 \
                and response.json \
                and response.json.get('enforcing') == enforce \
                    else False

        return response


    def create_role(self, name=None, users=None, groups=None, features=None):
        """
        Create a new management authorization role

        Args:
            name (:obj:`str`): The name of the authorization role.
            users (:obj:`list` of :obj:`dict`): The users who are included this role.
            groups (:obj:`list` of :obj:`dict`): The groups whose members are included in this role.
            features (:obj:`list` of :obj:`dict`): An array of features and the associated permission.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the created role is returned as JSON and can be accessed from
            the response.json attribute
        """
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_not_empty("users", users)
        data.add_value_not_empty("groups", groups)
        data.add_value_not_empty("features", features)

        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + '/v1'
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def update_role(self, name=None, users=None, groups=None, features=None):
        """
        Update a management authorization role

        Args:
            name (:obj:`str`): The name of the authorization role.
            users (:obj:`list` of :obj:`dict`): The users who are included this role.
            groups (:obj:`list` of :obj:`dict`): The groups whose members are included in this role.
            features (:obj:list` of :obj:`dict`): An array of features and the associated permission. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the updated management authorization role is returned as JSON and can be accessed from
            the response.json attribute
        """
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_not_empty("users", users)
        data.add_value_not_empty("groups", groups)
        data.add_value_not_empty("features", features)

        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + '/{}/v1'.format(name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def delete_role(self, role=None):
        """
        Delete a management authorization role.

        Args:
            role (:obj:`str`): The name of the authorization role.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + "/{}/v1".format(role)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def get_role(self, role=None):
        """
        Get a management authorization role.

        Args:
            role (:obj:`str`): The name of the authorization role.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the management authorization role is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + "/{}/v1".format(role)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_roles(self):
        """
        Get a list of the current management authorization roles.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the list of roles are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + '/v1'
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_features(self):
        """
        Get a list of the authorization features

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the list of management authorization roles are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = MANAGEMENT_AUTHORIZATION_FEATURES + '/v1'
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_features_for_user(self, user=None):
        """
        Get a list of the permitted features for a user.

        Args:
            user (:obj:`str`): The username to get the authorization features for.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful list of features is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = MANAGEMENT_AUTHORIZATION_FEATURES + '/users/{}/v1'.format(user)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        
        return response

    def get_groups_for_role(self, role=None):
        """
        Get a list of groups for a given role.

        Args:
            role (:obj:`str`): The name of the authorization role.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the list of groups is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + '/{}/groups/v1'.format(role)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_users_for_role(self, role=None):
        """
        Get a list of users for a given role.

        Args:
            role (:obj:`str`): The name of the authorization role.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the list of users is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + '/{}/users/v1'.format(role)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response
