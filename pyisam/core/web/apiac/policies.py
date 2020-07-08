"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

POLICY = "/wga/apiac/policy"

class Policies(object):

    def __init__(self, base_url, username, password):
        super(Policies, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, groups=[], attributes=[]):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_not_empty("group", grups)
        data.add_value_not_empty("attributes", attributes)

        response = self.client.post_json(POLICY, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, name, groups=[], attributes=[]):
        data = DataObject()
        data.add_value_not_empty("groups", groups)
        data.add_value_not_empty("attributes", attributes)

        endpoint = POLICY + "/{}".format(name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def get(self, name=None):
        endpoint = POLICY + "/{}".format(name)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def delete(self, name=None):
        endpoint = POLICY + "/{}".format(name)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200
        
        return response


    def list(self):
        response = self.client.get_json(POLICY)
        response.success = response.status_code == 200

        return response
