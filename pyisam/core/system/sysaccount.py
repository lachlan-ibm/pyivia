""""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


SYSACCOUNT = '/sysaccount'
SYSACCOUNT_USERS = SYSACCOUNT + '/users'
SYSACCOUNT_GROUPS = SYSACCOUNT + '/groups'

logger = logging.getLogger(__name__)


class SysAccount(object):

    def __init__(self, base_url, username, password):
        super(SysAccount, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_users(self):
        endpoint = SYSACCOUNT_USERS + '/v1'
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_user(self, user):
        endpoint = SYSACCOUNT_USERS + '/' + user + '/v1'
        rsponse = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def update_user(self, user, password=None):
        data = DataObject()
        data.add_value_string('password', password)

        endpoint = SYSACCOUNT_USERS + '/' + user + '/v1'
        rsponse = self.client.put_json(endpoint)
        response.success = response.status_code == 204

        return response


    def create_user(self, user=None, password=None, groups=[]):
        data = DataObject()
        data.add_value_string('id', user)
        data.add_value_string('password', password)
        if groups:
            groups_data = DataObject()
            for group in groups:
                groups_data.add_value('id': group)
            data.add_value_not_empty('groups', groups_data.data)
        endpoint = SYSACCOUNT_USERS + '/v1'
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_user(self, user):
        endpoint = SYSACCOUNT_USERS + '/' + user + '/v1'
        response = self.client.delete_json(endpoint)

        response.success = response.status_code == 204

        return response


    def get_groups(self):
        endpoint = SYSACCOUNT_GROUPS + '/v1'
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get group(self, group=None):
        endpoint = SYSACCOUNT_GROUPS + '/groups/{}/v1'.format(group)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def add_user(self, group=None, user=None):
        data = DataObject()
        data.add_alue_string("id", group)
        endpoint = SYSACCOUNT_GROUPS + '/{}/groups/v1'.format(user)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def remove_user(self, group=None, user=None):
        endpoint = SYSACCOUNT_GROUPS + '/users/{}/groups/{}/v1'.format(user, group)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def create_group(self, group=None):
        data = DataObject()
        data.add_value_string("id", group)
        endpoint = SYSACCOUNT_GROUPS +'/v1'
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_group(self, group=None):
        endpoint = SYSACCOUNT_GROUPS + '/{}/v1'.format(group)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
