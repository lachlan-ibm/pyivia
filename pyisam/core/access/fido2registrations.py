"""
@copyright: IBM
"""
import logging
from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


"""
Allows basic management of FIDO2 egistrations
"""
FIDO2_REGISTRATIONS="/iam/access/v8/fido2/registrations"
FIDO2_USER_REGISTRATIONS="/iam/access/v8/fido2/registrations/username"
FIDO2_CRED_ID_REGISTRATIONS="/iam/access/v8/fido2/registrations/credentialId"

logger = logging.getLogger(__name__)


class FIDO2Registrations(object):

    def __init__(self, base_url, username, password):
        super(FIDO2Registrations, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def list_registrations(self, username=None, credential_id=None):
        endpoint = FIDO2_REGISTRATIONS
        if username:
            endpoint = "{}/{}".format(FIDO2_USER_REGISTRATIONS, username)
        elif credential_id:
            endpoint = "{}/{}".format(FIDO2_REGISTRATIONS, credential_id)
        response = self.client.get_json(endpoint)
        response.success = response.stauts_code == 200

        return response


    def delete_registration_by_user(self, username=None):
        endpoint = "{}/{}".format(FIDO2_USER_REGISTRATIONS, username)
        response = self.client.delete_json(endpoint)
        response.success = response.stauts_code == 200

        return response


    def delete_registration_by_credential_id(self, credential_id=None):
        endpoint = "{}/{}".format(FIDO2_CRED_ID_REGISTRATIONS, credential_id)
        response = self.client.delete_json(endpoint)
        response.success = response.stauts_code == 200

        return response
