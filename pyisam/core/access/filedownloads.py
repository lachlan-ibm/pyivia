"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

FILE_DOWNLOADS = "/isam/downloads"

logger = logging.getLogger(__name__)


class FileDownloads(object):

    def __init__(self, base_url, username, password):
        super(FileDownloads, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_file(self, path, file_name):
        '''
        Get a file from the hosted files of a Verify Access applaince.

        Args:
            path (:obj:`str`): The directory which contains the file to be downloaded.
            file_name (:obj:`str`): The file to be downloaded

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the file contents are returned as JSON and can be accessed from
            the response.json attribute
        '''
        endpoint = ("%s/%s/%s" % (FILE_DOWNLOADS, path, file_name))

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_directory(self, path, recursive=None):
        '''
        Get the contents of a directory from the hosted files of a Verify Access appliance.

        Args:
            path (:obj:`str`): The direcotry whcih contains the files to be downloaded.
            recursive (bool, optional): Return files in sub-direcotories of the path specified. Default is False.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the file contents are returned as JSON and can be accessed from
            the response.json attribute

        '''
        parameters = DataObject()
        parameters.add_value("recursive", recursive)

        endpoint = "%s/%s" % (FILE_DOWNLOADS, path)

        response = self.client.get_json(endpoint, parameters.data)
        response.success == response.status_code == 200

        if response.success and isinstance(response.json, dict):
            response.json = response.json.get("contents", [])

        return response
