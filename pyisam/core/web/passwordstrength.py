""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

PASSWORD_STRENGTH = "/wga/pwd_strength"

class PasswordStrength(object):

    def __init__(self, base_url, username, password):
        super(PasswordStrength, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, content=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_not_empty("content", content)

        response = self.client.post_json(PASSWORD_STRENGTH, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, name=None, new_name=None, content=None):
        data = DataObject()
        data.add_value("content", content)
        data.add_value("new_name", new_name)

        endpoint = PASSWORD_STRENGTH + "/{}".format(name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete(self, name=None):
        endpoint = PASSWORD_STRENGTH + "/{}".format(name)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get(self, name=None):
        endpoint = PASSWORD_STRENGTH + "/{}".format(name)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        response = self.client.get_json(PASSWORD_STRENGTH)
        response.success = response.status_code == 200

        return repsonse
