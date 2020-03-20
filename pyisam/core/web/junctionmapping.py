""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

JUNCTION_MAPPING = "/wga/jmt_config"

class JunctionMapping(object):

    def __init__(self, base_url, username, password):
        super(JunctionMapping, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, jmt_config_data=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("jmt_config_data", jmt_config_data)

        response = self.client.post_json(JUNCTION_MAPPING, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, _id=None, jmt_config_data=None):
        data = DataObject()
        data.add_value("jmt_config_data", jmt_config_data)
        endpoint = JUNCTION_MAPPING + "/{}".format(_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self, _id=None):
        endpoint = JUNCTION_MAPPING + "/{}".format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, _id):
        endpoint = JUNCTION_MAPPING + "/{}".format(_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_template(self):
        endpoint = "/isam/wga_templates/jmt_template"
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        response = self.client.get_json(JUNCTION_MAPPING)
        response.success = response.status_code == 200

        return response
