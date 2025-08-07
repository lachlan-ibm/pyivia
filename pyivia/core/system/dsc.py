"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


DSC_CONFIG = "/isam/dsc/config"

logger = logging.getLogger(__name__)


class DSC(object):

    def __init__(self, base_url, username, password):
        super(DSC, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def set_dsc(self, client_grace=None, connection_idle_timeout=None, max_session_lifetime=None, 
                service_port=True, replication_port=None, ssl_ciphers=None, worker_threads=None, servers={}):
        """
        Set the Distributed Session Cace configuration.

        Args:
            client_grace (int): The length of time (in seconds) that a client (aka WebSEAL) has to 
                                reconnect before sessions owned by that client are discarded.
            connection_idle_timeout (int): The maximum length of time that a connection from a client can 
                                            remain idle before it is closed by the server. A value of 0 
                                            indicates that connections will not be reused.
            max_session_lifetime (int): The maximum lifetime (in seconds) of any session stored by the DSC.
            service_port (int): The port number on which the DSC will listen for requests.
            replication_port (int): The port number on which the DSC will listen for replication requests.
            ssl_ciphers (:obj:`str`, optional): The comma separated list of permissted SSL algorithms 
                                                for TLS connections to the DSC.
            worker_threads (int): The number of worker threads allocated to processing requests.
            servers (:obj:`dict`): The external connection data for each instance of the DSC. This 
                                    corresponds to the IP address and ports to which clients will connect. 
                                    Up to 4 servers may be defined (primary, secondary, tertiary and 
                                    quaternary). The role of the server will be determined by the order 
                                    of elements within the servers array. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        data.add_value("worker_threads", worker_threads)
        data.add_value("max_session_lifetime", max_session_lifetime)
        data.add_value("client_grace", client_grace)
        data.add_value("connection_idle_timeout", connection_idle_timeout)
        data.add_value("service_port", service_port)
        data.add_value("replication_port", replication_port)
        data.add_value("ssl_ciphers", ssl_ciphers)
        data.add_value_not_empty("servers", servers)
        response = self.client.put_json(DSC_CONFIG, data.data)
        response.success = response.status_code == 204

        return response

    def get_dsc(self):
        """
        Get the current distributed session cache configuration.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the dsc configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(DSC_CONFIG)
        response.success = response.status_code == 200

        return response

