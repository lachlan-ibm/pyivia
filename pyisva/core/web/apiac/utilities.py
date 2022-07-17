"""
@copyright: IBM
"""

import logging

from pyisva.util.model import DataObject
from pyisva.util.restclient import RESTClient

logger = logging.getLogger(__name__)

APIAC = "/wga/apiac"
CREDENTIALS = APIAC + "/credentials"
GROUPS = APIAC + "/groups"

class Utilities(object):

    def __init__(self, base_url, username, password):
        super(Utilities, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def store_crednetial(self, admin_id=None, admin_pwd=None, admin_domain=None):
        data = DataObject()
        data.add_value_string("admin_id", admin_id)
        data.add_value_string("admin_pwd", admin_pwd)
        data.add_value_string("admin_domain", admin_domain)

        response = self.client.post_json(CREDENTIALS, data.data)
        response.success = response.status_code == 200

        return response


    def delete_credential(self):
        response = self.client.delete_json(CREDENTIALS)
        response.success = response.status_code == 200

        return response


    def get_credential(self):
        response = self.client.get_json(CREDENTIALS)
        response.success = response.status_code == 200

        return response


    def list_groups(self):
        response = self.client.get_json(GROUPS)
        response.success = response.status_code == 200

        return response
