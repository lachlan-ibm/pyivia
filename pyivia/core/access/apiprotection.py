"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


CLIENTS = "/iam/access/v8/clients"
DEFINITIONS = "/iam/access/v8/definitions"

logger = logging.getLogger(__name__)


class APIProtection(object):

    def __init__(self, base_url, username, password):
        super(APIProtection, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_client(self, name=None, redirect_uri=None, company_name=None, company_url=None, 
                    contact_person=None, contact_type=None, email=None, phone=None, other_info=None, 
                    definition=None, client_id=None, client_secret=None):
        '''
        Create an OIDC api protection client.

        Args:
            name (:obj:`str`): Name of the client.
            redirect_uri (:obj:`str`, optional): URL which client should redirect to.
            company_name (:obj:`str`, optional): Company to associate client with.
            company_url (:obj:`str`, optional): URL to associate client with.
            contact_person (:obj:`str`, optional): Person who is responsible for API client.
            contact_type (:obj:`str`, optional): Position of contact person.
            email (:obj:`str`, optional): Contact email address for client.
            phone (:obj:`str`, optional): Contact phone number for client.
            other_info (:obj:`str`, optional): Other contact details associated with client.
            definition (:obj:`str`): The id of the API protection definition to use.
            client_id (:obj:`str`): The id of the client.
            client_secret (:obj:`str`, optional): The client secret to use. If not specified then a public client is created.
            require_pkce_verification (bool, optional): Whether or not this client must perform proof of key exchange 
                                                        when performing an authorization code flow. Added in 9.0.4.0
            jwks_uri (:obj:`str`): URI which is the location that a clients published JWK set. Added in 9.0.4.0
            encryption_db (:obj:`str): The SSL database containing the JWT encryption key. Added in 9.0.4.0
            encryption_cert (:obj:`str`): The certificate label of the JWT encryption key. Added in 9.0.4.0
            introspect_with_secret (bool, optional): Whether or not the client secret is required when 
                                                     performing an introspection request with this client. Added in 10.0.3.0.
            exts (:obj:`dict`, optional): Optional JSON dictionary of advanced configuration properties for the client.
                                          Added in 10.0.3.0.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created API client can be accessed from the 
            response.id_from_location attribute.

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("redirectUri", redirect_uri)
        data.add_value_string("companyName", company_name)
        data.add_value_string("companyUrl", company_url)
        data.add_value_string("contactPerson", contact_person)
        data.add_value_string("contactType", contact_type)
        data.add_value_string("email", email)
        data.add_value_string("phone", phone)
        data.add_value_string("otherInfo", other_info)
        data.add_value_string("definition", definition)
        data.add_value_string("clientId", client_id)
        data.add_value_string("clientSecret", client_secret)

        response = self.client.post_json(CLIENTS, data.data)
        response.success = response.status_code == 201

        return response


    def update_client(self, id=None, name=None, redirect_uri=None, company_name=None, company_url=None, 
                    contact_person=None, contact_type=None, email=None, phone=None, other_info=None, 
                    definition=None, client_id=None, client_secret=None):
        '''
        Update an OIDC API protection client.

        Args:
            name (:obj:`str`): Name of the client.
            redirect_uri (:obj:`str`, optional): URL which client should redirect to.
            company_name (:obj:`str`, optional): Company to associate client with.
            company_url (:obj:`str`, optional): URL to associate client with.
            contact_person (:obj:`str`, optional): Person who is responsible for API client.
            contact_type (:obj:`str`, optional): Position of contact person.
            email (:obj:`str`, optional): Contact email address for client.
            phone (:obj:`str`, optional): Contact phone number for client.
            other_info (:obj:`str`, optional): Other contact details associated with client.
            definition (:obj:`str`): The id of the API protection definition to use.
            client_id (:obj:`str`): The id of the client.
            client_secret (:obj:`str`, optional): The client secret to use. If not specified then a public client is created.
            require_pkce_verification (bool, optional): Whether or not this client must perform proof of key exchange 
                                                        when performing an authorization code flow. Added in 9.0.4.0
            jwks_uri (:obj:`str`): URI which is the location that a clients published JWK set. Added in 9.0.4.0
            encryption_db (:obj:`str): The SSL database containing the JWT encryption key. Added in 9.0.4.0
            encryption_cert (:obj:`str`): The certificate label of the JWT encryption key. Added in 9.0.4.0
            introspect_with_secret (bool, optional): Whether or not the client secret is required when 
                                                     performing an introspection request with this client. Added in 10.0.3.0.
            exts (:obj:`dict`, optional): Optional JSON dictionary of advanced configuration properties for the client.
                                          Added in 10.0.3.0.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("redirectUri", redirect_uri)
        data.add_value("companyName", company_name)
        data.add_value_string("companyUrl", company_url)
        data.add_value_string("contactPerson", contact_person)
        data.add_value_string("contactType", contact_type)
        data.add_value_string("email", email)
        data.add_value_string("phone", phone)
        data.add_value_string("otherInfo", other_info)
        data.add_value_string("definition", definition)
        data.add_value_string("clientId", client_id)
        data.add_value_string("clientSecret", client_secret)

        endpoint = "{}/{}".format(CLIENTS, id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete_client(self, id):
        '''
        Delete an OIDC API protection client.

        Args:
            id (:obj:`str`): The id of the client to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = "%s/%s" % (CLIENTS, id)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def list_clients(self, sort_by=None, count=None, start=None, filter=None):
        '''
        Get a list of API clients.

        Args:
            sort_by (:obj:`str`, optional): Attribute to sort results by.
            count (:obj:`str`, optional): Maximum number of results to fetch.
            start (:obj:`str`, optional): Pagination offset of returned results.
            filter (:obj:`str`): Attribute to filter results by

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the API clients are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("count", count)
        parameters.add_value_string("start", start)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(CLIENTS, parameters.data)
        response.success = response.status_code == 200

        return response


    def create_definition(self, name=None, description=None, tcm_behavior=None, token_char_set=None, access_token_lifetime=None,
            access_token_length=None, authorization_code_lifetime=None, authorization_code_length=None, refresh_token_length=None,
            max_authorization_grant_lifetime=None, pin_length=None, enforce_single_use_authorization_grant=None,
            issue_refresh_token=None, enforce_single_access_token_per_grant=None, enable_multiple_refresh_tokens_for_fault_tolerance=None,
            pin_policy_enabled=None, grant_types=None):
        '''
        Create an OIDC API Protection definition. Definitions can be used to configure one or more clients.

        Args:
            name (:obj:`str`): Name of the OIDC definition.
            description (:obj:`str`, optional): Description of the OIDC definition.
            tcm_behavior (:obj:`str`, optional): Specify the Trust Client Manager's behavior.
            token_char_set (:obj:`str`, optional): Specify the allowed characters for generated tokens. Default is alphanumeric set of characters.
            access_token_lifetime (int, optional): Length of time that access token is valid for.
            authorization_code_lifetime (int, optional): Length of time that authorization code is valid for.
            authorization_code_length (int, optional): Number of characters used to generate authorization code.
            refresh_token_length (int, optional): Number of characters used to generate refresh tokens.
            max_authorization_grant_lifetime (int, optional): The maximum duration of a grant, in seconds, where the resource owner authorized the client to access the protected resource.
            pin_length (int, optional): Length of PIN used to protect refresh token.
            enforce_single_use_authorization_grant (bool, optional): True if all tokens of the authorization grant should be revoked after an access token is validated.
            issue_refresh_token (bool, optional): True if a refresh token should be issued to the client.
            enforce_single_access_token_per_grant (bool, optional): True if previously granted access tokens should be revoked after a new access token is generated via a refresh token.
            enable_multiple_refresh_tokens_for_fault_tolerance (bool, optional): True if multiple refresh tokens are stored so that the old refresh token is valid until the new refresh token is successfully delivered.
            pin_policy_enabled (bool, optional): True if the refresh token will be further protected with a PIN provided by the API protection client.
            grant_types (:obj:`list` of :obj:`str`): A list of supported authorization grant types.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created OIDC definition can be accessed from the 
            response.id_from_location attribute

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("tcmBehavior", tcm_behavior)
        data.add_value_string("tokenCharSet", token_char_set)
        data.add_value("accessTokenLifetime", access_token_lifetime)
        data.add_value("accessTokenLength", access_token_length)
        data.add_value("authorizationCodeLifetime", authorization_code_lifetime)
        data.add_value("authorizationCodeLength", authorization_code_length)
        data.add_value("refreshTokenLength", refresh_token_length)
        data.add_value(
            "maxAuthorizationGrantLifetime", max_authorization_grant_lifetime)
        data.add_value("pinLength", pin_length)
        data.add_value(
            "enforceSingleUseAuthorizationGrant",
            enforce_single_use_authorization_grant)
        data.add_value("issueRefreshToken", issue_refresh_token)
        data.add_value(
            "enforceSingleAccessTokenPerGrant",
            enforce_single_access_token_per_grant)
        data.add_value(
            "enableMultipleRefreshTokensForFaultTolerance",
            enable_multiple_refresh_tokens_for_fault_tolerance)
        data.add_value("pinPolicyEnabled", pin_policy_enabled)
        data.add_value("grantTypes", grant_types)

        response = self.client.post_json(DEFINITIONS, data.data)
        response.success = response.status_code == 201

        return response


    def update_definition(self, definition_id=None, name=None, description=None, tcm_behavior=None,
            token_char_set=None, access_token_lifetime=None, access_token_length=None, authorization_code_lifetime=None,
            authorization_code_length=None, refresh_token_length=None, max_authorization_grant_lifetime=None, 
            pin_length=None, enforce_single_use_authorization_grant=None, issue_refresh_token=None,
            enforce_single_access_token_per_grant=None, enable_multiple_refresh_tokens_for_fault_tolerance=None,
            pin_policy_enabled=None, grant_types=None, oidc_enabled=False, iss=None, poc=None, lifetime=None, alg=None, 
            db=None, cert=None, enc_enabled=False, enc_alg=None, enc_db=None, enc_cert=None, enc_enc=None, access_policy_id=None):
        '''
        Update an OIDC API Protection definition. Definitions can be used to configure one or more clients.

        Args:
            name (:obj:`str`): Name of the OIDC definition.
            description (:obj:`str`, optional): Description of the OIDC definition.
            tcm_behavior (:obj:`str`, optional): Specify the Trust Client Manager's behavior.
            token_char_set (:obj:`str`, optional): Specify the allowed characters for generated tokens. Default is alphanumeric set
            access_token_lifetime (int, optional): Length of time that access token is valid for.
            authorization_code_lifetime (int, optional): Length of time that authorization code is valid for.
            authorization_code_length (int, optional): Number of characters used to generate authorization code.
            refresh_token_length (int, optional): Number of characters used to generate refresh tokens.
            max_authorization_grant_lifetime (int, optional): The maximum duration of a grant, in seconds, where the resource owner authorized the client to access the protected resource.
            pin_length (int, optional): Length of PIN used to protect refresh token.
            enforce_single_use_authorization_grant (bool, optional): True if all tokens of the authorization grant should be revoked after an access token is validated.
            issue_refresh_token (bool, optional): True if a refresh token should be issued to the client.
            enforce_single_access_token_per_grant (bool, optional): True if previously granted access tokens should be revoked after a new access token is generated via a refresh token.
            enable_multiple_refresh_tokens_for_fault_tolerance (bool, optional): True if multiple refresh tokens are stored so that the old refresh token is valid until the new refresh token is successfully delivered.
            pin_policy_enabled (bool, optional): True if the refresh token will be further protected with a PIN provided by the API protection client.
            grant_types (:obj:`list` of :obj:`str`): A list of supported authorization grant types.
            oidc_enabled (bool, optional): If OpenID Connect is enabled for this definition.
            iss (:obj:`str`): The issuer identifier of this definition.
            poc (:obj:`str`): The Point of Contact URL for this definition.
            lifetime (int): The lifetime of the id_tokens issued.
            alg (:obj:`str`): The signing algorithm for the JWT.
            db (:obj:`str`): The SSL database containing the signing key for RS/ES signing methods.
            cert (:obj:`str`): The certificate label of the signing key for RS/ES signing methods.
            enc_enabled (bool): Is encryption enabled for this definition.
            enc_alg (:obj:`str`): The key agreement algorithm for encryption.
            enc_enc (:obj:`str`): The encryption algorithm.
            access_policy_id (int): The id of access policy assigned to this definition.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("tcmBehavior", tcm_behavior)
        data.add_value_string("tokenCharSet", token_char_set)
        data.add_value("accessTokenLifetime", access_token_lifetime)
        data.add_value("accessTokenLength", access_token_length)
        data.add_value("authorizationCodeLifetime", authorization_code_lifetime)
        data.add_value("authorizationCodeLength", authorization_code_length)
        data.add_value("refreshTokenLength", refresh_token_length)
        data.add_value(
            "maxAuthorizationGrantLifetime", max_authorization_grant_lifetime)
        data.add_value("pinLength", pin_length)
        data.add_value(
            "enforceSingleUseAuthorizationGrant",
            enforce_single_use_authorization_grant)
        data.add_value("issueRefreshToken", issue_refresh_token)
        data.add_value(
            "enforceSingleAccessTokenPerGrant",
            enforce_single_access_token_per_grant)
        data.add_value(
            "enableMultipleRefreshTokensForFaultTolerance",
            enable_multiple_refresh_tokens_for_fault_tolerance)
        data.add_value("pinPolicyEnabled", pin_policy_enabled)
        data.add_value("grantTypes", grant_types)
        data.add_value("accessPolicyId", access_policy_id)
        
        if oidc_enabled:
            oidc = DataObject()
            oidc.add_value("enabled",True)
            oidc.add_value("iss",iss)
            oidc.add_value("poc",poc)
            oidc.add_value("lifetime",lifetime)
            oidc.add_value("alg",alg)
            oidc.add_value("db",db)
            oidc.add_value("cert",cert)
            enc_data = DataObject()
            enc_data.add_value_boolean("enabled", enc_enabled)
            if enc_enabled:
                enc_data.add_value("alg",enc_alg)
                enc_data.add_value("enc",enc_enc)
            oidc.add_value("enc",enc_data.data)

            data.add_value("oidc",oidc.data)

        response = self.client.put_json(DEFINITIONS+"/"+str(definition_id), data.data)
        response.success = response.status_code == 204

        return response


    def delete_definition(self, id):
        '''
        Remove an OIDC API protection definition.

        Args:
            id (:obj:`str`): the id of the definition to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "%s/%s" % (DEFINITIONS, id)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def list_definitions(self, sort_by=None, count=None, start=None, filter=None):
        '''
        Get a list of the configured API protection definitions.

        Args:
            sort_by (:obj:`str`, optional): Attribute to sort results by.
            count (:obj:`str`, optional): Maximum number of results to fetch.
            start (:obj:`str`, optional): Pagination offset of returned results.
            filter (:obj:`str`): Attribute to filter results by.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the OIDC definitions are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("count", count)
        parameters.add_value_string("start", start)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(DEFINITIONS, parameters.data)
        response.success = response.status_code == 200

        return response


class APIProtection9040(APIProtection):

    def __init__(self, base_url, username, password):
        super(APIProtection, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_valid_grant_types(self):
        return ["AUTHORIZATION_CODE","RESOURCE_OWNER_PASSWORD_CREDENTIALS","IMPLICIT_GRANT", "CLIENT_CREDENTIALS", "JWT_BEARER", "SAML_BEARER"]

    def create_definition(self, name=None, description=None, tcm_behavior=None, token_char_set=None, access_token_lifetime=None,
            access_token_length=None, authorization_code_lifetime=None, authorization_code_length=None, refresh_token_length=None,
            max_authorization_grant_lifetime=None, pin_length=None, enforce_single_use_authorization_grant=None,
            issue_refresh_token=None, enforce_single_access_token_per_grant=None,
            enable_multiple_refresh_tokens_for_fault_tolerance=None, pin_policy_enabled=None, grant_types=None, oidc_enabled=False,
            iss=None, poc=None, lifetime=None, alg=None, db=None, cert=None, enc_enabled=False, enc_alg=None, enc_enc=None, 
            access_policy_id=None, attribute_sources=[]):

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("tcmBehavior", tcm_behavior)
        data.add_value_string("tokenCharSet", token_char_set)
        data.add_value("accessTokenLifetime", access_token_lifetime)
        data.add_value("accessTokenLength", access_token_length)
        data.add_value("authorizationCodeLifetime", authorization_code_lifetime)
        data.add_value("authorizationCodeLength", authorization_code_length)
        data.add_value("refreshTokenLength", refresh_token_length)
        data.add_value(
            "maxAuthorizationGrantLifetime", max_authorization_grant_lifetime)
        data.add_value("pinLength", pin_length)
        data.add_value_boolean(
            "enforceSingleUseAuthorizationGrant",
            enforce_single_use_authorization_grant)
        data.add_value_boolean("issueRefreshToken", issue_refresh_token)
        data.add_value_boolean(
            "enforceSingleAccessTokenPerGrant",
            enforce_single_access_token_per_grant)
        data.add_value_boolean(
            "enableMultipleRefreshTokensForFaultTolerance",
            enable_multiple_refresh_tokens_for_fault_tolerance)
        data.add_value_boolean("pinPolicyEnabled", pin_policy_enabled)
        data.add_value("grantTypes", grant_types)
        data.add_value("accessPolicyId", access_policy_id)

        if oidc_enabled:
            oidc = DataObject()
            oidc.add_value_boolean("enabled",True)
            oidc.add_value("iss",iss)
            oidc.add_value("poc",poc)
            oidc.add_value("lifetime",lifetime)
            oidc.add_value("alg",alg)
            oidc.add_value("db",db)
            oidc.add_value("cert",cert)
            if enc_enabled:
                enc_data = DataObject()
                enc_data.add_value_boolean("enabled",True)
                enc_data.add_value("alg",enc_alg)
                enc_data.add_value("enc",enc_enc)
                oidc.add_value("enc",enc_data.data)
            oidc.add_value_not_empty("attributeSources", attribute_sources)
            data.add_value("oidc", oidc.data)
        
        response = self.client.post_json(DEFINITIONS, data.data)
        response.success = response.status_code == 201

        return response


    def create_client(self, name=None, redirect_uri=None, company_name=None, company_url=None, contact_person=None, 
            contact_type=None, email=None, phone=None, other_info=None, definition=None, client_id=None, 
            client_secret=None, require_pkce_verification=None, jwks_uri=None, encryption_db=None, encryption_cert=None):

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value("redirectUri", redirect_uri)
        data.add_value_string("companyName", company_name)
        data.add_value_string("companyUrl", company_url)
        data.add_value_string("contactPerson", contact_person)
        data.add_value_string("contactType", contact_type)
        data.add_value_string("email", email)
        data.add_value_string("phone", phone)
        data.add_value_string("otherInfo", other_info)
        data.add_value_string("definition", definition)
        data.add_value_string("clientId", client_id)
        data.add_value_string("clientSecret", client_secret)
        data.add_value_boolean("requirePkce", require_pkce_verification)
        data.add_value_string("jwksUri", jwks_uri)
        data.add_value_string("encryptionDb", encryption_db)
        data.add_value_string("encryptionCert", encryption_cert)

        response = self.client.post_json(CLIENTS, data.data)
        response.success = response.status_code == 201

        return response

class APIProtection10030(APIProtection9040):

    def create_client(self, name=None, redirect_uri=None, company_name=None, company_url=None, contact_person=None, 
            contact_type=None, email=None, phone=None, other_info=None, definition=None, client_id=None, 
            client_secret=None, require_pkce_verification=None, jwks_uri=None, encryption_db=None, encryption_cert=None,
            introspect_with_secret=None, exts=None):

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value("redirectUri", redirect_uri)
        data.add_value_string("companyName", company_name)
        data.add_value_string("companyUrl", company_url)
        data.add_value_string("contactPerson", contact_person)
        data.add_value_string("contactType", contact_type)
        data.add_value_string("email", email)
        data.add_value_string("phone", phone)
        data.add_value_string("otherInfo", other_info)
        data.add_value_string("definition", definition)
        data.add_value_string("clientId", client_id)
        data.add_value_string("clientSecret", client_secret)
        data.add_value_boolean("requirePkce", require_pkce_verification)
        data.add_value_string("jwksUri", jwks_uri)
        data.add_value_string("encryptionDb", encryption_db)
        data.add_value_string("encryptionCert", encryption_cert)
        data.add_value_boolean("introspectWithSecret", introspect_with_secret)
        data.add_value("extProperties", exts)

        response = self.client.post_json(CLIENTS, data.data)
        response.success = response.status_code == 201

        return response

