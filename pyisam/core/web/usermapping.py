""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

USER_MAP_CDAS = "/wga/user_map_cdas"

class UserMapping(object):

    def __init__(self, base_url, username, password):
        super(UserMapping, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, content=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("content", dynurl_config_data)

        response = self.client.post_json(USER_MAP_CDAS, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, _id=None, content=None):
        data = DataObject()
        data.add_value("content", dynurl_config_data)
        endpoint = USER_MAP_CDAS + "/{}".format(_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self, _id=None):
        endpoint = USER_MAP_CDAS + "/{}".format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, _id):
        endpoint = USER_MAP_CDAS + "/{}".format(_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_template(self):
        endpoint = "/isam/wga_templates/username_mapping_template"
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        response = self.client.get_json(USER_MAP_CDAS)
        response.success = response.status_code == 200

        return response
