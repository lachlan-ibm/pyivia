#!/bin/python
"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


METADATA = "/isam/container_ext/metadata"

logger = logging.getLogger(__name__)

'''
Class is responsible for managing container metadata required by Verify Access 
appliances hosting containers.
'''
class Metadata(object):


    def __init__(self, base_url, username, password):
        super(Metadata, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def get(self, metadata_name=None):
        '''
        Get the metadata properties for a managed container. 

        Args:
            metadata_name (:obj:`str`): Name of the container metadata document.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the image metadata is returned as JSON and can be accessed from
            the response.json attribute
        '''
        endpoint = "{}/{}".format(METADATA, metadata_name)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        Get the metadata properties for all known managed containers.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the image metadata is returned as JSON and can be accessed from
            the response.json attribute
        '''
        response = self.client.get_json(METADATA)
        response.success = response.status_code == 200

        return response