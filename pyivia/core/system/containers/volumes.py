#!/bin/python
"""
@copyright: IBM
"""

import logging
from requests import Response

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


VOLUMES = "/isam/container_ext/volumes"

logger = logging.getLogger(__name__)

'''
Class is responsible for managing container volumes hosted by Verify Access appliances.
'''
class Volumes(object):

    def __init__(self, base_url, username, password):
        super(Volumes, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None):
        '''
        Create a volume which can be mounted to a container deployment. 

        Args:
            name (:obj:`str`): Name of the volume to be created.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the created volume is returned as JSON and can be accessed from
            the response.json attribute
        '''
        data = DataObject()
        data.add_value_string("name", name)

        response = self.client.post_json(VOLUMES, data.data)
        response.success = response.status_code == 201

        return response


    def export_volume(self, volume_id=None, exported_volume=None):
        '''
        Export the files of a container volume mount.

        Args:
            volume_id (:obj:`str`): Unique id of the volume to export.
            exported_volume (:obj:`str`): Local file to write exported volume to.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        if not exported_volume:
            r = Response()
            setattr(r, 'status_code', 404)
            setattr(r, 'content', 'No volume specified')
            setattr(r, 'success', False)
            return r

        endpoint = "{}/{}".format(VOLUMES, volume_id)
        response = self.client.get_file(endpoint, exported_volume)

        response.success = response.status_code == 200

        return response


    def import_volume(self, volume_id=None, volume=None):
        '''
        Export the files of a container volume mount.

        Args:
            volume_id (:obj:`str`): Unique id of the volume the zip file should be imported to.
            volume (:obj:`str`): Local archive (zip) to be uploaded as volume.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        endpoint = "{}/{}".format(VOLUMES, volume_id)

        if not volume:
            r = Response()
            setattr(r, 'status_code', 404)
            setattr(r, 'content', 'No volume specified')
            setattr(r, 'success', False)
            return r

        with open(volume, 'rb') as f:
            data = {"volume": f}
            response = self.client.post_file(endpoint, files=data)
            response.success = response.status_code == 200

            return response


    def list(self):
        '''
        Get a list of the configured container volumes as JSON.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful volume properties are returned as JSON and can be accessed from
            the response.json attribute.
        '''
        response = self.client.get_json(VOLUMES)
        response.success = response.status_code == 200

        return response


    def delete(self, volume_id=None):
        '''
         Delete a container volume. A volume can only be removed if it is not in use by a container deployment. 

        Args:
            volume_id (:obj:`str`): Unique id of the volume to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful volume properties are returned as JSON and can be accessed from
            the response.json attribute.
        '''
        endpoint = "{}/{}".format(VOLUMES, volume_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response