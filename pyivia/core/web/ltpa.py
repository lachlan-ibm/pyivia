""""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

LTPA_KEY = "/wga/ltpa_key/"

class LTPA(object):

    def __init__(self, base_url, username, password):
        super(LTPA, self).__init__()
        self._client = RESTClient(base_url, username, password)

    def list_keyfiles(self):
        '''
        List the LTPA SSO keyfiles on the appliance.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the LTPA keyfile properties are returned as JSON and can be accessed from
            the response.json attribute
        '''
        response = self._client.get_json(LTPA_KEY)
        response.success = response.status_code == 200
        return response

    def export_keyfile(self, keyfile_id=None):
        '''
        Export a LTPA keyfile from IVIA. The contents of the file is retuned in the data property
        of the response.

        Args:
            keyfile_id (:obj:`str`): The LTPA key file to import. 
            keyfile_path (:obj:`str`): File path to export LTPA keyfile to.
        
        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful, the LTPA SSO file is returned as the data property
            of the response.
        '''
        response = self._client.get_json(f"{LTPA_KEY}/{keyfile_id}?export")
        response.success = response.status_code == 200
        return response

    def delete_keyfile(self, keyfile_id): 
        '''
        Delete a LTPA keyfile from IVIA.

        Args:
            keyfile_id (:obj:`str`): The LTPA key file to remove.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.
 
        '''
        response = self._client.delete_json(f"{LTPA_KEY}/{keyfile_id}")
        response.success = response.status_code == 200
        return response

    def import_keyfile(self, keyfile):
        '''
        Import the given file as a LTPA keyfile.

        Args:
            keyfile (:obj:`str`): The LTPA key file to import. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the LTPA keyfile id is returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = Response()
        try:
            files = {"ltpa_keyfile": open(keyfile, 'rb')}
            response = self._client.post_file(LTPA_KEY, files=files)
            response.success = response.status_code == 200

        except IOError as e:
            logger.error(e)
            response.success = False

        return response