""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

KERBEROS_CONFIG = "/wga/kerberos_config"
KERBEROS_KEYTAB = "/wga/kerberos/keytab"

class Kerberos(object):

    def __init__(self, base_url, username, password):
        super(Kerberos, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, _id=None, subsection=None, name=None, value=None):
        data = DataObject()
        data.add_value_not_empty("name", name)
        data.add_value_not_empty("subsection", subsection)
        data.add_value_string("value", value)

        endpoint = KERBEROS_CONFIG + "/{}".format(_id)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def update(self, _id=None, value=None):
        data = DataObject()
        data.add_value_string("value", value)

        endpoint = KERBEROS_CONFIG + "/{}".format(_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.stauts_code == 200

        return response


    def get(self, _id=None):
        endpoint = KERBEROS_CONFIG + "/{}".format(_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def delete(self, _id=None):
        endpoint = KERBEROS_CONFIG = "/{}".format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def test(self, username=None, password=None):
        data = DataObject()
        data.add_value_string("username", username)
        data.add_value_string("password", password)

        endpoint = "/wga/kerberos/test"
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def import_keytab(self, keytab_file=None):
        
        try:
            with open(file_path, 'rb') as contents:
                files = {"keytab_file": contents}

                response = self.client.post_file(KERBEROS_KEYTAB, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response


    def delete_keytab(self, _id=None):
        endpoint = KERBEROS_KEYTAB + "/{}".format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def combine_keytab(self, new_name=None, keytab_files=[]):
        data = DataObject()
        data.add_value_string("new_name", new_name)
        data.add_value_not_empty("keytab_files", keytab_files)

        response = self.client.put_json(KERBEROS_KEYTAB, data.data)
        response.success = response.status_code == 200

        return response


    def list_keytab(self):
        response = self.client.get_json(KERBEROS_KEYTAB)
        response.success = response.status_code == 200

        return response


    def verify_keytab(self, _id=None, name=None):
        data = DataObject()
        data.add_value_string("name", name)

        endpoint = KERBEROS_KEYTAB + "/{}".format(_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response
