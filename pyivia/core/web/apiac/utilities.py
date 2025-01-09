"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

APIAC = "/wga/apiac"
CREDENTIALS = APIAC + "/credentials"
GROUPS = APIAC + "/groups"

class Utilities(object):

    def __init__(self, base_url, username, password):
        super(Utilities, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def store_credential(self, admin_id=None, admin_pwd=None, admin_domain=None):
        '''
        Cache a admin Verify Identity Access administrator credential.

        Args:
            admin_id (:obj:`str`): The Verify Identity Access administrator username.
            admin_pwd (:obj:`str`): The Verify Identity Access administrator password.
            admin_domain (:obj:`str`): The Verify Identity Access domain. If not specified the default value of "Default" will be used.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("admin_id", admin_id)
        data.add_value_string("admin_pwd", admin_pwd)
        data.add_value_string("admin_domain", admin_domain)

        response = self.client.post_json(CREDENTIALS, data.data)
        response.success = response.status_code == 200

        return response


    def delete_credential(self):
        '''
        Delete the cached Verify Identity Access administrator credential.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        response = self.client.delete_json(CREDENTIALS)
        response.success = response.status_code == 200

        return response


    def get_credential(self):
        '''
        Retrieve the stored Verify Identity Access credentials.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the list of credentials is returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = self.client.get_json(CREDENTIALS)
        response.success = response.status_code == 200

        return response


    def list_groups(self):
        '''
        Retrieve a list of all Verify Identity Access groups.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the list of groups is returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = self.client.get_json(GROUPS)
        response.success = response.status_code == 200

        return response
