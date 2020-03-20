""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

CLIENT_CERT_CDAS = "/wga/client_cert_cdas"

class ClientCertMapping(object):

    def __init__(self, base_url, username, password):
        super(ClientCertMapping, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, content=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("content", content)

        response = self.client.post_json(CLIENT_CERT_CDAS, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, _id=None, content=None):
        data = DataObject()
        data.add_value("content", content)
        data.add_value_string("id", _id)
        endpoint = CLIENT_CERT_CDAS + "/{}".format(_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self, _id=None):
        endpoint = CLIENT_CERT_CDAS + "/{}".format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, _id):
        endpoint = CLIENT_CERT_CDAS + "/{}".format(_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_template(self, tempalte_id=None):
        endpoit = "/isam/wga_templates/client_cert_cdas_template"
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        response = self.client.get_json(CLIENT_CERT_CDAS)
        response.success = response.status_code == 200

        return response
