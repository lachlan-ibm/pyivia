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

    def create_oidc_federation(self, name=None, role=None, issuer_identifier=None, 
            signature_algorithm=None, signing_keystore=None, signing_key_label=None, 
            refresh_token_length=None, authorization_grant_lifetime=None, 
            authorization_code_lifetime=None, authorization_code_length=None, 
            access_token_lifetime=None, access_token_length=None, 
            id_token_lifetime=None, grant_types_supported=None, 
            active_delegate_id=None, rule_type=None,
            identity_mapping_rule_reference=None, applies_to=None, auth_type=None, 
            basic_auth_username=None, basic_auth_password=None, client_key_store=None, client_key_alias=None,
            issuer_uri=None, message_format=None, ssl_key_store=None, uri=None):

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("protocol", "OIDC")
        data.add_value_string("role", role)

        attributeMapping = DataObject()
        
        identityMapping = DataObject()
        identityMapping.add_value_string("activeDelegateId", active_delegate_id)
        properties = DataObject()
        properties.add_value_string("ruleType", rule_type)
        properties.add_value_string("identityMappingRuleReference", identity_mapping_rule_reference)
        identityMapping.add_value_not_empty("properties", properties.data)

        configuration = DataObject()
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)

        data.add_value_not_empty("configuration", configuration.data)

        response = self.client.post_json(FEDERATIONS, data.data)
        response.success = response.status_code == 201

        return response

    def create_oidc_partner(self, federation_id, name=None, enabled=False, role=None, template_name=None, client_id=None, 
        client_secret=None, applies_to=None, grant_type=None, authorization_endpoint_url=None, token_endpoint_url=None, 
        signature_algorithm=None, signing_keystore=None, signing_key_label=None, issuer_identifier=None, redirect_uri_prefix=None, jwk_endopoint_url=None, scope=[]):
        
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


    def list_federations(self):
        response = self.client.get_json(FEDERATIONS)
        response.success = response.status_code == 200
        return response

    def list_partners(self, federation_id):
        endpoint = "%s/%s/partners" % (FEDERATIONS, federation_id)
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
