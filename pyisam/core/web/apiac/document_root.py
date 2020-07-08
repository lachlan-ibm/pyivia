"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)


APIAC = "/wga/apiac/resource"

class DocumentRoot(object):

    def __init__(self, base_url, username, password):
        super(DocumentRoot, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, instance, file_name=None, file_type=None, contents=None):
        data = DataObject()
        data.add_value_string("file_name", file_name)
        data.add_value_string("type", file_type)
        data.add_value_string("contents", contents)

        endpoint = APIAC + "/instance/{}/documentation".format(instance)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def rename(self, instance, name=None, new_name=None, file_type=None):
        data = DataObject()
        data.add_value_string("new_name", new_name)
        data.add_value_string("type", file_type)

        endpoint = APIAC + "/instance/{}/documentation/{}".format(instance, name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, instance, name=None, file_type=None, contents=None):
        data = DataObject()
        data.add_value_string("contents", contents)
        data.add_value_string("type", file_type)
        
        endpoint = APIAC + "/instance/{}/documentation/{}".format(instance, name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def get(self, instance, name=None):
        endpoint = APIAC + "/instance/{}/documentation/{}".format(instance, name)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self, instance):
        endpoint = APIAC + "/instance/{}/documentation".format(instance)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response
