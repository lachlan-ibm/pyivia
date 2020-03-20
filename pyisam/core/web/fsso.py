""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

FSSO_CONFIG = "/wga/fsso_config"

class FSSO(object):

    def __init__(self, base_url, username, password):
        super(FSSO, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, fsso_config_data=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("fsso_config_data", fsso_config_data)

        response = self.client.post_json(FSSO_CONFIG, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, _id=None, fsso_config_data=None):
        data = DataObject()
        data.add_value("fsso_config_data", fsso_config_data)
        endpoint = FSSO_CONFIG + "/{}".format(_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self, _id=None):
        endpoint = FSSO_CONFIG + "/{}".format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, _id):
        endpoint = FSSO_CONFIG + "/{}".format(_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        response = self.client.get_json(FSSO_CONFIG)
        response.success = response.status_code == 200

        return response
