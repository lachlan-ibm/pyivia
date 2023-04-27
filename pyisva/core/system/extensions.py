"""
@copyright: IBM
"""

import logging

from pyisva.util.model import DataObject, Response
from pyisva.util.restclient import RESTClient

EXTENSIONS = "/extensions"

logger = logging.getLogger(__name__)


class Extensions(object):

    def __init__(self, base_url, username, password):
        super(Extensions, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_extension(self, ext_file=None, properties={}):
        '''
        Create a new extension by installing an extension archive from IBM App-Xchange.

        Args:
            ext_file (:obj:`str`): Path to file to upload as extension installer.
            properties (:obj:`dict`, optional): Optional set of configuration properties required by extension. Properties will change depending on the extension installed.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        files = {"extension_support_package": open(ext_file, "rb")}
        response = self.client.post_file(EXTENSIONS, files=files, parameters=properties)
        response.success = response.status_code == 200

        return response


    def update_extension(self, ext_file=None, properties={}):
        '''
        Update an previously installed extension.

        Args:
            ext_file (:obj:`str`): Path to file to upload as extension installer.
            properties (:obj:`dict`, optional): Optional set of configuration properties required by extension. Properties will change depending on the extension installed.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        files = None
        if ext_file:
            files = {"extension_support_package": open(ext_file, "rb")}
        response = self.client.put_file(EXTENSIONS, files=files, parameters=properties)
        response.success = response.status_code == 200

        return response


    def list_extensions(self):
        '''
        Get a list of the installed extensions.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the installed extensions are returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = self.client.get_json(EXTENSIONS)
        response.success = response.status_code == 200

        return response


    def delete_extension(self, extension):
        '''
        Delete an installed extension.

        Args:
            extension (:obj:`str`): The identifier of the extension to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the installed extensions are returned as JSON and can be accessed from
            the response.json attribute
        '''
        endpoint = EXTENSIONS + "/{}".format(extension)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
