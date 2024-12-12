#!/bin/python
"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


IMAGES = "/isam/container_ext/image"

logger = logging.getLogger(__name__)

'''
Class is responsible for managing container images cached by Verify Access appliances
'''
class Images(object):

    def __init__(self, base_url, username, password):
        super(Images, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, image=None):
        '''
        Pull a container image from a remote container registry. 

        Args:
            image (:obj:`str`): Name of the container image, eg. ``icr.io/ibmappgateway/ibm-application-gateway:23.04``. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the created image reference is returned as JSON and can be accessed from
            the response.json attribute
        '''
        data = DataObject()
        data.add_value_string("image", image)

        response = self.client.post_json(IMAGES, data.data)
        response.success = response.status_code == 201

        return response


    def update(self, image_id=None):
        '''
        Request the latest hash of a container image, if the hash has changed 
        then fetch the latest image and discard the old one. 

        Args:
            image_id (:obj:`str`): Unique identifier of the image being updated.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the updated image reference is returned as JSON and can be accessed from
            the response.json attribute
        '''
        endpoint = "{}/{}".format(IMAGES, image_id)
        response = self.client.put_json(endpoint)
        response.success = response.status_code == 200

        return response


    def delete(self, image_id=None):
        '''
        Delete a image from the local cache. An image can only be removed 
        if it is not in use by a container deployment. 

        Args:
            image_id (:obj:`str`): Unique identifier of the image being removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        endpoint = "{}/{}".format(IMAGES, image_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get(self, image_id=None):
        '''
        Get the detailed properties of a cached container image.

        Args:
            image_id (:obj:`str`): Unique id of image to get details details for.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the image properties are returned as JSON and can be accessed from
            the response.json attribute
        '''
        endpoint = "{}/{}".format(IMAGES, image_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        Get a list of detailed properties of a cached container images.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful image properties are returned as JSON and can be accessed from
            the response.json attribute
        '''
        response = self.client.get_json(IMAGES)
        response.success = response.status_code == 200

        return response