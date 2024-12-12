"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)


APIAC = "/wga/apiac/resource"

class DocumentRoot(object):

    def __init__(self, base_url, username, password):
        super(DocumentRoot, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, instance, file_name=None, file_type=None, contents=None):
        '''
        Create a new file or directory in the API Access Control document root.

        Args:
            instance (:obj:`str`): The name of the WebSEAL instance being configured.
            file_name (:obj:`str`): Name of new file or directory.
            file_type (:obj:`str`): Type of file. Either "file" or "dir".
            contents (:obj:`str`): If ``file_type == "file"`` this is the contents of the new file.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the file is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        data = DataObject()
        data.add_value_string("file_name", file_name)
        data.add_value_string("type", file_type)
        data.add_value_string("contents", contents)

        endpoint = APIAC + "/instance/{}/documentation".format(instance)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def rename(self, instance, name=None, new_name=None, file_type=None):
        '''
        Rename a file or directory in the API Access Control document root.

        Args:
            instance (:obj:`str`): The name of the WebSEAL instance being configured.
            name (:obj:`str`): Name of the existing file or directory.
            new_name (:obj:`str`): New name of the file or directory.
            file_type (:obj:`str`): File type being modified.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the file is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        data = DataObject()
        data.add_value_string("new_name", new_name)
        data.add_value_string("type", file_type)

        endpoint = APIAC + "/instance/{}/documentation/{}".format(instance, name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, instance, name=None, file_type=None, contents=None):
        '''
        Update an existing file in the API Access Control document root.

        Args:
            instance (:obj:`str`): The name of the WebSEAL instance being configured.
            file_name (:obj:`str`): Name of new file or directory.
            file_type (:obj:`str`): Type of file. Either "file" or "dir".
            contents (:obj:`str`): If ``file_type == "file"`` this is the contents of the new file.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the file is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        data = DataObject()
        data.add_value_string("contents", contents)
        data.add_value_string("type", file_type)
        
        endpoint = APIAC + "/instance/{}/documentation/{}".format(instance, name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def get(self, instance, name=None):
        '''
        Get a file or directory from the API Access Control document root

        Args:
            instance (:obj:`str`): The name of the WebSEAL instance being configured.
            name (:obj:`str`): Name of file or directory.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the file or directory is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = APIAC + "/instance/{}/documentation/{}".format(instance, name)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self, instance):
        '''
        Get a list of all of the files and directories in the API Access Control document root.

        Args:
            instance (:obj:`str`): The name of the WebSEAL instance being configured.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the files are returned as JSON and can be accessed from
            the response.json attribute.
            
        '''
        endpoint = APIAC + "/instance/{}/documentation".format(instance)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response
