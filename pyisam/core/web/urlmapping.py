""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

URL_MAPPING = "/wga/dynurl_config"

class URLMapping(object):

    def __init__(self, base_url, username, password):
        super(URLMapping, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, dynurl_config_data=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("dynurl_config_data", dynurl_config_data)

        response = self.client.post_json(URL_MAPPING, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, _id=None, dynurl_config_data=None):
        data = DataObject()
        data.add_value("dynurl_config_data", dynurl_config_data)
        endpoint = URL_MAPPING + "/{}".format(_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self, _id=None):
        endpoint = URL_MAPPING + "/{}".format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, _id):
        endpoint = URL_MAPPING + "/{}".format(_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_template(self):
        endpoint = "/isam/wga_templates/dynurl_template"
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        response = self.client.get_json(URL_MAPPING)
        response.success = response.status_code == 200

        return response
