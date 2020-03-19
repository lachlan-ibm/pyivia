""""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


ADVANCED_PARAMETERS = "/core/adv_params"

logger = logging.getLogger(__name__)


class AdvancedTuning(object):

    def __init__(self, base_url, username, password):
        super(AdvancedTuning, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_parameter(self, key=None, value=None, comment=None):
        data = DataObject()
        data.add_value_string("key", key)
        data.add_value_string("value", value)
        data.add_value_string("comment", comment)
        data.add_value("_isNew", True)

        response = self.client.post_json(ADVANCED_PARAMETERS, data.data)
        response.success = response.status_code == 201

        return response

    def update_parameter(self, id=None, key=None, value=None, comment=None):
        data = DataObject()
        data.add_value_string("key", key)
        data.add_value_string("value", value)
        data.add_value_string("comment", comment)

        response = self.client.put_json(ADVANCED_PARAMETERS+"/"+id, data.data)

        response.success = response.status_code == 200

        return response

    def list_parameters(self):
        response = self.client.get_json(ADVANCED_PARAMETERS)
        response.success = response.status_code == 200

        if response.success:
            response.json = response.json.get("tuningParameters", [])

        return response

    def delete_parameter(self, uuid=None):
        endpoint = ADVANCED_PARAMETERS + "/{}".format(uuid)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
