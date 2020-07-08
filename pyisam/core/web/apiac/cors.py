"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

CORS_POLICY = "/wga/apiac/cors"

class CORS(object):

    def __init__(self, base_url, username, password):
        super(CORS, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, allowed_origins=[], allow_credentials=None, exposed_headers=[],
            handle_preflight=None, allowed_methods=[], allowed_headers=[], max_age=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_not_empty("allowed_origins", allowed_origins)
        data.add_value_boolean("allow_credentials", allow_credentials)
        data.add_value_not_empty("exposed_headers", exposed_headers)
        data.add_value_boolean("handle_preflight", handle_preflight)
        data.add_value_not_empty("alowed_methods", allowed_methods)
        data.add_value_not_empty("alowed_headers", allowed_headers)
        data.add_value("max_age", max_age)

        response = self.client.put_json(CORS_POLICY, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, name, allowed_origins=[], allow_credentials=None, exposed_headers=[],
            handle_preflight=None, allowed_methods=[], allowed_headers=[], max_age=None):
        data = DataObject()
        data.add_value_not_empty("allowed_origins", allowed_origins)
        data.add_value_boolean("allow_credentials", allow_credentials)
        data.add_value_not_empty("exposed_headers", exposed_headers)
        data.add_value_boolean("handle_preflight", handle_preflight)
        data.add_value_not_empty("alowed_methods", allowed_methods)
        data.add_value_not_empty("alowed_headers", allowed_headers)
        data.add_value("max_age", max_age)

        endpoint = CORS_POLICY + "/{}".format(name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete(self, name=None):
        endpoint = CORS_POLICY + "/{}".format(name)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get(self, name=None):
        endpoint = CORS_POLICY + "/{}".format(name)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        response = self.client.get_json(CORS_POLICY)
        response.success = response.status_code == 200

        return response
