"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


PUSH_NOTIFICATION = "/iam/access/v8/push-notification"

logger = logging.getLogger(__name__)


class PushNotification(object):

    def __init__(self, base_url, username, password):
        super(PushNotification, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_provider(self, app_id=None, platform=None, provider_address=None,
            apple_key_store=None, apple_key_label=None,
            firebase_server_key=None):
        '''
        Create a push notification provider.

        Args:
            app_id (:obj:`str`): The application identifier associated with the registration.
            platform (:obj:`str`): The platform the registration is for.
            provider_address (:obj:`str`): The "host:port" address of the push notification service.
            apple_key_store (:obj:`str`, optional): The key store database containing the APNS certificate.
            apple_key_label (:obj:`str`, optional) The key label of the imported APNS certificate.
            firebase_server_key (:obj:`str`): The server key for access to the Firebase push notification service.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the push notification provider id is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        apple = DataObject()
        apple.add_value_string("key_store", apple_key_store)
        apple.add_value_string("key_label", apple_key_label)
        if apple.data:
            apple.add_value_string("provider_address", provider_address)

        firebase = DataObject()
        firebase.add_value_string("server_key", firebase_server_key)
        if firebase.data:
            firebase.add_value_string("provider_address", provider_address)

        provider = DataObject()
        provider.add_value_not_empty("apple", apple.data)
        provider.add_value_not_empty("firebase", firebase.data)

        data = DataObject()
        data.add_value_string("app_id", app_id)
        data.add_value_string("platform", platform)
        data.add_value_not_empty("provider", provider.data)

        response = self.client.post_json(PUSH_NOTIFICATION, data.data)
        response.success = response.status_code == 200

        return response


class PushNotification9021(PushNotification):

    def __init__(self, base_url, username, password):
        super(PushNotification9021, self).__init__(base_url, username, password)

    def list_providers(self):
        '''
        List the configured push notification service providers.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the push notification providers are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        response = self.client.get_json(PUSH_NOTIFICATION)
        response.success = response.status_code == 200

        return response

    def get_provider(self, pnr_id):
        '''
        Get a specific push notification provider.

        Args:
            pnr_id (:obj:`str`): The unique identifier for the push notification resource.
        
        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the push notification provider is returned as JSON and can be accessed from
            the response.json attribute.
        
        '''
        endpoint = '{}/{}'.format(PUSH_NOTIFICATION, pnr_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create_provider(self, app_id=None, platform=None, provider_address=None, apple_key_store=None, apple_key_label=None,
            firebase_server_key=None, imc_client_id=None, imc_client_secret=None, imc_refresh_token=None, imc_app_key=None):
        '''
        Create a push notification provider.

        Args:
            app_id (:obj:`str`): The application identifier associated with the registration.
            platform (:obj:`str`): The platform the registration is for.
            provider_address (:obj:`str`): The "host:port" address of the push notification service.
            apple_key_store (:obj:`str`, optional): The key store database containing the APNS certificate.
            apple_key_label (:obj:`str`, optional) The key label of the imported APNS certificate.
            firebase_server_key (:obj:`str`): The server key for access to the Firebase push notification service.
            imc_client_id (:obj:`str`, optional): The IBM Marketing Cloud issued Oauth client ID.
            imc_client_secret (:obj:`str`, optional): The IBM Marketing Cloud issued Oauth client secret.
            imc_refresh_token (:obj:`str`, optional): The IBM Marketing Cloud issued Oauth refresh token.
            imc_app_key (:obj:`str`, optional): The app key issued by IBM Marketing Cloud for the associated application.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the push notification provider uuid is returned as JSON and can be accessed from
            the response.json attribute

        '''
        apple = DataObject()
        apple.add_value_string("key_store", apple_key_store)
        apple.add_value_string("key_label", apple_key_label)
        if apple.data:
            apple.add_value_string("provider_address", provider_address)

        firebase = DataObject()
        firebase.add_value_string("server_key", firebase_server_key)
        if firebase.data:
            firebase.add_value_string("provider_address", provider_address)

        imc = DataObject()
        imc.add_value_string("client_id", imc_client_id)
        imc.add_value_string("client_secret", imc_client_secret)
        imc.add_value_string("refresh_token", imc_refresh_token)
        imc.add_value_string("app_key", imc_app_key)
        if imc.data:
            imc.add_value_string("provider_address", provider_address)

        provider = DataObject()
        provider.add_value_not_empty("apple", apple.data)
        provider.add_value_not_empty("firebase", firebase.data)
        provider.add_value_not_empty("imc", imc.data)

        data = DataObject()
        data.add_value_string("app_id", app_id)
        data.add_value_string("platform", platform)
        data.add_value_not_empty("provider", provider.data)

        response = self.client.post_json(PUSH_NOTIFICATION, data.data)
        response.success = response.status_code == 200

        return response


    def update_provider(self, pnr_id, app_id=None, platform=None, provider_address=None,
            apple_key_store=None, apple_key_label=None,
            firebase_server_key=None, imc_client_id=None,
            imc_client_secret=None, imc_refresh_token=None, imc_app_key=None):
        '''
        Update an existing a push notification provider.

        Args:
            pnr_id (:obj:`str`): The unique identifier for the push notification resource.
            app_id (:obj:`str`): The application identifier associated with the registration.
            platform (:obj:`str`): The platform the registration is for.
            provider_address (:obj:`str`): The "host:port" address of the push notification service.
            apple_key_store (:obj:`str`, optional): The key store database containing the APNS certificate.
            apple_key_label (:obj:`str`, optional) The key label of the imported APNS certificate.
            firebase_server_key (:obj:`str`): The server key for access to the Firebase push notification service.
            imc_client_id (:obj:`str`, optional): The IBM Marketing Cloud issued Oauth client ID.
            imc_client_secret (:obj:`str`, optional): The IBM Marketing Cloud issued Oauth client secret.
            imc_refresh_token (:obj:`str`, optional): The IBM Marketing Cloud issued Oauth refresh token.
            imc_app_key (:obj:`str`, optional): The app key issued by IBM Marketing Cloud for the associated application.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the push notification provider uuid is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        apple = DataObject()
        apple.add_value_string("key_store", apple_key_store)
        apple.add_value_string("key_label", apple_key_label)
        if apple.data:
            apple.add_value_string("provider_address", provider_address)

        firebase = DataObject()
        firebase.add_value_string("server_key", firebase_server_key)
        if firebase.data:
            firebase.add_value_string("provider_address", provider_address)

        imc = DataObject()
        imc.add_value_string("client_id", imc_client_id)
        imc.add_value_string("client_secret", imc_client_secret)
        imc.add_value_string("refresh_token", imc_refresh_token)
        imc.add_value_string("app_key", imc_app_key)
        if imc.data:
            imc.add_value_string("provider_address", provider_address)

        provider = DataObject()
        provider.add_value_not_empty("apple", apple.data)
        provider.add_value_not_empty("firebase", firebase.data)
        provider.add_value_not_empty("imc", imc.data)

        data = DataObject()
        data.add_value_string("app_id", app_id)
        data.add_value_string("platform", platform)
        data.add_value_not_empty("provider", provider.data)

        endpoint = PUSH_NOTIFICATION + '/{}'.format(pnr_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_provider(self, pnr_id):
        '''
        Delete an existing push notification provider.

        Args:
            pnr_id (:obj:`str`): The identifier for the push notification resource to be removed.
        
        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the push notification provider is returned as JSON and can be accessed from
            the response.json attribute.
        
        '''
        endpoint = '{}/{}'.format(PUSH_NOTIFICATION, pnr_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response