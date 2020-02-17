"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


CONFIG_DB = "/isam/cluster/v2"


logger = logging.getLogger(__name__)


class ConfigDb(object):

    def __init__(self, base_url, username, password):
        super(ConfigDb, self).__init__()
        self.client = RESTClient(base_url, username, password)


    """
    setup the CONFIG database.

    """
    def set_db(self, db_type=None, port=None, host=None, secure=True, user=None,
            passwd=None, db_name=None):
        data = DataObject()
        get_response = self.get_db()
        data.data = get_response.json

        data.add_value_string("cfgdb_address", host)
        data.add_value_string("cfgdb_port", port)
        data.add_value_string("cfgdb_secure", "true" if secure else "false")
        data.add_value_string("cfgdb_user", user)
        data.add_value_string("cfgdb_password", passwd)
        data.add_value_string("cfgdb_db_name", db_name)
        data.add_value_string("cfgdb_db_type", db_type)

        endpoint = CONFIG_DB

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204 

        return response

    def get_db(self):
        endpoint = CONFIG_DB

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

