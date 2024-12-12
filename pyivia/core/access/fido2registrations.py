"""
@copyright: IBM
"""
import logging
from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


FIDO2_REGISTRATIONS="/iam/access/v8/fido2/registrations"
FIDO2_USER_REGISTRATIONS="/iam/access/v8/fido2/registrations/username"
FIDO2_CRED_ID_REGISTRATIONS="/iam/access/v8/fido2/registrations/credentialId"

logger = logging.getLogger(__name__)


class FIDO2Registrations(object):

    def __init__(self, base_url, username, password):
        super(FIDO2Registrations, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def list_registrations(self, username=None, credential_id=None):
        '''
        Get a list all of the known FIDO2 registrations.

        Args:
            username (:obj:`str`, optional): Specify a username to filter registrations by.
            credential_id (:obj:`str`): Specify a credential id to filter registrations by.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the FIDO2 registrations are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = FIDO2_REGISTRATIONS
        if username:
            endpoint = "{}/{}".format(FIDO2_USER_REGISTRATIONS, username)
        elif credential_id:
            endpoint = "{}/{}".format(FIDO2_REGISTRATIONS, credential_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def delete_registration_by_user(self, username=None):
        '''
        Remove all registrations associated with a username.

        Args:
            username (:obj:`str`): The username to remove registrations for.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "{}/{}".format(FIDO2_USER_REGISTRATIONS, username)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def delete_registration_by_credential_id(self, credential_id=None):
        '''
        Delete a registration associated with the specified credential id.

        Args:
            credential_id (:obj:`str`): The credential id to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "{}/{}".format(FIDO2_CRED_ID_REGISTRATIONS, credential_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get_registration(self, credential_id):
        '''
        Get a specific registration by credential id.

        Args:
            credential_id (:obj:`str`): The unique identifier for the authenticator.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the FIDO2 registration is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = "{}/{}".format(FIDO2_REGISTRATIONS, credential_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response