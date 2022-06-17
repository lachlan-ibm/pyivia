"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


CLUSTER_CONFIG = "/isam/cluster/v2"


logger = logging.getLogger(__name__)


class ConfigDb(object):

    def __init__(self, base_url, username, password):
        super(ConfigDb, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def set_config_db(self, embedded=None, db_type=None, port=None, host=None, secure=True, user=None, passwd=None, 
            db_name=None, extra_config={}):
        """
        Set the Configuration Database connection.

        Args:
            db_type (:obj:`str`)): 
        """
        data = DataObject()
        get_response = self.get_cluster()
        data.data = get_response.json
        data.add_vaule_boolean("cfgdb_embedded", embedded)
        data.add_value_string("cfgdb_address", host)
        data.add_value_string("cfgdb_port", port)
        data.add_value_string("cfgdb_secure", "true" if secure else "false")
        data.add_value_string("cfgdb_user", user)
        data.add_value_string("cfgdb_password", passwd)
        data.add_value_string("cfgdb_db_name", db_name)
        data.add_value_string("cfgdb_db_type", db_type)
        if extra_config != None and isinstance(extra_config, dict):
            for key in extra_config.keys():
                data.add_value(key, extra_config.get(key))

        endpoint = CLUSTER_CONFIG

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204 

        return response


    def set_runtime_db(self, embedded=None, db_type=None, port=None, host=None, secure=True, user=None, db_name=None, 
            extra_config={}):
        """
        Set the High Volume Database connection

        """
        data = DataObject()
        get_response = self.get_cluster()
        data.data = get_response.json
        data.add_vaule_boolean("hvdb_embedded", embedded)
        data.add_value_string("hvdb_address", host)
        data.add_value_string("hvdb_port", port)
        data.add_value_string("hvdb_secure", "true" if secure else "false")
        data.add_value_string("hvdb_user", user)
        data.add_value_string("hvdb_password", passwd)
        data.add_value_string("hvdb_db_name", db_name)
        data.add_value_string("hvdb_db_type", db_type)
        if extra_config != None and isinstance(extra_config, dict):
            for key in extra_config.keys():
                data.add_value(key, extra_config.get(key))

        endpoint = CLUSTER_CONFIG

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204 

        return response
        return


    def update_cluster(self, primary_master=None, dsc_external_clients=False, dsc_port=None, dsc_use_ssl=None, 
            dsc_ssl_label=None, dsc_worker_threads=None, dsc_maximum_session_lifetime=None, dsc_client_grace_period=None,
            dsc_connection_idle_timeout=None, hvdb_embedded=None, hvdb_max_size=None, hvdb_db_type=None, 
            hvdb_address=None, hvdb_port=None, hvdb_user=None, hvdb_password=None, hvdb_db_name=None, hvdb_db_secure=None,
            cfgdb_embedded=None, cfgdb_db_type=None, cfgdb_address=None, cfgdb_port=None, cfgdb_user=None, cfgdb_password=None,
            cfgdb_db_name=None, cfgdb_db_secure=None, first_port=None, cfgdb_fs=None, extra_config={}):
        """
        Update the cluster configuration.

        Args:

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        get_response = self.get_cluster()
        data.data = get_response.json
        if extra_config != None and isinstance(extra_config, dict):
            for key in extra_config.keys():
                data.add_value(key, extra_config.get(key))


    def get_cluster(self):
        """
        Get the current cluster configuration.

        Ruturns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the obligations are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = CLUSTER_CONFIG

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


