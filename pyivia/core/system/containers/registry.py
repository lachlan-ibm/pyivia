#!/bin/python
"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


REGISTRY = "/isam/container_ext/repo"

logger = logging.getLogger(__name__)

'''
Class is responsible for managing authorization configuration to 
external container image registries.
'''
class Registry(object):


    def __init__(self, base_url, username, password):
        super(Registry, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create(self, host=None, username=None, secret=None, proxy_host=None, proxy_port=None,
               proxy_user=None, proxy_pass=None, proxy_schema=None, ca=None):
        '''
        Create a credential for a user and container registry.

        Args:
            host (:obj:`str`): The address or domain name of the registry to authenticate to.
            username (:obj:`str`, optional): The user to authenticate as.
            secret (:obj:`str`, optional): The secret to authenticate with.
            proxy_host (:obj:`str`, optional): An optional proxy to set when pulling images from this container registry. 
            proxy_port (:obj:`str`, optional): The port for the proxy. The default is 3128.
            proxy_user (:obj:`str`, optional): The user to authenticate to the proxy with.
            proxy_pass (:obj:`str`, optional): The password to authenticate to the proxy with. Must be provided if proxy_user is set.
            proxy_schema (:obj:`str`, optional): The TCP schema to use. The default is ``http``.
            ca (:obj:`str`, optional): A X509 Certificate Authority (CA) bundle file to use when verifying connections to this registry.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the created container registry reference is returned as JSON and can be accessed from
            the response.json attribute
        '''
        data = DataObject()
        data.add_value_string("host", host)
        data.add_value_string("user", username)
        data.add_value_string("secret", secret)
        data.add_value_string("proxy_host", proxy_host)
        data.add_value_string("proxy_port", proxy_port)
        data.add_value_string("proxy_user", proxy_user)
        data.add_value_string("proxy_pass", proxy_pass)
        data.add_value_string("proxy_schema", proxy_schema)
        if ca:
            with open(ca, 'r') as f:
                data.add_value_string("ca", f.read())

        response = self.client.post_json(REGISTRY, data.data)
        response.success = response.status_code == 201

        return response


    def update(self, rgy_id, host=None, username=None, secret=None, proxy_host=None, proxy_port=None,
               proxy_user=None, proxy_pass=None, proxy_schema=None):
        '''
        Update the username/secret used to authenticate to a Container Registry. This 
        will override any existing login configuration. 

        Args:
            rgy_id(:obj:`str`): The id of the registry credential to be updated.
            host (:obj:`str`): The address or domain name of the registry to authenticate to.
            username (:obj:`str`, optional): The user to authenticate as.
            secret (:obj:`str`, optional): The secret to authenticate with.
            proxy_host (:obj:`str`, optional): An optional proxy to set when pulling images from this container registry. 
            proxy_port (:obj:`str`, optional): The port for the proxy. The default is 3128.
            proxy_user (:obj:`str`, optional): The user to authenticate to the proxy with.
            proxy_pass (:obj:`str`, optional): The password to authenticate to the proxy with. Must be provided if proxy_user is set.
            proxy_schema (:obj:`str`, optional): The TCP schema to use. The default is ``http``.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        data = DataObject()
        data.add_value_string("host", host)
        data.add_value_string("user", username)
        data.add_value_string("secret", secret)
        data.add_value_string("proxy_host", proxy_host)
        data.add_value_string("proxy_port", proxy_port)
        data.add_value_string("proxy_user", proxy_user)
        data.add_value_string("proxy_pass", proxy_pass)
        data.add_value_string("proxy_schema", proxy_schema)

        endpoint = "{}/{}".format(REGISTRY, rgy_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response


    def delete(self, rgy_id=None):
        '''
        Delete a credential for a user and container registry.

        Args:
            rgy_id(:obj:`str`): The id of the registry credential to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        endpoint = "{}/{}".format(REGISTRY, rgy_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, rgy_id=None):
        '''
        Get the credential for known users of a container registry. 

        Args:
            rgy_id(:obj:`str`): Unique id for registry to get authentication details for.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the container registry is returned as JSON and can be accessed from
            the response.json attribute
        '''
        endpoint = "{}/{}".format(REGISTRY, rgy_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        Get all known credential for all container registries.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the container registry are returned as JSON and can be accessed from
            the response.json attribute
        '''
        response = self.client.get_json(REGISTRY)
        response.success = response.status_code == 200

        return response