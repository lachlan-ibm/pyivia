"""
@copyright: IBM
"""

import logging, json

from pyivia.util.model import Response
from pyivia.util.restclient import RESTClient

EXTENSIONS = "/extensions"

logger = logging.getLogger(__name__)


class Extensions(object):

    def __init__(self, base_url, username, password):
        super(Extensions, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_extension(self, ext_file=None, properties={}, third_party_packages=[]) -> Response:
        '''
        Create a new extension by installing an extension archive 
        from `IBM App-Xchange <https://exchange.xforce.ibmcloud.com/hub>`_.

        Args:
            ext_file (:obj:`str`): Path to file to upload as extension installer.
            properties (:obj:`dict`, optional): Optional set of configuration properties 
                            required by extension. Properties will change depending on the 
                            extension installed. This data is likely supposed to be a serialized 
                            JSON string.
            third_party_packages (:obj:`list` of :obj:`str`): List of file paths to be uploaded to 
                                                            the appliance during extension activation.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        response = Response()
        response.success = False
        if not ext_file:
            return response
        try:
            files = {"extension_support_package": open(ext_file, "rb")}
            endpoint = "{}/inspect".format(EXTENSIONS)
            response = self.client.post_file(endpoint, files=files, accept_type="*/*")
            response.success = response.status_code == 200
            if response.success == True:
                endpoint = "{}/activate".format(EXTENSIONS)
                tpp = []
                for third_party_package in third_party_packages:
                    tpp += [('third_party_package', open(third_party_package, "rb"))]
                params = {"config_data": json.dumps(properties).replace(", ", ",").replace(": ", ":")}
                response = self.client.post_file(endpoint, files=tpp, data=params, accept_type="*/*")
                response.success = response.status_code == 200
        except Exception as e:
            response.success = False
            response.data = str(e)
        return response


    def update_extension(self, ext_file=None, properties={}):
        '''
        Update an previously installed extension.

        Args:
            ext_file (:obj:`str`): Path to file to upload as extension installer.
            properties (:obj:`dict`, optional): Optional set of configuration properties required by extension. 
                                                Properties will change depending on the extension installed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

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
            :obj:`~requests.Response`: The response from verify identity access. 

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
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the installed extensions are returned as JSON and can be accessed from
            the response.json attribute
        '''
        endpoint = EXTENSIONS + "/{}".format(extension)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
