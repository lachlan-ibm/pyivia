"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient

STS_BASE = "/iam/access/v8/sts/"
STS_MODULES = STS_BASE + "modules"
STS_MODULE_TYPES = STS_BASE + "module-types"
STS_TEMPLATES = STS_BASE + "templates"
STS_CHAINS = STS_BASE + "chains"

logger = logging.getLogger(__name__)

class SecurityTokenService(object):

    def __init__(self, base_url, username, password):
        super(SecurityTokenService, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def list_module_types(self):
        """
        Get the list of Security Token Service module types.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the STS module types are returned as JSON and can be accessed from
            the response.json attribute.
        """

        endpoint = STS_MODULE_TYPES

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def list_modules(self):
        """
        Get a list of the configured Security Token Service modules.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the STS modules are returned as JSON and can be accessed from
            the response.json attribute.
        """

        endpoint = STS_MODULES

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_module(self, module_id):
        """
        Get the configuration of A Security Token Service module.

        Args:
            module_id (:obj:`str`): The system-assigned STS module ID value.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the STS module configuration is returned as JSON and can be accessed from
            the response.json attribute.
        """

        endpoint = "%s/%s" % (STS_MODULES, module_id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_templates(self):
        """
        Get a list of STS chain templates.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the STS chain templates are returned as JSON and can be accessed from
            the response.json attribute.
        """

        endpoint = STS_TEMPLATES

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_template(self, template_id):
        """
        Get a STS cain template.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the STS chain template is returned as JSON and can be accessed from
            the response.json attribute.
        """
        endpoint = "%s/%s" % (STS_TEMPLATES, template_id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create_template(self, name, description=None, modules=[]):
        """
        Create a STS chain template.

        Args:
            name (:obj:`str`): A friendly name for the STS Chain Template
            description (:obj:`str`): A description of the STS Chain Template
            modules (:obj:`list` of :obj:`str`): An array of the modules that make up the STS Chain Template. Each module contains

                        - id: The token id of an STS module
                        - mode: The mode the STS module is used in in the chain. Must be one of the supported modes of the STS module
                        - prefix (optional): The prefix for the chain item.

                    example:: 

                            {
                                "id":"default-map",
                                "mode":"map",
                                "prefix":"uuid3dbf4c6a-013d-15d5-bb8b-c2665e02a402"
                            }

        Returns:
            :obj:`~requests.response`: the response from verify identity access. 

            success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created STS template can be accessed from the 
            response.id_from_location attribute.
        """
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_not_empty("chainItems", modules)

        response = self.client.post_json(STS_TEMPLATES, data.data)
        response.success = response.status_code == 201

        return response


    def delete_template(self, template_id):
        """
        Remove a STS chian template.

        Args:
            template_id (:obj:`str`): The system-assigned STS chain ID value.

        Returns:
            :obj:`~requests.response`: the response from verify identity access. 

            success can be checked by examining the response.success boolean attribute.
        """
        endpoint = "%s/%s" % (STS_TEMPLATES, template_id)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def list_chains(self):
        """
        Get a list of the configured STS chains.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the STS chains are returned as JSON and can be accessed from
            the response.json attribute.
        """
        response = self.client.get_json(STS_CHAINS)
        response.success = response.status_code == 200

        return response


    def get_chain(self, chain_id):
        """
        Get a configured STS chain.

        Args:
            chain_id (:obj:`str`): The system-assigned STS chain template ID value.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the STS chain is returned as JSON and can be accessed from
            the response.json attribute.
        """
        endpoint = "%s/%s" % (STS_CHAINS, chain_id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_chain(self, name, description=None, template_id=None, request_type=None, token_type=None, xpath=None,
            sign_responses=None, sign_key_store=None, sign_key_alias=None, sign_include_cert=None, sign_include_pubkey=None, 
            sign_include_ski=None, sign_include_issuer=None, sign_include_subject=None, validate_requests=None, 
            validation_key_store=None, validation_key_alias=None, validation_include_cert=None, validation_include_pubkey=None,
            validation_include_ski=None, validation_include_issuer=None , validation_include_subject=None, 
            send_validation_confirmation=None, issuer_address=None, issuer_port_type_namespace=None, issuer_port_type_name=None,
            issuer_service_namespace=None, issuer_service_name=None, applies_to_address=None, applies_to_port_type_namespace=None, 
            applies_to_port_type_name=None, applies_to_service_namespace=None, applies_to_service_name=None, 
            self_properties=[], partner_properties=[]):
        """
        Create a STS chain.

        Args:
            name (:obj:`str`): A friendly name for the STS Chain
            description (:obj:`str`, optional): A description of the STS Chain
            template_id (:obj:`str`): The Id of the STS Chain Template that is referenced by this STS Chain
            request_type (:obj:`str`): The type of request to associate with this chain. The request is one of the types 
                                       that are supported by the WS-Trust specification.
            token_type (:obj:`str`, optional): The STS module type to map a request message to an STS Chain Template
            xpath (:obj:`str`, optional): The custom lookup rule in XML Path Language to map a request message to an STS 
                            Chain Template
            sign_responses (`bool`, optional): Whether to sign the Trust Server SOAP response messages.
            sign_key_store (:obj:`str`, optional): SSL database which contains private key to sign messages.
            sign_key_alias (:obj:`str`, optional): private key to sign messages.
            sign_include_cert (`bool`, optional): Whether to include the BASE64 encoded certificate data with your 
                                                  signature.
            sign_include_pubkey (`bool`, optional): Whether to include the public key with the signature.
            sign_include_ski (`bool`, optional): Whether to include the X.509 subject key identifier with the signature
            sign_include_issuer (`bool`, optional): Whether to include the issuer name and the certificate serial 
                                                    number with the signature
            sign_include_subject (`bool`, optional): Whether to include the subject name with the signature.
            validate_requests (`bool`, optional): Whether requires a signature on the received SOAP request message 
                                                  that contains the RequestSecurityToken message.
            validation_key_store (:obj:`str`, optional): The SSL database which contains the private key to validate
                                                        messages.
            validation_key_alias (:obj:`str`, optional): The key to validate the received SOAP request message
            validation_include_cert (`bool`, optional): Whether the BASE64 encoded certificate data is included with 
                                                        the signature.
            validation_include_pubkey (`bool`, optional): Whether to include the public key with the signature.
            validation_include_ski (`bool`, optional): Whether to include the X.509 subject key identifier with the 
                                                       signature.
            validation_include_issuer (`bool`, optional): Whether to include the issuer name and the certificate serial 
                                                          number with the signature.
            validation_include_subject (`bool`, optional): Whether to include the subject name with the signature.
            send_validation_confirmation (`bool`, optional): Whether to send signature validation confirmation.
            issuer_address (:obj:`str`): The URI of the issuer company or enterprise
            issuer_port_type_namespace (:obj:`str`, optional): The namespace URI part of a qualified name for the issuer
                                                               Web service port type.
            issuer_port_type_name (:obj:`str`, optional): The local part of a qualified name for the issuer Web service 
                                                        port type.
            issuer_service_namespace (:obj:`str`, optional): The namespace URI part of a qualified name for the issuer 
                                                            Web service.
            issuer_service_name (:obj:`str`, optional): The local part of a qualified name for the issuer Web service.
            applies_to_address (:obj:`str`): The URI of the scope company or enterprise
            applies_to_port_type_namespace (:obj:`str`, optional): The namespace URI part of a qualified name for the scope
                            Web service port 
            applies_to_port_type_name (:obj:`str`, optional): The local part of a qualified name for the scope Web 
                            service port type.
            applies_to_service_namespace (:obj:`str`, optional): The namespace URI part of a qualified name for the scope
                            Web service
            applies_to_service_name (:obj:`str`, optional): The local part of a qualified name for the scope Web service.
            self_properties (:obj:`list` of :obj:`dict`): The self properties for all modules within the STS Chain Template 
                            referenced in the STS Chain. A property has the format `{"name":"STS Property","value":["demo","values"]}`
            partner_properties (:obj:`list` of :obj:`dict`): The partner properties for all modules within the STS Chain Template 
                            referenced in the STS Chain. A property has the format `{"name":"STS Property","value":["demo","values"]}`

        """
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("chainId", template_id)
        data.add_value_string("requestType", request_type)
        data.add_value_string("tokenType", token_type)
        data.add_value_string("xPath", xpath)

        signKey = DataObject()
        signKey.add_value_string("keyAlias_db", sign_key_store)
        signKey.add_value_string("keyAlias_cert", sign_key_alias)
        signKey.add_value_boolean("includeCertificateData", sign_include_cert)
        signKey.add_value_boolean("includePublicKey", sign_include_pubkey)
        signKey.add_value_boolean("includeSubjectKeyIdentifier", sign_include_ski)
        signKey.add_value_boolean("includeIssuerDetails", sign_include_issuer)
        signKey.add_value_boolean("includeSubjectName", sign_include_subject)

        validKey = DataObject()
        validKey.add_value_string("keyAlias_db", validation_key_store)
        validKey.add_value_string("keyAlias_cert", validation_key_alias)
        validKey.add_value_boolean("includeCertificateData", validation_include_cert)
        validKey.add_value_boolean("includePublicKey", validation_include_pubkey)
        validKey.add_value_boolean("includeSubjectKeyIdentifier", validation_include_ski)
        validKey.add_value_boolean("includeIssuerDetails", validation_include_issuer)
        validKey.add_value_boolean("includeSubjectName", validation_include_subject)


        applies_to = DataObject()
        applies_to.add_value_string("address", applies_to_address)
        applies_to.add_value_string("portTypeNamespace", applies_to_port_type_namespace)
        applies_to.add_value_string("portTypeName", applies_to_port_type_name)
        applies_to.add_value_string("serviceNamespace", applies_to_service_namespace)
        applies_to.add_value_string("serviceName", applies_to_service_name)
        data.add_value("appliesTo", applies_to.data)

        issuer = DataObject()
        issuer.add_value_string("address", issuer_address)
        issuer.add_value_string("portTypeNamespace", issuer_port_type_namespace)
        issuer.add_value_string("portTypeName", issuer_port_type_name)
        issuer.add_value_string("serviceNamespace", issuer_service_namespace)
        issuer.add_value_string("serviceName", issuer_service_name)
        data.add_value("issuer", issuer.data)

        data.add_value_boolean("validateRequests", validate_requests)
        data.add_value_not_empty("validationKey", validKey.data)
        data.add_value_boolean("signResponses", sign_responses)
        data.add_value_not_empty("signatureKey", signKey.data)
        data.add_value_boolean("sendValidationConfirmation", send_validation_confirmation)

        properties = DataObject()
        properties.add_value_not_empty("self", self_properties)
        properties.add_value_not_empty("partner", partner_properties)
        data.add_value("properties", properties.data)

        response = self.client.post_json(STS_CHAINS, data.data)
        response.success = response.status_code == 201

        return response

    def delete_chain(self, chain_id):
        """
        Delete a STS chain

        Args:
            chain_id (:obj:`str`): The system-assigned STS chain ID value.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        endpoint = "%s/%s" % (STS_CHAINS, chain_id)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def update_chain(self, chain_id, name=None, description=None, template_id=None, request_type=None, token_type=None, xpath=None,
            sign_responses=None, sign_key_store=None, sign_key_alias=None, sign_include_cert=None, sign_include_pubkey=None, 
            sign_include_ski=None, sign_include_issuer=None, sign_include_subject=None, validate_requests=None, 
            validation_key_store=None, validation_key_alias=None, validation_include_cert=None, validation_include_pubkey=None,
            validation_include_ski=None, validation_include_issuer=None , validation_include_subject=None, 
            send_validation_confirmation=None, issuer_address=None, issuer_port_type_namespace=None, issuer_port_type_name=None,
            issuer_service_namespace=None, issuer_service_name=None, applies_to_address=None, applies_to_port_type_namespace=None, 
            applies_to_port_type_name=None, applies_to_service_namespace=None, applies_to_service_name=None, 
            self_properties=[], partner_properties=[]):
        """
        Update an existing STS chain

        Args:
            chain_id (:obj:`str`): The Verify Identity Access assigned identifier of the STS chain.
            name (:obj:`str`): A friendly name for the STS Chain
            description (:obj:`str`, optional): A description of the STS Chain
            template_id (:obj:`str`): The Id of the STS Chain Template that is referenced by this STS Chain
            request_type (:obj:`str`): The type of request to associate with this chain. The request is one of the types 
                            that are supported by the WS-Trust specification.
            token_type (:obj:`str`, optional): The STS module type to map a request message to an STS Chain Template
            xpath (:obj:`str`, optional): The custom lookup rule in XML Path Language to map a request message to an STS 
                            Chain Template
            sign_responses (`bool`, optional): Whether to sign the Trust Server SOAP response messages.
            sign_key_store (:obj:`str`, optional): SSL database which contains private key to sign messages.
            sign_key_alias (:obj:`str`, optional): private key to sign messages.
            sign_include_cert (`bool`, optional): Whether to include the BASE64 encoded certificate data with your 
                            signature.
            sign_include_pubkey (`bool`, optional): Whether to include the public key with the signature.
            sign_include_ski (`bool`, optional): Whether to include the X.509 subject key identifier with the signature
            sign_include_issuer (`bool`, optional): Whether to include the issuer name and the certificate serial 
                            number with the signature
            sign_include_subject (`bool`, optional): Whether to include the subject name with the signature.
            validate_requests (`bool`, optional): Whether requires a signature on the received SOAP request message 
                            that contains the RequestSecurityToken message.
            validation_key_store (:obj:`str`, optional): The SSL database which contains the private key to validate
                            messages.
            validation_key_alias (:obj:`str`, optional): The key to validate the received SOAP request message
            validation_include_cert (`bool`, optional): Whether the BASE64 encoded certificate data is included with 
                            the signature.
            validation_include_pubkey (`bool`, optional): Whether to include the public key with the signature.
            validation_include_ski (`bool`, optional): Whether to include the X.509 subject key identifier with the 
                                                       signature.
            validation_include_issuer (`bool`, optional): Whether to include the issuer name and the certificate serial 
                                                          number with the signature.
            validation_include_subject (`bool`, optional): Whether to include the subject name with the signature.
            send_validation_confirmation (`bool`, optional): Whether to send signature validation confirmation.
            issuer_address (:obj:`str`): The URI of the issuer company or enterprise
            issuer_port_type_namespace (:obj:`str`, optional): The namespace URI part of a qualified name for the issuer
                            Web service port type.
            issuer_port_type_name (:obj:`str`, optional): The local part of a qualified name for the issuer Web service 
                            port type.
            issuer_service_namespace (:obj:`str`, optional): The namespace URI part of a qualified name for the issuer 
                            Web service.
            issuer_service_name (:obj:`str`, optional): The local part of a qualified name for the issuer Web service.
            applies_to_address (:obj:`str`): The URI of the scope company or enterprise
            applies_to_port_type_namespace (:obj:`str`, optional): The namespace URI part of a qualified name for the scope
                            Web service port 
            applies_to_port_type_name (:obj:`str`, optional): The local part of a qualified name for the scope Web 
                            service port type.
            applies_to_service_namespace (:obj:`str`, optional): The namespace URI part of a qualified name for the scope
                            Web service
            applies_to_service_name (:obj:`str`, optional): The local part of a qualified name for the scope Web service.
            self_properties (:obj:`list` of :obj:`dict`): The self properties for all modules within the STS Chain Template 
                            referenced in the STS Chain. A property has the format `{"name":"STS Property","value":["demo","values"]}`
            partner_properties (:obj:`list` of :obj:`dict`): The partner properties for all modules within the STS Chain Template 
                            referenced in the STS Chain. A property has the format `{"name":"STS Property","value":["demo","values"]}`

        """
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("chainId", template_id)
        data.add_value_string("requestType", request_type)
        data.add_value_string("tokenType", token_type)
        data.add_value_string("xPath", xpath)

        signKey = DataObject()
        signKey.add_value_string("keyAlias_db", sign_key_store)
        signKey.add_value_string("keyAlias_cert", sign_key_alias)
        signKey.add_value_boolean("includeCertificateData", sign_include_cert)
        signKey.add_value_boolean("includePublicKey", sign_include_pubkey)
        signKey.add_value_boolean("includeSubjectKeyIdentifier", sign_include_ski)
        signKey.add_value_boolean("includeIssuerDetails", sign_include_issuer)
        signKey.add_value_boolean("includeSubjectName", sign_include_subject)

        validKey = DataObject()
        validKey.add_value_string("keyAlias_db", validation_key_store)
        validKey.add_value_string("keyAlias_cert", validation_key_alias)
        validKey.add_value_boolean("includeCertificateData", validation_include_cert)
        validKey.add_value_boolean("includePublicKey", validation_include_pubkey)
        validKey.add_value_boolean("includeSubjectKeyIdentifier", validation_include_ski)
        validKey.add_value_boolean("includeIssuerDetails", validation_include_issuer)
        validKey.add_value_boolean("includeSubjectName", validation_include_subject)


        applies_to = DataObject()
        applies_to.add_value_string("address", applies_to_address)
        applies_to.add_value_string("portTypeNamespace", applies_to_port_type_namespace)
        applies_to.add_value_string("portTypeName", applies_to_port_type_name)
        applies_to.add_value_string("serviceNamespace", applies_to_service_namespace)
        applies_to.add_value_string("serviceName", applies_to_service_name)
        data.add_value("appliesTo", applies_to.data)

        issuer = DataObject()
        issuer.add_value_string("address", issuer_address)
        issuer.add_value_string("portTypeNamespace", issuer_port_type_namespace)
        issuer.add_value_string("portTypeName", issuer_port_type_name)
        issuer.add_value_string("serviceNamespace", issuer_service_namespace)
        issuer.add_value_string("serviceName", issuer_service_name)
        data.add_value("issuer", issuer.data)

        data.add_value_boolean("validateRequests", validate_requests)
        data.add_value_not_empty("validationKey", validKey.data)
        data.add_value_boolean("signResponses", sign_responses)
        data.add_value_string("signatureKey", signKey.data)
        data.add_value_boolean("sendValidationConfirmation", send_validation_confirmation)

        properties = DataObject()
        properties.add_value_not_empty("self", self_properties)
        properties.add_value_not_empty("partner", partner_properties)
        data.add_value("properties", properties.data)

        endpoint = "{}/{}".format(STS_CHAINS, chain_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response
