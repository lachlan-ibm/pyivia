""""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient

REMOTE_SYS_LOGS = "/isam/rsyslog_forwarder"

logger = logging.getLogger(__name__)


class RemoteSyslog(object):

    def __init__(self, base_url, username, password):
        super(RemoteSyslog, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get(self, source=None):
        '''
        Get the configuration for the given Remote Syslog source.

        Args:
            source (:obj:`str`): The name of the log source. It can be either ``webseal``, 
                                ``azn_server``, ``policy_server`` or ``runtime_logs``.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the remote system logger properties is returned 
            as JSON and can be accessed from the response.json attribute
        '''
        endpoint = "{}/{}".format(REMOTE_SYS_LOGS, source)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        List the Remote Syslog configuration.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the remote system logger properties are returned 
            as JSON and can be accessed from the response.json attribute
        '''
        response = self.client.get_json(REMOTE_SYS_LOGS)
        response.success = response.status_code == 200

        return response


    def add_server(self, server=None, port=None, debug=None, protocol=None, format=None,
               keyfile=None, ca_certificate=None, client_certificate=None, permitted_peers=None,
               sources=[]):
        '''
        Add a Remote Syslog configuration.

        Args:
            server: (:obj:`str`): The IP address or host name of the remote syslog server.
            port (`int`): The port on which the remote syslog server is listening.
            debug (`bool`): Whether the forwarder process will be started in debug mode. 
                            All trace messages will be sent to the log file of the remote 
                            syslog forwarder.
            protocol (:obj:`str`): The protocol which will be used when communicating with the 
                                   remote syslog server. Valid options include ``udp``, ``tcp`` 
                                   or ``tls``.
            format (:obj:`str`, optional): 	The format of the messages which are forwarded to 
                                            the rsyslog server. Valid options include ``rfc-3164`` or 
                                            ``rfc-5424``.
            keyfile (:obj:`str`, optional): The name of the key file which contains the SSL certificates
                                            used when communicating with the remote syslog server (e.g. pdsrv). 
                                            This option is required if the protocol is ``tls``.
            ca_certificate (:obj:`str`, optional): The label which is used to identify within the SSL key file 
                                                   the CA certificate of the remote syslog server. This option 
                                                   is required if the protocol is ``tls``.
            client_certificate (:obj:`str`, optional): The label which is used to identify within the SSL key file 
                                                the client certificate which will be used during mutual 
                                                authentication with the remote syslog server.
            permitted_peers (:obj:`str`, optional): The subject DN of the remote syslog server. If this policy 
                                                data is not specified any certificates which have been signed by 
                                                the CA will be accepted.
            sources (:obj:`list` :obj:`dict`): The source of the log file entries which will be sent to the remote 
                                                syslog server. The format of the dictionary is::

                                                                                   {
                                                                                        "name": "WebSEAL:default:request.log",
                                                                                        "tag": "WebSEAL",
                                                                                        "facility": "local0",
                                                                                        "severity": "debug"
                                                                                    }

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("server", server)
        data.add_value("port", port)
        data.add_value_boolean("debug", debug)
        data.add_value_string("protocol", protocol)
        data.add_value_string("format", format)
        data.add_value_string("keyfile", keyfile)
        data.add_value_string("ca_certificate", ca_certificate)
        data.add_value_string("client_certificate", client_certificate)
        data.add_value_string("permitted_peers", permitted_peers)
        data.add_value_not_empty("sources", sources)

        servers = self.list().json
        if servers == None or not isinstance(servers, list):
            response = Response()
            response.success= False
            return response
        idx = -1
        for i, s in enumerate(servers):
            if s.get('name', "") == server:
                idx = i
        if idx != -1:
            del servers[idx]
        servers += [data.data]
        response = self.client.put_json(REMOTE_SYS_LOGS, servers)
        response.success = response.status_code == 204

        return response


    def update(self, servers=[]):
        '''
        Update the Remote Syslog configuration.

        Args:
            servers: (:obj:`list` of :obj:`str`): The remote server configuration to use.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        response = self.client.put_json(REMOTE_SYS_LOGS, servers)
        response.success = response.status_code == 204

        return response