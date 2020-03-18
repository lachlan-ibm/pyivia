""""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


MANAGEMENT_AUTHORIZATION = "/authorization"
MANAGEMENT_AUTHORIZATION_ROLES = MANAGEMENT_AUTHORIZATION + "/roles"
MANAGEMENT_AUTHORIZATION_FEATURES = MANAGEMENT_AUTHORIZATION + "/features"

logger = logging.getLogger(__name__)


class ManagementAuthorization(object):

    def __init__(self, base_url, username, password):
        super(ManagementAuthorization, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def enable(self, enforce=False):
        data = DataObject()
        data.add_value_boolean("enforcing", enforce)
        endpoint = MANAGEMENT_AUTHORIZATION + '/config/v1'
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response

    def update(self, enforce_config=False, roles=[]):
        auth_config = DataObject()
        auth_config.add_value_boolean("enforcing", enforce_config)

        auth_roles = DataObject()
        auth_roles.add_value_not_empty("roles", roles)

        data = DataObject()
        data.add_value("config", auth_config.data)
        data.add_value_not_empty("roles", auth_roles.data)
        endpoint = MANAGEMENT_AUTHORIZATION + '/v1'
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def get(self):
        endpoint = MANAGEMENT_AUTHORIZATION + '/v1'
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_role(self, name=None, users=None, groups=None, features=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_not_empty("users", users)
        data.add_value_not_empty("grpups", groups)
        data.add_value_not_empty("features", features)

        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + '/v1'
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def update_role(self, name=None, users=None, groups=None, features=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_not_empty("users", users)
        data.add_value_not_empty("grpups", groups)
        data.add_value_not_empty("features", features)

        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + '/{}/v1'.format(name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def delete_role(self, role=None):
        endpoint = MANAGEMENT_AUTHORIZATION_ROLES "/{}/v1".format(role)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def get_role(self, role=None):
        endpoint = MANAGEMENT_AUTHORIZATION_ROLES "/{}/v1".format(role)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_roles(self):
        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + '/v1'
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_features(self):
        endpoint = MANAGEMENT_AUTHORIZATION_FEATURES + '/v1'
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_features_for_user(self, user=None):
        endpoint = MANAGEMENT_AUTHORIZATION_FEATURES + '/users/{}/v1'.format(user)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        
        return response

    def get_groups_for_role(self, role=None):
        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + '/{}/groups/v1'.format(role)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_users_for_role(self, role=None):
        endpoint = MANAGEMENT_AUTHORIZATION_ROLES + '/{}/users/v1'
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response
