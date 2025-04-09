#!/bin/python
"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


HEALTH = "/isam/container_ext/health"

logger = logging.getLogger(__name__)

class HealthCheck(object):
    '''
    Class is responsible for managing authorization configuration to 
    external container image registries.
    '''

    def __init__(self, base_url, username, password):
        super(HealthCheck, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get(self, deployment_id=None):
        '''
        Get the health of a configured container as JSON.

        Args:
            deployment_id (:obj:`str`): Unique id of the managed container.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the health check output is returned as JSON and can be accessed from
            the response.json attribute
        '''
        endpoint = "{}/{}".format(HEALTH, deployment_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def list(self):
        '''
        Get the health of all configured containers as JSON. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the health check output is returned as JSON and can be accessed from
            the response.json attribute
        '''
        response = self.client.get_json(HEALTH)
        response.success = response.status_code == 200

        return response