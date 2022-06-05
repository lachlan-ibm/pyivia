"""
@copyright: IBM
"""

import logging
import uuid
import json

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

FEDERATIONS = "/iam/access/v8/federations/"

logger = logging.getLogger(__name__)

class Federations(object):

    def __init__(self, base_url, username, password):
        super(Federations, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_oidc_federation(self, name=None, role=None, redirect_uri_prefix=None, response_types_supported=None, 
            attribute_mappings=None, identity_delegate_id=None, identity_rule_type="JAVASCRIPT", identity_mapping_rule=None, 
            identity_applies_to=None, identity_auth_type=None, identity_ba_user=None, identity_ba_password=None,
            identity_client_keystore=None, identity_client_key_alias=None, identity_issuer_uri=None, 
            identity_message_format=None, identity_ssl_keystore=None, identity_uri=None, adv_delegate_id=None,
            adv_rule_type="JAVASCRIPT", adv_mapping_rule=None):
        """
        Create an OIDC Federation.

        Args:
            name (:obj:`str`): 	A meaningful name to identify this federation.
            role (:obj:`str`): The role of a federation, valid values are "ip", "sp", "op" and "rp".
            response_types_supported (:obj:`str`): 
            attribute_mappings (:obj:`list` of :obj:`dict`): The attribute mapping data. format is:
                            `[{"name":"email","source":"ldap_email"},{"mobile":"source":"ldap_phone"}]`
            identity_delegate_id (:obj:`str`): The active mapping module instance.
            identity_rule_type (:obj:`str`): The type of the mapping rule. The only supported type currently is JAVASCRIPT.
            identity_mapping_rule (:obj:`str`): A reference to an ID of an identity mapping rule. 
            identity_applies_to (:obj:`str`): Refers to STS chain that consumes callout response. Required if WSTRUST 
                            messageFormat is specified, ignored otherwise.
            identity_auth_type (:obj:`str`): Authentication method used when contacting external service. Supported 
                            values are NONE, BASIC or CERTIFICATE.
            identity_ba_user (:obj:`str`): Username for authentication to external service. Required if BASIC authType 
                            is specified, ignored otherwise.
            identity_ba_password (:obj:`str`): Password for authentication to external service. Required if BASIC 
                            authType is specified, ignored otherwise.
            identity_client_keystore (:obj:`str`): Contains key for HTTPS client authentication. Required if CERTIFICATE 
                            authType is specified, ignored otherwise.
            identity_client_key_alias (:obj:`str`): Alias of the key for HTTPS client authentication. Required if 
                            CERTIFICATE authType is specified, ignored otherwise.
            identity_issuer_uri (:obj:`str`): Refers to STS chain that provides input for callout request. Required if 
                            WSTRUST messageFormat is specified, ignored otherwise.
            identity_message_format (:obj:`str`): Message format of callout request. Supported values are XML or WSTRUST.
            identity_ssl_keystore (:obj:`str`): SSL certificate trust store to use when validating SSL certificate of 
                            external service.
            identity_uri (:obj:`str`): Address of destination server to call out to. 
            adv_delegate_id (:obj:`str`): The active module instance. Valid values are "skip-advance-map" and "default-map".
            adv_rule_type (:obj:`str`): The type of the mapping rule. The only supported type currently is JAVASCRIPT.
            adv_mapping_rule (:obj:`str`): A reference to an ID of an advance configuration mapping rule.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created obligation can be acess from the
            response.id_from_location attribute

        """
        attributeMapping = DataObject()
        attributeMapping.add_value_not_empty("map", attribute_mappings)

        advConfig = DataObject()
        advConfig.add_value_string("activeDelegateId", adv_delegate_id)
        advConfigProps = DataObject()
        advConfigProps.add_value_string("ruleType", adv_rule_type)
        advConfigProps.add_vaule_string("advanceMappingRuleReference", adv_mapping_rule)
        advConfig.add_value_not_empty("properties", advConfigProps.data)

        identityMapping = DataObject()
        identityMapping.add_value_string("activeDelegateId", identity_delegate_id)
        properties = DataObject()
        if identity_delegate_id == "default-map":
            properties.add_value_string("ruleType", identity_rule_type)
            properties.add_value_string("identityMappingRuleReference", identity_mapping_rule_reference)

        elif identity_delegate_id == "default-http-custom-map":
            properties.add_value_string("appliesTo", identity_applies_to)
            properties.add_value_string("authType", identity_auth_type)
            properties.add_value_string("basicAuthUsername", identity_ba_user)
            properties.add_value_string("basicAuthPassword", identity_ba_password)
            properties.add_value_string("clientKeyStore", identity_client_keystore)
            properties.add_value_string("clientKeyAlias", identity_client_key_alias)
            properties.add_value_string("issuerUri", identity_issuer_uri)
            properties.add_value_string("messageFormat", identity_message_format)
            properties.add_value_string("sslKeyStore", identity_ssl_keystore)
            properties.add_value_string("uri", identity_uri)
        identityMapping.add_value_not_empty("properties", properties.data)

        configuration = DataObject()
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)
        configuration.add_value_not_empty("advancedConfiguration", advConfig.data)
        configuration.add_value_string("redirectUriPrefix", redirect_uri_prefix)
        configuration.add_value_string("responseTypes", response_types_supported)

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("protocol", "OIDC")
        data.add_value_string("role", role)
        data.add_value_not_empty("configuration", configuration.data)

        response = self.client.post_json(FEDERATIONS, data.data)
        response.success = response.status_code == 201

        return response

    def create_oidc_partner(self, federation_id, name=None, enabled=False, role="rp", template_name=None, client_id=None, 
        client_secret="", active_delegate_id=None, metadata_endpoint_url=None, issuer_identifier=None, response_types=[],
        authorization_endpoint=None, token_endpoint=None, user_info_endpoint=None, signature_alg=None, 
        verification_keystore=None, verification_key_label=None, jwk_endopoint_url=None, key_mgmt_alg=None, 
        content_encrypt_alg=None, decrypt_keystore=None, decrypt_key_label=None, scope=[], perform_user_info=None, 
        token_endpoint_auth_method=None, attribute_mapping=None, identity_delegate_id=None, identity_mapping_rule=None,
        identity_auth_type=None, identity_ba_user=None, identity_ba_password=None, identity_client_keystore=None, 
        identity_client_key_alias=None, identity_issuer_uri=None, identity_msg_fmt=None, identity_ssl_keystore=None,
        identity_uri=None, adv_config_delegate_id=None, adv_config_rule_type="JAVASCRIPT", adv_config_mapping_rule=None):
        """
        Add a partner configuration to an ODIC RP.

        Args:
            federation_id (:obj:`str`): The id of the ODIC federation to create a partner for.
            name (:obj:`str`): THe name o the partner to be created.
            enabled (:obj:`str`): Whether to enable the partner.
            role (:obj:`str`, optional): The role this partner plays in its federation. Default is "rp"
            template_name (:obj:`str`): An identifier for the template on which to base this partner.
            client_id (:obj:`str`): The id that identifies this client to the provider.
            client_secret(:obj:`str`, optional): The secret associated with the client ID. Set as "" if using a public 
                            client.
            active_delegate_id (:obj:`str`): The active module instance. Valid values are "noMetadata" and "metadataEndpointUrl".
            metadata_endpoint (:obj:`str`, optional): The /metadata endpoint URL of the provider.
            issuer_identifier (:obj:`str`, optional): The issuer ("iss") value of the provider.
            response_types (:obj:`str`, optional): List of response type which determines which flow to be executed.
            authorization_endpoint (:obj:`str`, optional): The /authorize endpoint URL of the provider.
            token_endpoint (:obj:`str`, optional): The /token endpoint URL of the provider. Required if "code" response 
                            type is selected.
            user_info_endpoint (:obj:`str`, optional): The /userinfo endpoint URL of the provider.
            signature_alg (:obj:`str`, optional): The signing algorithm to use. Supported values are "none", "HS256", 
                            "HS384", "HS512", "RS256", "RS384", "RS512", "ES256", "ES384", "ES512", "PS256", "PS384", 
                            "PS512". Default is none.
            verification_keystore (:obj:`str`, optional): When signature algorithm requires a certificate, the keystore 
                            which contains the selected certificate to perform the signing.
            verification_key_label (:obj:`str`, optional): When signature algorithm requires a certificate, the alias 
                            of the public key in the selected keystore to use in signature verification.
            jwk_endopoint_url (:obj:`str`): When signature algorithm requires a certificate, the JWK endpoint of the provider.
            key_mgmt_alg (:obj:`str`, optional): The key management algorithm to use. Supported values are "none", "dir", 
                            "A128KW", "A192KW", "A256KW", "A128GCMKW", "A192GCMKW", "A256GCMKW", "ECDH-ES", "ECDH-ES+A128KW", 
                            "ECDH-ES+A192KW", "ECDH-ES+A256KW", "RSA1_5", "RSA-OAEP", "RSA-OAEP-256".
            content_encrypt_alg (:obj:`str`, optional): The content encryption algorithm to use. Supported values are 
                            "none", "A128CBC-HS256", "A192CBC-HS384", "A256CBC-HS512", "A128GCM", "A192GCM", "A256GCM".
            decrypt_keystore (:obj:`str`): When key management algorithm requires a certificate, the keystore which 
                            contains the selected certificate to perform JWT decryption.
            decrypt_key_label (:obj:`str`): When key management algorithm requires a certificate, the alias of the 
                            private key in the selected keystore to perform JWT decryption.
            scope (:obj:`list` of :obj:`str`, optional): An array of strings that identify the scopes to request from 
                            the provider. Defaults to ["openid"].
            perform_user_info (`bool`, optional): A setting that specifies whether to perform user info request 
                            automatically whenever possible.
            token_endpoint_auth_method (:obj:`str): The token endpoint authentication method. Valid values are 
                            "client_secret_basic" and "client_secret_post".
            attribute_mapping (:obj:`list` of :obj:`dict`, optional): List of configured attribute sources. Format of
                            complex object is ```[{"name":"email", "source": "ldap"}, {"name":"preferred_name", 
                            "source":"credential"}]```.
            identity_delegate_id (:obj:`str`): The active mapping module instance. Valid values are "skip-identity-map", 
                            "default-map" and "default-http-custom-map".
            identity_auth_type (:obj:`str`, optional): Authentication method used when contacting external service. Supported 
                            values are NONE, BASIC or CERTIFICATE.
            identity_ba_user (:obj:`str`, optional): Username for authentication to external service.
            identity_ba_password (:obj:`str`, optional): Password for authentication to external service.
            identity_client_keystore (:obj:`str`, optional): Contains key for HTTPS client authentication.
            identity_cliekt_key_alias (:obj:`str`, optional): Alias of the key for HTTPS client authentication.
            identity_issuer_uri (:obj:`str`, optional): Refers to STS chain that provides input for callout request.
            identity_msg_fmt (:obj:`str`, optional): Message format of callout request.
            identity_ssl_keystore (:obj:`str`, optional): SSL certificate trust store to use when validating SSL 
                            certificate of external service.
            identity_uri (:obj:`str`): Address of destination server to call out to.
            adv_config_delegate_id (:obj:`str`): The active module instance. Valid values are "skip-advance-map" and 
                            "default-map".
            adv_config_rule_type (:obj:`str`, optional): The type of the mapping rule. The only supported type currently 
                            is JAVASCRIPT.
            adv_config_mapping_rule (:obj:`str`, optional): A reference to an ID of an advance configuration.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created obligation can be acess from the
            response.id_from_location attribute

        """
        #TODO
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value("enabled", enabled)
        data.add_value_string("role", role)

        attributeMapping = DataObject()
        identityMapping = DataObject()

        configuration = DataObject()
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)

        configuration.add_value_not_empty("templateName", template_name)
        configuration.add_value_not_empty("clientId", client_id)
        configuration.add_value_not_empty("clientSecret", client_secret)
        configuration.add_value_not_empty("appliesTo", applies_to)
        configuration.add_value_not_empty("grantType", grant_type)
        configuration.add_value_not_empty("authorizationEndpointUrl", authorization_endpoint_url)
        configuration.add_value_not_empty("tokenEndpointUrl", token_endpoint_url)
        configuration.add_value_not_empty("signatureAlgorithm", signature_algorithm)
        configuration.add_value_not_empty("signingKeystore", signing_keystore)
        configuration.add_value_not_empty("signingKeyLabel", signing_key_label)
        configuration.add_value_not_empty("issuerIdentifier", issuer_identifier)
        configuration.add_value_not_empty("redirectUriPrefix", redirect_uri_prefix)
        configuration.add_value_not_empty("jwkEndpointUrl", jwk_endopoint_url)
        configuration.add_value("scope", scope)

        data.add_value_not_empty("configuration", configuration.data)

        endpoint = "%s/%s/partners" % (FEDERATIONS, federation_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response


    def create_saml_federation(self, name=None, role=None, access_policy=None, artifact_lifetime=None, assertion_attr_types=[],
            assertion_session_not_on_or_after=None, assertion_multi_attr_stmt=None, assertion_valid_before=None, 
            assertion_valid_after=None, artifact_resolution_service=[], attribute_mapping=[], company_name=None,
            encrypt_block_alg=None, encrypt_key_transport_alg=None, encrypt_key_alias=None, encrypt_key_store=None, 
            encrypt_name_id=None, encrypt_assertions=None, encrypt_assertion_attrs=None, decrypt_key_alias=None, 
            decrypt_key_store=None, identity_delegate_id=None, identity_rule_type='JAVASCRIPT', identity_rule_id=None,
            identity_applies_to=None, identity_auth_type=None, identity_ba_user=None, identity_ba_password=None,
            identity_client_keystore=None, identity_client_key_alias=None, identity_issuer_uri=None, identity_msg_fmt=None,
            identity_ssl_keystore=None, identity_uri=None, ext_delegate_id=None, ext_mapping_rule=None, service_data=[],
            msg_valid_time=None, msg_issuer_fmt=None, msg_issuer_name_qualifier=None, name_id_format=None, name_id_supported=[],
            consent_to_federate=True, exclude_session_index_logout_request=False, poc_url=None, provider_id=None, 
            session_timeout=None, sign_alg=None, sign_digest_alg=None, sign_key_store=None, sign_key_alias=None, 
            sign_assertion=None, sign_auth_rsp=None, sign_arti_req=None, sign_arti_rsp=None, sign_authn_rsp=None, 
            sing_logout_req=None, sign_logout_rsp=None, sign_name_id_req=None, sign_name_id_rsp=None, validate_auth_req=None,
            validate_assert=None, validate_arti_req=None, validate_arti_rsp=None,validate_logout_req=None, validate_logout_rsp=None,
            validate_name_id_req=None, validate_name_id_rsp=None,

            template_name=None, active_delegate_id=None, need_consent_to_federate=None,
            signature_algorithm=None, signing_keystore=None, signing_key_label=None, sso_service_binding=None,message_issuer_format=None,
            decrypt_keystore=None, decrypt_key_label=None, point_of_contact_url=None, provider_id=None, company_name=None):
        """
        Create a SAML 2.0 federation.

        Args:
            name (:obj:`str`): The name of the federation
            role (:obj:`str`): The role of a federation: "ip" for a SAML 2.0 identity provider federation, and "sp" for 
                            a SAML 2.0 service provider federation.
            tempalte_name (:obj:`str`, optional): An identifier for the template on which to base this federation.
            access_policy (:obj:`str`, optional): The access policy that should be applied during single sign-on.
            artifact_lifetime(`int`, optional): The number of seconds that an artifact is valid. The default value is 120.
            assertion_attr_types (:obj:`list` of :obj:`str`, optional): A setting that specifies the types of attributes 
                            to include in the assertion.
            assertion_session_not_on_or_after (`int`, optional): The number of seconds that the security context established for 
                            the principal should be discarded by the service provider.The default value is 3600.
            assertion_mult_attr_stmt (`bool`, optional): A setting that specifies whether to keep multiple attribute 
                            statements in the groups in which they were received.
            assertion_valid_before (`int, optional): The number of seconds before the issue date that an assertion is 
                            considered valid.
            assertion_valid_after (`int`, optional): The number of seconds the assertion is valid after being issued.
            artifact_resolution_service (:obj:`list` of :obj:`dict`, optional): Endpoints where artifacts are exchanged 
                            for actual SAML messages. Required if artifact binding is enabled. Format of artifact 
                            resolution service data is ```[{"binding":"soap","default":false,"index":0,"url":"https://demo.com/endpoint"},
                            {"binding":"soap","default":true,"index":1,"url":"https://domain.com/endpoint"}]```
            attribute_mapping (:obj:`list` of :obj:`dict`, optional): The attribute mapping data. format is:
                            ```[{"name":"email","source":"ldap_email"},{"mobile":"source":"ldap_phone"}]```
            company_name (:obj:`str`, optional): The name of the company that creates the identity provider or service 
                            provider.
            encrypt_block_alg (:obj:`str`, optional): Block encryption algorithm used to encrypt and decrypt SAML message.
            encrypt_key_transport_alg (:obj:`str`): Key transport algorithm used to encrypt and decrypt keys.
            encrypt_key_alias (:obj:`str`, optional): The certificate for encryption of outgoing SAML messages.
            encrypt_key_store (:obj:`str`, optioanl): The certificate database name.
            encrypt_name_id (`bool`, optional): A setting that specifies whether the name identifiers should be encrypted.
            encrypt_assertions (`bool`, optional): A setting that specifies whether to encrypt assertions.
            encrypt_assertion_attrs (`bool`, optional): A setting that specifies whether to encrypt assertion attributes
            decrypt_key_alias (:obj:`str`, optional): A public/private key pair that the federation partners can use to
                            encrypt certain message content.
            decrypt_key_store (:obj:`str`, optional): The certificate database name.
        

        """
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("protocol", "SAML2_0")
        data.add_value_string("role", role)
        data.add_value_string("templateName", template_name)

        encryptionSettings = DataObject()
        signatureSettings = DataObject()

        identityMapping = None
        if (active_delegate_id is not None):
            identityMapping = DataObject()
            identityMapping.add_value_string("activeDelegateId", active_delegate_id)

        decryptionKeyIdentifier = DataObject()
        decryptionKeyIdentifier.add_value_string("keystore", decrypt_keystore)
        decryptionKeyIdentifier.add_value_string("label", decrypt_key_label)
        signingKeyIdentifier = DataObject()
        signingKeyIdentifier.add_value_string("keystore", signing_keystore)
        signingKeyIdentifier.add_value_string("label", signing_key_label)

        encryptionSettings.add_value_not_empty("decryptionKeyIdentifier", decryptionKeyIdentifier.data)
        signatureSettings.add_value_not_empty("signingKeyIdentifier", signingKeyIdentifier.data)

        ssoServiceBinding = None
        if (sso_service_binding is not None):
            ssoServiceBinding = DataObject()
            ssoServiceBinding.add_value_string("binding", sso_service_binding)

        configuration = DataObject()
        configuration.add_value_not_empty("encryptionSettings", encryptionSettings.data)
        configuration.add_value_not_empty("signatureSettings", signatureSettings.data)
        configuration.add_value_string("providerId", provider_id)
        configuration.add_value_string("pointOfContactUrl", point_of_contact_url)
        configuration.add_value_string("companyName", company_name)
        if (ssoServiceBinding is not None):
            configuration.add_value("singleSignOnService", [ssoServiceBinding.data])
        if (identityMapping is not None):
            configuration.add_value("identityMapping", identityMapping.data)
        configuration.add_value("needConsentToFederate", need_consent_to_federate)
        configuration.add_value_string("messageIssuerFormat", message_issuer_format)

        data.add_value_not_empty("configuration", configuration.data)

        response = self.client.post_json(FEDERATIONS, data.data)
        response.success = response.status_code == 201

        return response


    def create_saml_partner(self, federation_id, name=None, enabled=False, role=None, template_name=None, acs_binding=None, block_encryption_algorithm=None,
        encryption_key_transport_algorithm = None, encryption_keystore=None, encryption_key_label=None,signature_digest_algorithm=None, acs=None, single_logout_service=None,
        acs_default=True, acs_index=0, acs_url=None, attribute_mapping=[], active_delegate_id=None, client_auth_method=None, signature_algorithm=None,
        validate_logout_request=None,validate_logout_response=None,
        provider_id=None, signature_validation=None, validate_authn_request=None, validation_keystore=None, validation_key_label=None, mapping_rule=None):
        
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value("enabled", enabled)
        data.add_value_string("role", role)
        data.add_value_string("templateName", template_name)

        attributeMapping = DataObject()
        attributeMapping.add_value_not_empty("map", attribute_mapping)

        properties = DataObject()

        clientAuth = DataObject()
        clientAuth.add_value_string("method", client_auth_method)
        clientAuth.add_value_not_empty("properties", properties.data)

        serverCertValidation = DataObject()
        # serverCertValidation.add_value_string("keystore", "")

        soapSettings = DataObject()
        soapSettings.add_value_not_empty("clientAuth", clientAuth.data)
        if clientAuth.data or serverCertValidation.data:
            soapSettings.add_value("serverCertValidation", serverCertValidation.data)

        properties = DataObject()
        properties.add_value_string("identityMappingRule", mapping_rule)

        identityMapping = DataObject()
        identityMapping.add_value_not_empty("properties", properties.data)
        identityMapping.add_value_string("activeDelegateId", active_delegate_id)

        assertionConsumerService = DataObject()
        assertionConsumerService.add_value_string("binding", acs_binding)
        assertionConsumerService.add_value("default", acs_default)
        assertionConsumerService.add_value("index", acs_index)
        assertionConsumerService.add_value_string("url", acs_url)

        encryptionKeyIdentifier = DataObject()
        encryptionKeyIdentifier.add_value("keystore", encryption_keystore)
        encryptionKeyIdentifier.add_value("label", encryption_key_label)

        encryptionSettings = DataObject()
        encryptionSettings.add_value_not_empty("encryptionKeyIdentifier", encryptionKeyIdentifier.data)
        encryptionSettings.add_value_string("blockEncryptionAlgorithm", block_encryption_algorithm)
        encryptionSettings.add_value_string("encryptionKeyTransportAlgorithm", encryption_key_transport_algorithm)

        validationKeyIdentifier = DataObject()
        validationKeyIdentifier.add_value("keystore", validation_keystore)
        validationKeyIdentifier.add_value("label", validation_key_label)

        validationOptions = DataObject()
        validationOptions.add_value("validateAuthnRequest", validate_authn_request)
        validationOptions.add_value("validateLogoutRequest", validate_logout_request)
        validationOptions.add_value("validateLogoutResponse", validate_logout_response)

        signatureSettings = DataObject()
        signatureSettings.add_value_not_empty("validationOptions", validationOptions.data)
        signatureSettings.add_value_not_empty("validationKeyIdentifier", validationKeyIdentifier.data)
        signatureSettings.add_value_string("signatureAlgorithm", signature_algorithm)
        signatureSettings.add_value_string("digestAlgorithm", signature_digest_algorithm)

        configuration = DataObject()
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)
        configuration.add_value_not_empty("assertionConsumerService", [assertionConsumerService.data])
        configuration.add_value_not_empty("assertionConsumerService", acs)
        configuration.add_value_not_empty("singleLogoutService", single_logout_service)
        configuration.add_value_not_empty("signatureSettings", signatureSettings.data)
        configuration.add_value_not_empty("encryptionSettings", encryptionSettings.data)
        configuration.add_value_not_empty("soapSettings", soapSettings.data)
        configuration.add_value_not_empty("providerId", provider_id)

        data.add_value_not_empty("configuration", configuration.data)

        endpoint = "%s%s/partners" % (FEDERATIONS, federation_id)

        print(json.dumps(data.data))

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response


    def get_federation(self, federation_id=None):
        """
        Get a federation configuration.

        Args:
            federation_id (:obj:`str`): The unique id of the federation

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the federation configuration is returned as JSON and can be accessed from
            the response.json attribute

        """
        endpoint = "%s/%s" % (FEDERATIONS, federation_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def list_federations(self):
        response = self.client.get_json(FEDERATIONS)
        response.success = response.status_code == 200
        return response

    def list_partners(self, federation_id):
        endpoint = "%s/%s/partners" % (FEDERATIONS, federation_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def get_partner(self, federation_id, partner_id=None):
        """
        Get a partner configuration from a federation

        Args:
            federation_id (:obj:`str`): The id of the federation.
            partner_id (:obj:`str`): The id of the partner to return.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the federation partner configuration is returned as JSON and can be accessed from
            the response.json attribute

        """
        endpoint = "%s/%s/partners/%s" % (FEDERATIONS, federation_id, partner_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


class Federations9040(Federations):

    def create_oidc_rp_federation(self, name=None, redirect_uri_prefix=None,
            response_types=None, active_delegate_id=None, identity_mapping_rule_reference=None,
            advanced_configuration_active_delegate=None, advanced_configuration_rule_id=None):

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("protocol", "OIDC10")
        data.add_value_string("role", 'rp')

        attributeMapping = DataObject()
        
        identityMapping = DataObject()
        identityMapping.add_value_string("activeDelegateId", active_delegate_id)
        properties = DataObject()
        properties.add_value_string("identityMappingRuleReference", identity_mapping_rule_reference)
        identityMapping.add_value_not_empty("properties", properties.data)

        advancedConfiguration = DataObject()
        if advanced_configuration_active_delegate == None : 
            advancedConfiguration.add_value_string("activeDelegateId", 'skip-advance-map')
        else:
            advancedConfiguration.add_value_string("activeDelegateId", advanced_configuration_active_delegate)
            properties = DataObject()
            properties.add_value_string("advanceMappingRuleReference", advanced_configuration_rule_id)
            advancedConfiguration.add_value_not_empty("properties", properties.data)

        configuration = DataObject()
        configuration.add_value_string("redirectUriPrefix", redirect_uri_prefix)
        configuration.add_value("responseTypes", response_types)
        configuration.add_value_not_empty("advanceConfiguration", advancedConfiguration.data)
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)

        data.add_value_not_empty("configuration", configuration.data)

        response = self.client.post_json(FEDERATIONS, data.data)
        response.success = response.status_code == 201

        return response

    def create_oidc_rp_partner(self, federation_id, name=None, enabled=False, client_id=None, 
            client_secret=None, metadata_endpoint=None, scope=None,
            token_endpoint_auth_method=None, perform_userinfo=False,
            advanced_configuration_active_delegate='skip-advance-map', advanced_configuration_rule_id=None,
            signing_algorithm=None):

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value("enabled", enabled)
        data.add_value_string("role", 'rp')

        attributeMapping = DataObject()
        identityMapping = DataObject()

        configuration = DataObject()


        configuration.add_value_not_empty("clientId", client_id)
        configuration.add_value_not_empty("signatureAlgorithm", signing_algorithm)
        configuration.add_value_not_empty("clientSecret", client_secret)
        configuration.add_value_not_empty("scope", scope)
        configuration.add_value_not_empty("tokenEndpointAuthMethod", token_endpoint_auth_method)
        configuration.add_value_not_empty("performUserinfo", perform_userinfo)

        basic = DataObject()
        basic.add_value_not_empty("activeDelegateId","metadataEndpointUrl")

        basic_properties = DataObject()
        basic_properties.add_value_not_empty("metadataEndpointUrl", metadata_endpoint)
        basic.add_value("properties",basic_properties.data)
        
        configuration.add_value("scope", scope)

        configuration.add_value_not_empty("identityMapping", identityMapping.data)

        if advanced_configuration_active_delegate: 
            advancedConfiguration = DataObject()
            advancedConfiguration.add_value_string("activeDelegateId", advanced_configuration_active_delegate)
            if (advanced_configuration_active_delegate != 'skip-advance-map'):
                properties = DataObject()
                properties.add_value_string("advanceMappingRuleReference", advanced_configuration_rule_id)
                advancedConfiguration.add_value_not_empty("properties", properties.data)
            configuration.add_value_not_empty("advanceConfiguration", advancedConfiguration.data)

        configuration.add_value_not_empty("basicConfiguration", basic.data)

        data.add_value_not_empty("configuration", configuration.data)

        endpoint = "%s/%s/partners" % (FEDERATIONS, federation_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response

class Federations10000(Federations9040):

    def create_saml_federation(self, name=None, role=None, template_name=None, active_delegate_id=None, need_consent_to_federate=None,
            signature_algorithm=None, signing_keystore=None, signing_key_label=None, sso_service_binding=None,message_issuer_format=None,
            decrypt_keystore=None, decrypt_key_label=None, point_of_contact_url=None, provider_id=None, company_name=None):

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("protocol", "SAML2_0")
        data.add_value_string("role", role)
        data.add_value_string("templateName", template_name)

        encryptionSettings = DataObject()
        signatureSettings = DataObject()

        identityMapping = None
        if (active_delegate_id is not None):
            identityMapping = DataObject()
            identityMapping.add_value_string("activeDelegateId", active_delegate_id)

        decryptionKeyIdentifier = DataObject()
        decryptionKeyIdentifier.add_value_string("keystore", decrypt_keystore)
        decryptionKeyIdentifier.add_value_string("label", decrypt_key_label)
        signingKeyIdentifier = DataObject()
        signingKeyIdentifier.add_value_string("keystore", signing_keystore)
        signingKeyIdentifier.add_value_string("label", signing_key_label)

        encryptionSettings.add_value_not_empty("decryptionKeyIdentifier", decryptionKeyIdentifier.data)
        signatureSettings.add_value_not_empty("signingKeyIdentifier", signingKeyIdentifier.data)

        ssoServiceBinding = None
        if (sso_service_binding is not None):
            ssoServiceBinding = DataObject()
            ssoServiceBinding.add_value_string("binding", sso_service_binding)

        configuration = DataObject()
        configuration.add_value_not_empty("encryptionSettings", encryptionSettings.data)
        configuration.add_value_not_empty("signatureSettings", signatureSettings.data)
        configuration.add_value_string("providerId", provider_id)
        configuration.add_value_string("pointOfContactUrl", point_of_contact_url)
        configuration.add_value_string("companyName", company_name)
        if (ssoServiceBinding is not None):
            configuration.add_value("singleSignOnService", [ssoServiceBinding.data])
        if (identityMapping is not None):
            configuration.add_value("identityMapping", identityMapping.data)
        configuration.add_value("needConsentToFederate", need_consent_to_federate)
        configuration.add_value_string("messageIssuerFormat", message_issuer_format)

        data.add_value_not_empty("configuration", configuration.data)

        response = self.client.post_json(FEDERATIONS, data.data)
        response.success = response.status_code == 201

        return response


    def create_saml_partner(self, federation_id, name=None, enabled=False, role=None, template_name=None, acs_binding=None, block_encryption_algorithm=None,
        encryption_key_transport_algorithm = None, encryption_keystore=None, encryption_key_label=None,signature_digest_algorithm=None, acs=None, single_logout_service=None,
        acs_default=True, acs_index=0, acs_url=None, attribute_mapping=[], active_delegate_id=None, client_auth_method=None, signature_algorithm=None,
        validate_logout_request=None,validate_logout_response=None,
        provider_id=None, signature_validation=None, validate_authn_request=None, validation_keystore=None, validation_key_label=None, mapping_rule=None):
        
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value("enabled", enabled)
        data.add_value_string("role", role)
        data.add_value_string("templateName", template_name)

        attributeMapping = DataObject()
        attributeMapping.add_value_not_empty("map", attribute_mapping)

        properties = DataObject()

        clientAuth = DataObject()
        clientAuth.add_value_string("method", client_auth_method)
        clientAuth.add_value_not_empty("properties", properties.data)

        serverCertValidation = DataObject()
        # serverCertValidation.add_value_string("keystore", "")

        soapSettings = DataObject()
        soapSettings.add_value_not_empty("clientAuth", clientAuth.data)
        if clientAuth.data or serverCertValidation.data:
            soapSettings.add_value("serverCertValidation", serverCertValidation.data)

        properties = DataObject()
        properties.add_value_string("identityMappingRule", mapping_rule)

        identityMapping = DataObject()
        identityMapping.add_value_not_empty("properties", properties.data)
        identityMapping.add_value_string("activeDelegateId", active_delegate_id)

        assertionConsumerService = DataObject()
        assertionConsumerService.add_value_string("binding", acs_binding)
        assertionConsumerService.add_value("default", acs_default)
        assertionConsumerService.add_value("index", acs_index)
        assertionConsumerService.add_value_string("url", acs_url)

        encryptionKeyIdentifier = DataObject()
        encryptionKeyIdentifier.add_value("keystore", encryption_keystore)
        encryptionKeyIdentifier.add_value("label", encryption_key_label)

        encryptionSettings = DataObject()
        encryptionSettings.add_value_not_empty("encryptionKeyIdentifier", encryptionKeyIdentifier.data)
        encryptionSettings.add_value_string("blockEncryptionAlgorithm", block_encryption_algorithm)
        encryptionSettings.add_value_string("encryptionKeyTransportAlgorithm", encryption_key_transport_algorithm)

        validationKeyIdentifier = DataObject()
        validationKeyIdentifier.add_value("keystore", validation_keystore)
        validationKeyIdentifier.add_value("label", validation_key_label)

        validationOptions = DataObject()
        validationOptions.add_value("validateAuthnRequest", validate_authn_request)
        validationOptions.add_value("validateLogoutRequest", validate_logout_request)
        validationOptions.add_value("validateLogoutResponse", validate_logout_response)

        signatureSettings = DataObject()
        signatureSettings.add_value_not_empty("validationOptions", validationOptions.data)
        signatureSettings.add_value_not_empty("validationKeyIdentifier", validationKeyIdentifier.data)
        signatureSettings.add_value_string("signatureAlgorithm", signature_algorithm)
        signatureSettings.add_value_string("digestAlgorithm", signature_digest_algorithm)

        configuration = DataObject()
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)
        configuration.add_value_not_empty("assertionConsumerService", [assertionConsumerService.data])
        configuration.add_value_not_empty("assertionConsumerService", acs)
        configuration.add_value_not_empty("singleLogoutService", single_logout_service)
        configuration.add_value_not_empty("signatureSettings", signatureSettings.data)
        configuration.add_value_not_empty("encryptionSettings", encryptionSettings.data)
        configuration.add_value_not_empty("soapSettings", soapSettings.data)
        configuration.add_value_not_empty("providerId", provider_id)

        data.add_value_not_empty("configuration", configuration.data)

        endpoint = "%s%s/partners" % (FEDERATIONS, federation_id)

        print(json.dumps(data.data))

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response
