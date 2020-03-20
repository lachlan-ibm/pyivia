""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

RATELIMIT = "/wga/ratelimiting"

class Rate_Limit(object):

    def __init__(self, base_url, username, password):
        super(Rate_Limit, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, content=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("content", content)

        response = self.client.post_json(RATELIMIT, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, _id=None, content=None):
        data = DataObject()
        data.add_value("content", content)
        endpoint = RATELIMIT + "/{}".format(_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self, _id=None):
        endpoint = RATELIMIT + "/{}".format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, _id):
        endpoint = RATELIMIT + "/{}".format(_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        response = self.client.get_json(RATELIMIT)
        response.success = response.status_code == 200

        return response
