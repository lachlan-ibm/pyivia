"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient

FILE_DOWNLOADS = "/isam/downloads"

logger = logging.getLogger(__name__)


class FileDownloads(object):

    def __init__(self, base_url, username, password):
        super(FileDownloads, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get(self, file_path, recursive=None):
        """
        Get a file from the "File Downloads" directory of an appliance

        Args:
            file_path (:obj:`str`): The relative path of the file to be retrieved. To get the contents of a directory
                            include the trailing '/'
            recursive (:obj:`str`, optional): Return the contents of sub-directories as well. Valid values are 'yes'
                            and 'no'.
        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the files are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = ("%s/%s" % (FILE_DOWNLOADS, file_path))

        response = Response()
        if file_path.ends_with('/'):
            if recursive:
                endpoint += "?recursive={}".format(recursive)
            response = self.client.get_json(endpoint)
        else:
            response = self.client.get(endpoint)
        response.success = response.status_code == 200

        return response


    def get_directory(self, path, recursive=None):
        '''
        Get the contents of a directory from the hosted files of a Verify Identity Access appliance.

        Args:
            path (:obj:`str`): The directory which contains the files to be downloaded.
            recursive (bool, optional): Return files in sub-directories of the path specified. Default is False.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the file contents are returned as JSON and can be accessed from
            the response.json attribute

        '''
        parameters = DataObject()
        parameters.add_value("recursive", recursive)

        endpoint = "%s/%s" % (FILE_DOWNLOADS, path)

        response = self.client.get_json(endpoint, parameters.data)
        response.success = response.status_code == 200

        if response.success and isinstance(response.json, dict):
            response.json = response.json.get("contents", [])

        return response

