"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

CORS_POLICY = "/wga/apiac/cors"

class CORS(object):

    def __init__(self, base_url, username, password):
        super(CORS, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, allowed_origins=[], allow_credentials=None, exposed_headers=[],
            handle_preflight=None, allowed_methods=[], allowed_headers=[], max_age=None):
        '''
        Create a CORS policy

        Args:
            name (:obj:`str`): The name of the CORS policy.
            allowed_origins (:obj:`list` of :obj:`str`): An array of origins which are allowed to make cross origin 
                                                        requests to this resource.
            allow_credentials (bool): Controls whether or not the Access-Control-Allow-Credentials header will be set.
            exposed_headers (bool): Controls the values populated in the Access-Control-Expose-Headers header.
            handle_preflight (bool): Controls whether or not the Reverse Proxy will handle pre-flight requests.
            allowed_methods (:obj:`list` of :obj:`str`): HTTP methods permitted in pre-flight requests and the subsequent 
                                                        Access-Control-Allow-Methods header.
            allowed_headers (:obj:`list` of :obj:`str`): Names of HTTP headers permitted in pre-flight requests and the 
                                                        subsequent Access-Control-Allow-Headers header.
            max_age (int): Set the Access-Control-Max-Age header added to pre-flight requests.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_not_empty("allowed_origins", allowed_origins)
        data.add_value_boolean("allow_credentials", allow_credentials)
        data.add_value_not_empty("exposed_headers", exposed_headers)
        data.add_value_boolean("handle_preflight", handle_preflight)
        data.add_value_not_empty("allowed_methods", allowed_methods)
        data.add_value_not_empty("allowed_headers", allowed_headers)
        data.add_value("max_age", max_age)

        response = self.client.put_json(CORS_POLICY, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, name, allowed_origins=[], allow_credentials=None, exposed_headers=[],
            handle_preflight=None, allowed_methods=[], allowed_headers=[], max_age=None):
        '''
        Update an existing CORS policy.

        Args:
            name (:obj:`str`): The name of the CORS policy.
            allowed_origins (:obj:`list` of :obj:`str`): An array of origins which are allowed to make cross origin 
                                                        requests to this resource.
            allow_credentials (bool): Controls whether or not the Access-Control-Allow-Credentials header will be set.
            exposed headers (bool): Controls the values populated in the Access-Control-Expose-Headers header.
            handle_preflight (bool): Controls whether or not the Reverse Proxy will handle pre-flight requests.
            allowed_methods (:obj:`list` of :obj:`str`): HTTP methods permitted in pre-flight requests and the subsequent 
                                                        Access-Control-Allow-Methods header.
            allowed_headers (:obj:`list` of :obj:`str`): Names of HTTP headers permitted in pre-flight requests and the 
                                                        subsequent Access-Control-Allow-Headers header.
            max_age (int): Set the Access-Control-Max-Age header added to pre-flight requests.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_not_empty("allowed_origins", allowed_origins)
        data.add_value_boolean("allow_credentials", allow_credentials)
        data.add_value_not_empty("exposed_headers", exposed_headers)
        data.add_value_boolean("handle_preflight", handle_preflight)
        data.add_value_not_empty("allowed_methods", allowed_methods)
        data.add_value_not_empty("allowed_headers", allowed_headers)
        data.add_value("max_age", max_age)

        endpoint = CORS_POLICY + "/{}".format(name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete(self, name=None):
        '''
        Delete an existing CORS policy.

        Args:
            name (:obj:`str`): The name of the CORS policy to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = CORS_POLICY + "/{}".format(name)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get(self, name=None):
        '''
        Get a configured CORS policy.

        Args:
            name (:obj:`str`): The name of the CORS policy.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the CORS policy is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = CORS_POLICY + "/{}".format(name)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        List the configured CORS policies.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the CORS policies are returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = self.client.get_json(CORS_POLICY)
        response.success = response.status_code == 200

        return response
