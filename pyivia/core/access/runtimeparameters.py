"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


RUNTIME_TUNING = "/mga/runtime_tuning"
RUNTIME_TRACE = RUNTIME_TUNING + "/trace_specification/v1"
ENDPOINTS = "endpoints"

logger = logging.getLogger(__name__)


class RuntimeParameters(object):

    def __init__(self, base_url, username, password):
        super(RuntimeParameters, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def update_parameter(self, parameter, value=None):
        '''
        Update a single runtime tuning parameter.

        Args:
            value (:obj:`str`): The parameter to be updated.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value("value", value)

        endpoint = "%s/%s/v1" % (RUNTIME_TUNING, parameter)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def list_parameters(self):
        '''
        Get a list of all of the configured runtime tuning parameters.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the runtime tuning parameters are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = "%s/v1" % RUNTIME_TUNING

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def add_listening_interface(self, interface, port, secure=None):
        '''
        Add a new endpoint for the runtime server.

        Args:
            interface (:obj:`str`): The concatenation of the interface and IP address UUIDs, separated by a '.' character.
                                    eg: ``38a69185-a61a-44a1-b574-a3b502f01414.f980aabe-80b7-4738-9cda-bccede8d34f2``
            port (int): The port that the endpoint will listen on.
            secure (bool): Flag to indicate if endpoint uses SSL

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the new runtime endpoint id is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        data = DataObject()
        data.add_value("interface", interface)
        data.add_value("port", port)
        data.add_value("secure", secure)

        endpoint = "%s/%s/v1" % (RUNTIME_TUNING, ENDPOINTS)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_listening_interface(self, interface, port):
        '''
        Remove an existing runtime endpoint.

        Args:
            interface (:obj:`str`): The concatenation of the interface and IP address UUIDs, separated by a '.' character.
                                    eg: ``38a69185-a61a-44a1-b574-a3b502f01414.f980aabe-80b7-4738-9cda-bccede8d34f2``
            port (int): The port that the endpoint will listen on.
            secure (bool): Flag to indicate if endpoint uses SSL

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "%s/%s/%s:%d/v1" % (RUNTIME_TUNING, ENDPOINTS, interface, port)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def update_trace(self, trace_string=""):
        '''
        Update the JVM trace settings for the Runtime Liberty server.

        Args:
            trace_string (:obj:`str`): The new JVM trace settings.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.        
        '''
        parameters = DataObject()
        parameters.add_value("value", trace_string)

        response = self.client.put_json(RUNTIME_TRACE, parameters.data)
        response.success = response.status_code == 204

        return response
