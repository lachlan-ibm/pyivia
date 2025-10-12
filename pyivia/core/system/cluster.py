"""
@copyright: IBM

"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


CLUSTER_CONFIG = "/isam/cluster/v2"


logger = logging.getLogger(__name__)


class Cluster(object):

    def __init__(self, base_url, username, password):
        super(Cluster, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def set_config_db(self, embedded=None, db_type=None, port=None, host=None, secure=True, user=None, passwd=None, 
            db_name=None, db_key_store=None, extra_config={}) -> Response:
        """

        Set the Configuration Database connection.

        Args:
            embedded (`bool`): A flag true/false indicating whether or not the Configuration database is embedded (true) 
                            or external (false).
            db_type (:obj:`str`): The type of database that is being used. Valid values are db2, postgresql and oracle.
            port (`int`): The port on which the external database server is listening.
            host (:obj:`str`): The IP or hostname of the external database server.
            secure (`bool`, optional): A flag true/false indicating whether or not the external database is secure.
            user (:obj:`str`): The administrator name for the external database.
            passwd (:obj:`str`): The administrator password for the external database.
            db_name (:obj:`str`): The name of the external database.
            db_key_store (:obj:`str`): The SSL Key Store which contains the trusted certificate of the Oracle DB 
                            requiring secure connectivity.
            extra_config (:obj:`dict`, optional): External databases require different sets of parameters depending on 
                            the type of database. Any additional parameters can be added to a dictionary.
                            Examples of ``extra_config`` include:
        .. code-block::

            DB2
                {
                 "cfgdb_db_alt": true,
                 "cfgdb_db2_alt_address": "db2-bak.isam.ibm.com",
                 "cfgdb_db2_alt_port": "50009"
                }

            Oracle
                {"cfgdb_driver_type": "thin"}


            Postgresql
                {
                 "cfgdb_failover_servers": [
                     {"address":"secondary.pg.ibm.com",
                      "port":5432
                      "order":1
                     },
                     {"address":"tertiary.pg.ibm.com",
                      "port":5432
                      "order":2
                     }
                    ]
                }

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        current = self.get()
        if current.success == True and current.json:
            data.data = current.json
        data.add_value_boolean("cfgdb_embedded", embedded)
        data.add_value_string("cfgdb_address", host)
        data.add_value_string("cfgdb_port", port)
        data.add_value_string("cfgdb_secure", "true" if secure else "false")
        data.add_value_string("cfgdb_user", user)
        data.add_value_string("cfgdb_password", passwd)
        data.add_value_string("cfgdb_db_name", db_name)
        data.add_value_string("cfgdb_db_type", db_type)
        data.add_value_string("cfgdb_db_truststore", db_key_store)
        if extra_config != None and isinstance(extra_config, dict):
            for key in extra_config.keys():
                data.add_value(key, extra_config.get(key))

        endpoint = CLUSTER_CONFIG

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204 

        return response


    def set_runtime_db(self, embedded=None, db_type=None, port=None, host=None, secure=True, user=None, passwd=None,
            db_name=None, db_key_store=None, extra_config={}) -> Response:
        """
        Set the High Volume Database connection

        Args:
            embedded (`bool`): A flag true/false indicating whether or not the Runtime database (HVDB) is embedded 
                            (true) or external (false).
            db_type (:obj:`str`): The type of database that is being used. Valid values are db2, postgresql and oracle.
            port (`int`): The port on which the external database server is listening.
            host (:obj:`str`): The IP or hostname of the external database server.
            secure (`bool`): A flag true/false indicating whether or not the external database is secure.
            user (:obj:`str`): 	The administrator name for the external database.
            passwd (:obj:`str`): The administrator password for the external database.
            db_name (:obj:`str`): The name of the external database.
            db_key_store (:obj:`str`): 	The SSL Key Store which contains the trusted certificate for the embedded 
                            Runtime database.
            extra_config (:obj:`dict`, optional): External databases require different sets of parameters depending on 
                            the type of database. Any additional parameters can be added to a dictionary.
                            Examples of ``extra_config`` include:
        .. code-block::

            DB2
                {"cfgdb_db_alt": true,
                 "cfgdb_db2_alt_address": "db2-bak.isam.ibm.com",
                 "cfgdb_db2_alt_port": "50009"
                }

            Oracle
                {"cfgdb_driver_type": "thin"}


            Postgresql
                {"cfgdb_failover_servers": [
                     {"address":"secondary.pg.ibm.com",
                      "port":5432
                      "order":1
                     },
                     {"address":"tertiary.pg.ibm.com",
                      "port":5432
                      "order":2
                     }
                    ]
                }

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        current = self.get()
        if current.success == True and current.json:
            data.data = current.json
        data.add_value_boolean("hvdb_embedded", embedded)
        data.add_value_string("hvdb_address", host)
        data.add_value_string("hvdb_port", port)
        data.add_value_string("hvdb_db_secure", "true" if secure else "false")
        data.add_value_string("hvdb_user", user)
        data.add_value_string("hvdb_password", passwd)
        data.add_value_string("hvdb_db_name", db_name)
        data.add_value_string("hvdb_db_type", db_type)
        data.add_value_string("hvdb_db_truststore", db_key_store)
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
            cfgdb_db_name=None, cfgdb_db_secure=None, first_port=None, cfgdb_fs=None, extra_config={}) -> Response:
        """
        Update the cluster configuration.

        Args:
            primary_master (:obj:`str`): The address (management interface) of the node that is acting as the primary master.
            dsc_external_clients (`bool`): A flag true/false indicating whether clients that are external to the cluster 
                            will need to use the DSC.
            dsc_port (`int`, optional): The port over which DSC communication will take place.
            dsc_use_ssl (`bool`, optional): A flag true/false indicating whether or not SSL should be used when 
                            communicating with the DSC.
            dsc_ssl_label (:obj:`str`): The name of the SSL certificate that will be presented to clients.
            dsc_worker_threads (`int`): The number of worker threads that will be used.
            dsc_maximum_session_lifetime (`int`): The maximum lifetime of sessions within the DSC.
            dsc_client_grace_period (`int`): When a client is shut down we give the client a grace period (in seconds) 
                            to restart and register an interest in a session again before we remove the session from 
                            the session cache.
            dsc_connection_idle_timeout (`int`): The maximum length of time that a connection from a client can remain 
                            idle before it is closed by the server.
            hvdb_embedded (`bool`): A flag true/false indicating whether or not the Runtime database (HVDB) is embedded 
                            (true) or external (false).
            hvdb_max_size (`int`): The percentage of currently available disk space which can be used for the embedded 
                            Runtime database. This option is only valid if hvdb_embedded is set to true.
            hvdb_db_type (:obj:`str`): The type of database that is being used. Valid values are db2, postgresql and oracle. 
            hvdb_address (:obj:`str`): The IP or hostname of the external database server. 
            hvdb_port (`int`): The port on which the external database server is listening. 
            hvdb_user (:obj:`str`): The administrator name for the external database. 
            hvdb_password (:obj:`str`): The administrator password for the external database. 
            hvdb_db_name (:obj:`str`): The name of the external database.
            hvdb_db_secure (`bool`): A flag true/false indicating whether or not the external database is secure.
            cfgdb_embedded (`bool`): A flag true/false indicating whether or not the Configuration database is embedded 
                            (true) or external (false).
            cfgdb_db_type (:obj:`str`): The type of database that is being used.
            cfgdb_address (:obj:`str`): The IP or hostname of the external database server.
            cfgdb_port (`int`): The port on which the external database server is listening. 
            cfgdb_user (:obj:`str`): The administrator name for the external database.
            cfgdb_password (:obj:`str`): The administrator password for the external database.
            cfgdb_db_name (:obj:`str`): The name of the external database.
            cfgdb_db_secure (`bool`): A flag true/false indicating whether or not the external database is secure.
            first_port (`int`): A port number that is the first in a range of 30 ports that will be reserved for use by 
                            the cluster web services.
            cfgdb_fs (:obj:`str`): A flag true/false indicating whether to use the external Configuration database as 
                            an alternate method to share internal files among the cluster.


        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        current = self.get()
        if current.success and current.json:
            data.data = current.json
        data.add_value_string("primary_master", primary_master)
        data.add_value_boolean("dsc_external_clients", dsc_external_clients)
        data.add_value("dsc_port", dsc_port)
        data.add_value_boolean("dsc_use_ssl", dsc_use_ssl)
        data.add_value_string("dsc_ssl_label", dsc_ssl_label)
        data.add_value("dsc_worker_threads", dsc_worker_threads)
        data.add_value("dsc_maximum_session_lifetime", dsc_maximum_session_lifetime)
        data.add_value("dsc_client_grace_period", dsc_client_grace_period)
        data.add_value("dsc_connection_idle_timeout", dsc_connection_idle_timeout)
        data.add_value_boolean("hvdb_embedded", hvdb_embedded)
        data.add_value("hvdb_max_size", hvdb_max_size) 
        data.add_value_string("hvdb_db_type", hvdb_db_type)
        data.add_value_string("hvdb_address", hvdb_address)
        data.add_value("hvdb_port", hvdb_port)
        data.add_value_string("hvdb_user", hvdb_user)
        data.add_value_string("hvdb_password", hvdb_password)
        data.add_value_string("hvdb_db_name", hvdb_db_name)
        data.add_value_boolean("hvdb_db_secure", hvdb_db_secure)
        data.add_value_boolean("cfgdb_embedded", cfgdb_embedded)
        data.add_value_string("cfgdb_db_type", cfgdb_db_type)
        data.add_value_string("cfgdb_address", cfgdb_address)
        data.add_value("cfgdb_port", cfgdb_port) 
        data.add_value_string("cfgdb_user", cfgdb_user)
        data.add_value_string("cfgdb_password", cfgdb_password)
        data.add_value_string("cfgdb_db_name", cfgdb_db_name)
        data.add_value_boolean("cfgdb_db_secure", cfgdb_db_secure)
        data.add_value("first_port", first_port)
        data.add_value_boolean("cfgdb_fs", cfgdb_fs)
        if extra_config != None and isinstance(extra_config, dict):
            for key in extra_config.keys():
                data.add_value(key, extra_config.get(key))
        response = self.client.put_json(CLUSTER_CONFIG, data.data)
        response.success = response.status_code == 204
        return response


    def get(self) -> Response:
        """
        Get the current cluster configuration.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the cluster configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = CLUSTER_CONFIG

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response
