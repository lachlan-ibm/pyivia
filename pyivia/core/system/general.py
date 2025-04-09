"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


NET_GENERAL = "/net/general"

logger = logging.getLogger(__name__)


class General(object):

    def __init__(self, base_url, username, password):
        super(General, self).__init__()
        self.client = RESTClient(base_url, username, password)
    
    def update_hostname(self, hostname):
        '''
        Update the hostname for an appliance based deployment.

        Args:
            hostname (:obj:`str`): System hostname.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        data = DataObject()
        data.add_value_string("hostName", hostname)

        response = self.client.put_json(NET_GENERAL, data.data)
        response.success = response.status_code == 200

        return response
    
    def get(self):
        '''
        Get General Network Configuration 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the system's general networking properties are returned 
            as JSON and can be accessed from the response.json attribute

        '''
        response = self.client.get_json(NET_GENERAL)
        response.success = response.status_code == 200

        return response