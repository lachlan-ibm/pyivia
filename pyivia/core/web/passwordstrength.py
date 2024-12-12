""""
@copyright: IBM
"""

import logging
import urllib

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

PASSWORD_STRENGTH = "/wga/pwd_strength"

class PasswordStrength(object):

    def __init__(self, base_url, username, password):
        super(PasswordStrength, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, content=None):
        '''
        Create a Password Strength rule.

        Args:
            name (:obj:`str`): The name of the rule to be created.
            content (:obj:`str`): The contents of the password rule in plaintext format.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the kerberos subsection/property is returned as JSON and can be accessed from  
            the response.json attribute 
        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_not_empty("content", content)

        response = self.client.post_json(PASSWORD_STRENGTH, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, name=None, new_name=None, content=None):
        '''
        Update a Password Strength rule. This can be used to update a password strength file name or modify the
        contents of a rule.

        Args:
            name (:obj:`str`): The name of the rule to be updated.
            new_name (:obj:`str`, optional): The new name of the password rule file.
            content (:obj:`str`, optional): The new contents of the password rule in plaintext format.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the kerberos subsection/property is returned as JSON and can be accessed from  
            the response.json attribute 
        '''
        data = DataObject()
        data.add_value("content", content)
        data.add_value("new_name", new_name)

        endpoint = PASSWORD_STRENGTH + "/{}".format(name)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete(self, name=None):
        '''
        Delete a Password Strength rule.

        Args:
            name (:obj:`str`): The name of the rule to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the kerberos subsection/property is returned as JSON and can be accessed from  
            the response.json attribute 
        '''
        endpoint = PASSWORD_STRENGTH + "/{}".format(name)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get(self, name=None):
        '''
        Get a Password Strength rule.

        Args:
            name (:obj:`str`): The name of the rule to be updated.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the kerberos subsection/property is returned as JSON and can be accessed from  
            the response.json attribute 
        '''
        endpoint = PASSWORD_STRENGTH + "/{}".format(name)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        Return a list of the names of the configured password strength rules.

        Args:
            name (:obj:`str`): The name of the rule to be updated.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the kerberos subsection/property is returned as JSON and can be accessed from  
            the response.json attribute 
        '''
        response = self.client.get_json(PASSWORD_STRENGTH)
        response.success = response.status_code == 200

        return response
