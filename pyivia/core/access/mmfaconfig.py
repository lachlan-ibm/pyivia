"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


MMFA_CONFIG = "/iam/access/v8/mmfa-config"

logger = logging.getLogger(__name__)


class MMFAConfig(object):

    def __init__(self, base_url, username, password):
        super(MMFAConfig, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def update(self, client_id=None, hostname=None, junction=None, options=None,
            port=None):
        '''
        Update the mobile multi-factor authentication (MMFA) configuration.

        Args:
            client_id (:obj:`str`): The id of the Open-Id Connect client to use.
            hostname (:obj:`str`): The hostname of the WebSEAL instance configured for MMFA.
            junction (:obj:`astr`): The junction prefix configured for MMFA.
            options (:obj:`str`): A list of configurable key-value pairs to be presented in the QR code.
            port (:obj:`str`): The port the MMFA endpoint is listening on.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("client_id", client_id)
        data.add_value_string("hostname", hostname)
        data.add_value_string("junction", junction)
        data.add_value_string("options", options)
        data.add_value("port", port)

        response = self.client.post_json(MMFA_CONFIG, data.data)
        response.success = response.status_code == 204

        return response


class MMFAConfig9021(MMFAConfig):

    def __init__(self, base_url, username, password):
        super(MMFAConfig9021, self).__init__(base_url, username, password)


    def update(self, client_id=None, hostname=None, junction=None, options=None, port=None,
            details_url=None, enrollment_endpoint=None,
            hotp_shared_secret_endpoint=None, totp_shared_secret_endpoint=None,
            token_endpoint=None, authntrxn_endpoint=None,
            mobile_endpoint_prefix=None, qrlogin_endpoint=None,
            discovery_mechanisms=[],):
        '''
        Update the mobile multi-factor authentication (MMFA) configuration.

        Args:
            client_id (:obj:`str`): The id of the OIDC client to use.
            hostname (:obj:`str`, optional): The hostname of the WebSEAL instance configured for MMFA.
            junction (:obj:`str`, optional): The junction prefix configured for MMFA.
            port (int, optional): The port the MMFA endpoint is listening on.
            hotp_shared_secret_endpoint (:obj:`str`): The HOTP shared secret endpoint returned from the discovery endpoint.
            totp_shared_secret_endpoint (:obj:`str`): The TOTP shared secret endpoint returned from the discovery endpoint.
            token_endpoint (:obj:`str`): The OAuth token endpoint returned from the discovery endpoint.
            authntrxn_endpoint (:obj:`str`): The SCIM Transaction endpoint returned from the discovery endpoint.
            mobile_endpoint_prefix (:obj:`str`): The prefix of the runtime endpoint that is constructed and saved as the request URL of a transaction. 
            qrlogin_endpoint (:obj:`str`): The QR Code login endpoint returned from the discovery endpoint.
            discovery_mechanisms (:obj:`list` of :obj:`str`): A list of authentication mechanism URIs to be included in the discovery endpoint response.
            options (:obj:`str`): A list of configurable key-value pairs to be presented in the QR code.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoints = DataObject()
        endpoints.add_value_string("details_url", details_url)
        endpoints.add_value_string("enrollment_endpoint", enrollment_endpoint)
        endpoints.add_value_string(
            "hotp_shared_secret_endpoint",hotp_shared_secret_endpoint)
        endpoints.add_value_string(
            "totp_shared_secret_endpoint",totp_shared_secret_endpoint)
        endpoints.add_value_string("token_endpoint", token_endpoint)
        endpoints.add_value_string("authntrxn_endpoint", authntrxn_endpoint)
        endpoints.add_value_string(
            "mobile_endpoint_prefix", mobile_endpoint_prefix)
        endpoints.add_value_string("qrlogin_endpoint", qrlogin_endpoint)

        data = DataObject()
        data.add_value_string("client_id", client_id)
        data.add_value_string("hostname", hostname)
        data.add_value_string("junction", junction)
        data.add_value_string("options", options)
        data.add_value("port", port)
        data.add_value_not_empty("endpoints", endpoints.data)
        data.add_value_not_empty("discovery_mechanisms", discovery_mechanisms)

        response = self.client.post_json(MMFA_CONFIG, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self):
        '''
        Delete the mobile multi-factor authentication configuration.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        response = self.client.delete_json(MMFA_CONFIG)
        response.success = response.status_code == 204

        return response