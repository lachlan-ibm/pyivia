"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


RUNTIME_DB = "/isam/cluster/v2"

logger = logging.getLogger(__name__)


class RuntimeDb(object):

    def __init__(self, base_url, username, password):
        super(RuntimeDb, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def set_db(self, db_type=None, port=None, host=None, secure=True, user=None, passwd=None, db_name=None, extra_attrs={}):
        """
        Set the High Volume (runtime) Database configuration.

        Args:
            db_type (:obj:`str`): The type of database that is being used. Valid values are db2, postgresql and oracle.
            port (`int`): The port on which the external database server is listening.
            host (:obj:`str`): The IP or hostname of the external database server.
            secure (`bool`): A flag true/false indicating whether or not the external database is secure.
            user (:obj:`str`): The administrator name for the external database.
            passwd (:obj:`str`): The administrator password for the external database.
            db_name (:obj:`str`): The name of the external database.
            extra_attrs (:obj:`dict`): External databases require different sets of parameters depending on the type 
                        of database.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        current = self.get_db()
        if current.success == True and current.json:
            data.data = current.json

        data.add_value_string("hvdb_address", host)
        data.add_value_string("hvdb_port", port)
        data.add_value_string("hvdb_db_secure", "true" if secure else "false")
        data.add_value_string("hvdb_user", user)
        data.add_value_string("hvdb_password", passwd)
        data.add_value_string("hvdb_db_name", db_name)
        data.add_value_string("hvdb_db_type", db_type)
        if extra_attrs != None and isinstance(extra_attrs, dict):
            for key in extra_attrs.keys():
                data.add_value(key, extra_attrs.get(key))

        endpoint = RUNTIME_DB
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204 

        return response

    def get_db(self):
        """
        Get the current database configuration.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the database configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = RUNTIME_DB

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

