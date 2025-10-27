"""
@copyright: IBM
"""

import ntpath
import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


FIDO2_RELYING_PARTIES="/iam/access/v8/fido2/relying-parties"
FIDO2_METADATA="/iam/access/v8/fido2/metadata"
FIDO2_METADATA_SERVICE="/iam/access/v8/fido2/metadata-services"
FIDO2_MEDIATOR="/iam/access/v8/mapping-rules"

logger = logging.getLogger(__name__)


class FIDO2Config(object):

    def __init__(self, base_url, username, password):
        super(FIDO2Config, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def list_relying_parties(self):
        '''
        Get a list of all the configured FIDO2 relying parties.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the FIDO2 relying parties are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        response = self.client.get_json(FIDO2_RELYING_PARTIES)
        response.success = response.status_code == 200

        return response


    def get_relying_party(self, rp_id):
        '''
        Get the configuration of a FIDO2 relying party.

        Args:
            rp_id (:obj:`str`): The id of the FIDO2 relying party.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the FIDO2 relying party is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = "{}/{}".format(FIDO2_RELYING_PARTIES, rp_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create_relying_party(self, name=None, rp_id=None, origins=None, metadata_set=[], metadata_soft_fail=True,
            mediator_mapping_rule_id=None, attestation_statement_types=None, attestation_statement_formats=None,
            attestation_public_key_algorithms=None, attestation_android_safetynet_max_age=None,
            attestation_android_safetynet_clock_skew=None, attestation_android_safetynet_cts_match=None,
            relying_party_impersonation_group=None, compound_all_valid=None, timeout=None,
            metadata_services=[]):
        '''
        Create a FIDO2 relying party.

        Args:
            name (:obj:`str`): Name of relying party.
            rp_id (:obj:`str`): The domain that the relying party acts for This should be a valid domain name.
            origins (:obj:`list` of :obj:`str`): List of allowed origins for he relying party. 
                                    Origins must be a valid URI and https origins should be a subdomain of the ``rp_id``.
            metadata_set (:obj:`list` of :obj:`str`): List of document id's to included as metadata.
            metadata_soft_fail (bool): Flag to indicate if a registration attempt should fail if metadata cannot be found.
            mediator_mapping_rule_id (:obj:`str`): The id of the FIDO JavaScript mapping rule to use as a mediator.
            attestation_statement_types (:obj:`list` of :obj:`str`): List of allowed attestation types.
            attestation_statement_formats (:obj:`list` of :obj:`str`): List of allowed attestation formats.
            attestation_public_key_algorithms (:obj:`list` of :obj:`str`): List of supported cryptographic signing algorithms.
            attestation_android_safetynet_max_age (int): Length of time that an "android-safetynet" attestation is valid for.
            attestation_android_safetynet_clock_skew (int): Clock skew allowed for "android-safetynet" attestations.
            attestation_android_safetynet_cts_match (int): Enforce the Android Safetynet CTS Profile Match flag.
            relying_party_impersonation_group (:obj:`str`, optional): Group which permits users to perform FIDO flows on behalf of another user.
            compound_all_valid (`bool`, optional): True if all attestation statements in a compound attestatation must
                                                    be valid to successfully register a given authenticator. Only
                                                    valid if ``compound`` is included in ``attestation_statement_formats``.
            timeout (`int`, optional): Lenght of time a user has to complete a FIDO2/WebAuthn ceremony. 
                                        Default value is 300 seconds (5 mins).
            metadata_services (:obj:`list` of :obj:`str`): List of MDS id's to included as metadata providers.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created FIDO2 relying party can be accessed from the 
            response.id_from_location attribute

        '''
        data = DataObject()
        data.add_value("name", name)
        data.add_value("rpId", rp_id)

        fidoServerOptions = DataObject()
        fidoServerOptions.add_value("timeout", timeout)
        fidoServerOptions.add_value_not_empty("origins", origins)
        fidoServerOptions.add_value("metadataSet", metadata_set)
        fidoServerOptions.add_value("metadataServices", metadata_services)
        fidoServerOptions.add_value_boolean("metadataSoftFail", metadata_soft_fail)
        fidoServerOptions.add_value_string("mediatorMappingRuleId", mediator_mapping_rule_id)

        attestation = DataObject()
        attestation.add_value_not_empty("statementTypes", attestation_statement_types)
        attestation.add_value_not_empty("statementFormats", attestation_statement_formats)
        attestation.add_value_not_empty("publicKeyAlgorithms", attestation_public_key_algorithms)
        attestation.add_value_boolean("compoundAttestationAllValid", compound_all_valid)
        fidoServerOptions.add_value_not_empty("attestation", attestation.data)

        attestationAndroidSafetyNetOptions = DataObject()
        attestationAndroidSafetyNetOptions.add_value("attestationMaxAge", attestation_android_safetynet_max_age)
        attestationAndroidSafetyNetOptions.add_value("clockSkew", attestation_android_safetynet_clock_skew)
        attestationAndroidSafetyNetOptions.add_value_boolean("ctsProfileMatch", attestation_android_safetynet_cts_match)
        fidoServerOptions.add_value_not_empty("android-safetynet", attestationAndroidSafetyNetOptions.data)

        data.add_value("fidoServerOptions", fidoServerOptions.data)

        relyingPartyOptions = DataObject()
        relyingPartyOptions.add_value("impersonationGroup", relying_party_impersonation_group)
        data.add_value("relyingPartyOptions", relyingPartyOptions.data)

        response = self.client.post_json(FIDO2_RELYING_PARTIES, data.data)
        response.success = response.status_code == 201

        return response


    def update_relying_party(self, id, name=None, rp_id=None, origins=None, metadata_set=[], metadata_soft_fail=True,
            mediator_mapping_rule_id=None, attestation_statement_types=None, attestation_statement_formats=None,
            attestation_public_key_algorithms=None, attestation_android_safety_net_max_age=None,
            attestation_android_safetynet_clock_skew=None, attestation_android_safetynet_cts_match=None,
            relying_party_impersonation_group=None, compound_all_valid=None, timeout=None,
            metadata_services=[]):
        '''
        Update a FIDO2 relying party.

        Args:
            name (:obj:`str`): Name of relying party.
            rp_id (:obj:`str`): The domain that the relying party acts for This should be a valid domain name.
            origins (:obj:`list` of :obj:`str`): List of allowed origins for he relying party. 
                                    Origins must be a valid URI and https origins should be a subdomain of the ``rp_id``.
            metadata_set (:obj:`list` of :obj:`str`): List of document id's to included as metadata.
            metadata_soft_fail (bool): Flag o indicate if a registration attempt should fail if metadata cannot be found.
            mediator_mapping_rule_id (:obj:`str`): The id of the FIDO JavaScript mapping rule to use as a mediator.
            attestation_statement_types (:obj:`list` of :obj:`str`): List of allowed attestation types.
            attestation_statement_formats (:obj:`list` of :obj:`str`): List of allowed attestation formats.
            attestation_public_key_algorithms (:obj:`list` of :obj:`str`): List of supported cryptographic signing algorithms.
            attestation_android_safetynet_max_age (int): Length of time that an "android-safetynet" attestation is valid for.
            attestation_android_safetynet_clock_skew (int): Clock skew allowed for "android-safetynet" attestations.
            attestation_android_safetynet_cts_match (int): Enforce the Android Safetynet CTS Profile Match flag.
            relying_party_impersonation_group (:obj:`str`): Group which permits users to perform FIDO flows on behalf of another user.
            compound_all_valid (`bool`, optional): True if all attestation statements in a compound attestatation must
                                                    be valid to successfully register a given authenticator. Only
                                                    valid if ``compound`` is included in ``attestation_statement_formats``.
            timeout (`int`, optional): Lenght of time a user has to complete a FIDO2/WebAuthn ceremony. 
                                        Default value is 300 seconds (5 mins).
            metadata_services (:obj:`list` of :obj:`str`): List of MDS id's to included as metadata providers.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("id", id)
        data.add_value_string("name", name)
        data.add_value_string("rpId", rp_id)

        fidoServerOptions = DataObject()
        fidoServerOptions.add_value("timeout", timeout)
        fidoServerOptions.add_value_not_empty("origins", origins)
        fidoServerOptions.add_value("metadataSet", metadata_set)
        fidoServerOptions.add_value("metadataServices", metadata_services)
        fidoServerOptions.add_value_boolean("metadataSoftFail", metadata_soft_fail)
        fidoServerOptions.add_value_string("mediatorMappingRuleId", mediator_mapping_rule_id)

        attestation = DataObject()
        attestation.add_value_not_empty("statementTypes", attestation_statement_types)
        attestation.add_value_not_empty("statementFormats", attestation_statement_formats)
        attestation.add_value_not_empty("publicKeyAlgorithms", attestation_public_key_algorithms)
        attestation.add_value_not_empty("publicKeyAlgorithms", attestation_public_key_algorithms)
        attestation.add_value_boolean("compoundAttestationAllValid", compound_all_valid)
        fidoServerOptions.add_value("attestation", attestation.data)

        attestationAndroidSafetyNetOptions = DataObject()
        attestationAndroidSafetyNetOptions.add_value("attestationMaxAge", attestation_android_safety_net_max_age)
        attestationAndroidSafetyNetOptions.add_value("clockSkew", attestation_android_safetynet_clock_skew)
        attestationAndroidSafetyNetOptions.add_value_boolean("ctsProfileMatch", attestation_android_safetynet_cts_match)
        fidoServerOptions.add_value("android-safetynet", attestationAndroidSafetyNetOptions.data)

        data.add_value("fidoServerOptions", fidoServerOptions.data)

        relyingPartyOptions = DataObject()
        relyingPartyOptions.add_value("impersonationGroup", relying_party_impersonation_group)
        data.add_value("relyingPartyOptions", relyingPartyOptions.data)

        endpoint = "%s/%s" % (FIDO2_RELYING_PARTIES, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete_relying_party(self, rp_id):
        '''
        Delete an existing FIDO2 relying party.

        Args:
            rp_id (:obj:`str`): The id of the FIDO2 relying party.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "{}/{}".format(FIDO2_RELYING_PARTIES, rp_id)
        response = self.client.delete_json(endpoint)
        response.success =response.status_code == 204

        return response


    def list_metadata(self):
        '''
        Get a list of all the configured metadata documents.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the metadata documents are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        response = self.client.get_json(FIDO2_METADATA)
        response.success = response.status_code == 200

        return response


    def get_metadata(self, metadata_id):
        '''
        Get a configured metadata documents.

        Arg:
            metadata_id (:obj:`str`): The id of the metadata document to get.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the metadata document is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = "{}/{}".format(FIDO2_METADATA, metadata_id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create_metadata(self, filename=None):
        '''
        Create a metadata document from a file.

        Args:
            filename (:obj:`str`): Absolute path to a FIDO2 Metadata document

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created metadata can be accessed from the 
            response.id_from_location attribute.

        '''
        response = Response()
        if not filename:
            setattr(response, 'status_code', 404)
            setattr(response, 'content', 'No volume specified')
            setattr(response, 'success', False)
            return response

        try:
            with open(filename, 'rb') as content:
                data = DataObject()
                data.add_value_string("filename", ntpath.basename(filename))
                data.add_value_string("contents", content.read().decode('utf-8'))

                endpoint = FIDO2_METADATA

                response = self.client.post_json(endpoint, data.data)
                response.success = response.status_code == 201

        except IOError as e:
            logger.error(e)
            response.success = False

        return response


    def update_metadata(self, metadata_id, filename=None):
        '''
        Update an existing metadata document from a file.

        Args:
            metadata_id (:obj:`str`): The id of the FIDO2 metadata document to be updated.
            filename (:obj:`str`): Absolute path to a FIDO2 Metadata document.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        response = Response()
        if not filename:
            setattr(response, 'status_code', 404)
            setattr(response, 'content', 'No volume specified')
            setattr(response, 'success', False)
            return response

        try:
            with open(filename, 'rb') as content:
                files = {"file": content}

                endpoint = ("%s/%s/file" % (FIDO2_METADATA, metadata_id))

                response = self.client.post_file(endpoint, accept_type="application/json,text/html,application/*", files=files)
                response.success = response.status_code == 200

        except IOError as e:
            logger.error(e)
            response.success = False

        return response


    def delete_metadata(self, metadata_id):
        '''
        Remove an existing metadata document from the store

        Args:
            metadata_id (:obj:`str`): The id of the metadata document to be removed.

        Returns
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = ("%s/%s/file" % (FIDO2_METADATA, id))

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204


    def create_mediator(self, name=None, filename=None):
        '''
        Create a FIDO2 mediator JavaScript mapping rule.

        Args:
            name (:obj:`str`): The name of the mapping rule to be created.
            filename (:obj:`str`): The contents of the mapping rule.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created mediator can be access from the 
            response.id_from_location attribute.

        '''
        response = Response()
        if not filename:
            setattr(response, 'status_code', 404)
            setattr(response, 'content', 'No volume specified')
            setattr(response, 'success', False)
            return response

        try:
            with open(filename, 'rb') as content:
                data = DataObject()
                data.add_value_string("filename", ntpath.basename(filename))
                data.add_value_string("content", content.read().decode('utf-8'))
                data.add_value_string("type", "FIDO2")
                data.add_value_string("name", name)

                response = self.client.post_json(FIDO2_MEDIATOR, data.data)
                response.success = response.status_code == 201

        except IOError as e:
            logger.error(e)
            response.success = False

        return response


    def update_mediator(self, mediator_id, filename=None):
        '''
        Update an existing mediator mapping rule with new contents

        Args:
            mediator_id (:obj:`str`): The id of the existing mapping rule.
            filename (:obj:`str`): Absolute path to the file containing the new mapping rule contents.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        response = Response()
        if not filename:
            setattr(response, 'status_code', 404)
            setattr(response, 'content', 'No volume specified')
            setattr(response, 'success', False)
            return response

        try:
            with open(filename, 'rb') as content:
                data = DataObject()
                data.add_value_string("content", content.read().decode('utf-8'))

                endpoint = ("%s/%s" % (FIDO2_MEDIATOR, id))

                response = self.client.put_json(endpoint, data.data)
                response.success = response.status_code == 204

        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def get_mediator(self, mediator_id):
        '''
        Get the contents of a configured mediator.

        Args:
            mediator_id (:obj:`str`): The id of the mediator to return.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the mediator is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = ("%s/%s" % (FIDO2_MEDIATOR, mediator_id))
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_mediators(self):
        '''
        Get a list of all of the configured mediators.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the metadata document is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        response = self.client.get_json(FIDO2_MEDIATOR)
        response.success = response.status_code == 200

        return response


    def delete_mediator(self, mediator_id):
        '''
        Remove a configured mediator mapping rule.

        Args:
            mediator_id (:obj:`str`): The id of the mediator mapping rule to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = ("%s/%s" % (FIDO2_MEDIATOR, mediator_id))
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def create_metadata_service(self, url, retry_interval=None, jws_truststore=None, truststore=None, username=None,
            password=None, keystore=None, certificate=None, protocol=None, timeout=None, proxy=None, headers=[]) -> Response:
        '''
        Create a FIDO2 Metadata Service connection.

        Args:
            url (:obj:`str`): The URL used to connect to the metadata service (including the protocol).
            retry_interval (`int`): When the lifetime of a downloaded metadata has expired and a request to retrieve the new metadata fails, this defines the wait 
                                    interval (in seconds) before retrying the download. If not specified the default value of 3600 seconds will be used. A value of 
                                    0 will result in a retry on each attestation validation.
            jws_truststore (:obj:`str`): The name of the JWS verification truststore. The truststore contains the certificate used to verify the signature of the 
                                         downloaded metadata blob. If not specified the SSL trust store or the trust store configured in the HTTPClientV2 advanced 
                                         configuration will be used.
            truststore (:obj:`str`): The name of the truststore to use. The truststore has a dual purpose. Firstly it is used when making a HTTPS connection to the 
                                     Metadata Service. Secondly if the ``jws_truststore`` is not specified it must contain the certificate used to verify the signature of 
                                     the downloaded metadata blob. If not specified and a HTTPS connection is specified, the trust store configured in the HTTPClientV2 
                                     advanced configuration will be used.
            username (:obj:`str`): The basic authentication username. If not specified BA will not be used.
            password (:obj:`str`): The basic authentication password. If not specified BA will not be used.
            keystore (:obj:`str`): The client keystore. If not specified client certificate authentication will not be used.
            protocol (:obj:`str`): The SSL protocol to use for the HTTPS connection. Valid values are TLS, TLSv1, TLSv1.1 and TLSv1.2. If not specified the protocol 
                                   configured in the HTTPClientV2 advanced configuration will be used.
            timeout (int): The request timeout in seconds. A value of 0 will result in no timeout. If not specified the connect timeout configured in the HTTPClientV2 
                           advanced configuration will be used.
            proxy (:obj:`str`): Yes	The URL of the proxy server used to connect to the metadata service (including the protocol).
            headers (:obj:`list` of :obj:`str`): A list of HTTP headers to be added to the HTTP request when retrieving the metadata from the service.


        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created FIDO2 metadata service can be accessed from the 
            response.id_from_location attribute

        '''
        raise Exception ("Not yet implemented")


    def update_metadata_service(self, mds_id, url=None, retry_interval=None, jws_truststore=None, truststore=None, username=None,
            password=None, keystore=None, certificate=None, protocol=None, timeout=None, proxy=None, headers=[]) -> Response:
        '''
        Update an existing FIDO2 Metadata Service connection.

        Args:
            mds_id (:obj:`str`): The Verify Identity Access assigned identifier.
            url (:obj:`str`): The URL used to connect to the metadata service (including the protocol).
            retry_interval (`int`): When the lifetime of a downloaded metadata has expired and a request to retrieve the new metadata fails, this defines the wait 
                                    interval (in seconds) before retrying the download. If not specified the default value of 3600 seconds will be used. A value of 
                                    0 will result in a retry on each attestation validation.
            jws_truststore (:obj:`str`): The name of the JWS verification truststore. The truststore contains the certificate used to verify the signature of the 
                                         downloaded metadata blob. If not specified the SSL trust store or the trust store configured in the HTTPClientV2 advanced 
                                         configuration will be used.
            truststore (:obj:`str`): The name of the truststore to use. The truststore has a dual purpose. Firstly it is used when making a HTTPS connection to the 
                                     Metadata Service. Secondly if the ``jws_truststore`` is not specified it must contain the certificate used to verify the signature of 
                                     the downloaded metadata blob. If not specified and a HTTPS connection is specified, the trust store configured in the HTTPClientV2 
                                     advanced configuration will be used.
            username (:obj:`str`): The basic authentication username. If not specified BA will not be used.
            password (:obj:`str`): The basic authentication password. If not specified BA will not be used.
            keystore (:obj:`str`): The client keystore. If not specified client certificate authentication will not be used.
            protocol (:obj:`str`): The SSL protocol to use for the HTTPS connection. Valid values are TLS, TLSv1, TLSv1.1 and TLSv1.2. If not specified the protocol 
                                   configured in the HTTPClientV2 advanced configuration will be used.
            timeout (int): The request timeout in seconds. A value of 0 will result in no timeout. If not specified the connect timeout configured in the HTTPClientV2 
                           advanced configuration will be used.
            proxy (:obj:`str`): Yes	The URL of the proxy server used to connect to the metadata service (including the protocol).
            headers (:obj:`list` of :obj:`str`): A list of HTTP headers to be added to the HTTP request when retrieving the metadata from the service.


        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        raise Exception ("Not yet implemented")


    def get_metadata_service(self, mds_id) -> Response:
        '''
        Get a configured metadata service.

        Args:
            mds_id (:obj:`str`): The Verify Identity Access assigned identifier.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the metadata service is returned as JSON and can be accessed from
            the response.json attribute.
        '''
        raise Exception ("Not yet implemented")


    def list_metadata_services(self) -> Response:
        '''
        List the configured metadata services.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the metadata services are returned as JSON and can be accessed from
            the response.json attribute.        
        '''
        raise Exception ("Not yet implemented")


    def delete_metadata_service(self, mds_id) -> Response:
        '''
        Delete a configured metadata service.

        Args:
            mds_id (:obj:`str`): The Verify Identity Access assigned identifier.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        raise Exception ("Not yet implemented")


class FIDO2Config10050(FIDO2Config):

    def __init__(self, base_url, username, password):
        super(FIDO2Config10050, self).__init__(base_url, username, password)

    def create_relying_party(self, name=None, rp_id=None, origins=None, metadata_set=[], metadata_soft_fail=True,
            mediator_mapping_rule_id=None, attestation_statement_types=None, attestation_statement_formats=None,
            attestation_public_key_algorithms=None, attestation_android_safetynet_max_age=None,
            attestation_android_safetynet_clock_skew=None, attestation_android_safetynet_cts_match=None,
            relying_party_impersonation_group=None, compound_all_valid=None, timeout=None, metadata_services=[]):
        '''
        Create a FIDO2 relying party.

        Args:
            name (:obj:`str`): Name of relying party.
            rp_id (:obj:`str`): The domain that the relying party acts for This should be a valid domain name.
            origins (:obj:`list` of :obj:`str`): List of allowed origins for he relying party. 
                                    Origins must be a valid URI and https origins should be a subdomain of the ``rp_id``.
            metadata_set (:obj:`list` of :obj:`str`): List of document id's to included as metadata.
            metadata_soft_fail (bool): Flag to indicate if a registration attempt should fail if metadata cannot be found.
            mediator_mapping_rule_id (:obj:`str`): The id of the FIDO JavaScript mapping rule to use as a mediator.
            attestation_statement_types (:obj:`list` of :obj:`str`): List of allowed attestation types.
            attestation_statement_formats (:obj:`list` of :obj:`str`): List of allowed attestation formats.
            attestation_public_key_algorithms (:obj:`list` of :obj:`str`): List of supported cryptographic signing algorithms.
            attestation_android_safetynet_max_age (int): Length of time that an "android-safetynet" attestation is valid for.
            attestation_android_safetynet_clock_skew (int): Clock skew allowed for "android-safetynet" attestations.
            attestation_android_safetynet_cts_match (int): Enforce the Android Safetynet CTS Profile Match flag.
            relying_party_impersonation_group (:obj:`str`, optional): Group which permits users to perform FIDO flows on behalf of another user.
            metadata_services (:obj:`list` of :obj:`str`): A list of FIDO2 Metadata service ID's that this FIDO2 Relying Party will use to retrieve metadata used for attestation validation. Can be empty to indicate no metadata service will be used.
            compound_all_valid (`bool`, optional): True if all attestation statements in a compound attestatation must
                                                    be valid to successfully register a given authenticator. Only
                                                    valid if ``compound`` is included in ``attestation_statement_formats``.
            timeout (`int`, optional): Lenght of time a user has to complete a FIDO2/WebAuthn ceremony. 
                                        Default value is 300 seconds (5 mins).


        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created FIDO2 relying party can be accessed from the 
            response.id_from_location attribute

        '''
        data = DataObject()
        data.add_value("name", name)
        data.add_value("rpId", rp_id)

        fidoServerOptions = DataObject()
        fidoServerOptions.add_value("timeout", timeout)
        fidoServerOptions.add_value_not_empty("origins", origins)
        fidoServerOptions.add_value("metadataSet", metadata_set)
        fidoServerOptions.add_value("metadataServices", metadata_services)
        fidoServerOptions.add_value_boolean("metadataSoftFail", metadata_soft_fail)
        fidoServerOptions.add_value_string("mediatorMappingRuleId", mediator_mapping_rule_id)

        attestation = DataObject()
        attestation.add_value_not_empty("statementTypes", attestation_statement_types)
        attestation.add_value_not_empty("statementFormats", attestation_statement_formats)
        attestation.add_value_not_empty("publicKeyAlgorithms", attestation_public_key_algorithms)
        attestation.add_value_boolean("compoundAttestationAllValid", compound_all_valid)
        fidoServerOptions.add_value_not_empty("attestation", attestation.data)

        attestationAndroidSafetyNetOptions = DataObject()
        attestationAndroidSafetyNetOptions.add_value("attestationMaxAge", attestation_android_safetynet_max_age)
        attestationAndroidSafetyNetOptions.add_value("clockSkew", attestation_android_safetynet_clock_skew)
        attestationAndroidSafetyNetOptions.add_value_boolean("ctsProfileMatch", attestation_android_safetynet_cts_match)
        fidoServerOptions.add_value_not_empty("android-safetynet", attestationAndroidSafetyNetOptions.data)

        data.add_value("fidoServerOptions", fidoServerOptions.data)

        relyingPartyOptions = DataObject()
        relyingPartyOptions.add_value("impersonationGroup", relying_party_impersonation_group)
        data.add_value("relyingPartyOptions", relyingPartyOptions.data)

        logger.debug(data.data)
        response = self.client.post_json(FIDO2_RELYING_PARTIES, data.data)
        response.success = response.status_code == 201

        return response


    def update_relying_party(self, id, name=None, rp_id=None, origins=None, metadata_set=[], metadata_soft_fail=True,
            mediator_mapping_rule_id=None, attestation_statement_types=None, attestation_statement_formats=None,
            attestation_public_key_algorithms=None, attestation_android_safety_net_max_age=None,
            attestation_android_safetynet_clock_skew=None, attestation_android_safetynet_cts_match=None,
            relying_party_impersonation_group=None, compound_all_valid=None, timeout=None, metadata_services=[]):
        '''
        Update a FIDO2 relying party.

        Args:
            name (:obj:`str`): Name of relying party.
            rp_id (:obj:`str`): The domain that the relying party acts for This should be a valid domain name.
            origins (:obj:`list` of :obj:`str`): List of allowed origins for he relying party. 
                                    Origins must be a valid URI and https origins should be a subdomain of the ``rp_id``.
            metadata_set (:obj:`list` of :obj:`str`): List of document id's to included as metadata.
            metadata_soft_fail (bool): Flag o indicate if a registration attempt should fail if metadata cannot be found.
            mediator_mapping_rule_id (:obj:`str`): The id of the FIDO JavaScript mapping rule to use as a mediator.
            attestation_statement_types (:obj:`list` of :obj:`str`): List of allowed attestation types.
            attestation_statement_formats (:obj:`list` of :obj:`str`): List of allowed attestation formats.
            attestation_public_key_algorithms (:obj:`list` of :obj:`str`): List of supported cryptographic signing algorithms.
            attestation_android_safetynet_max_age (int): Length of time that an "android-safetynet" attestation is valid for.
            attestation_android_safetynet_clock_skew (int): Clock skew allowed for "android-safetynet" attestations.
            attestation_android_safetynet_cts_match (int): Enforce the Android Safetynet CTS Profile Match flag.
            relying_party_impersonation_group (:obj:`str`): Group which permits users to perform FIDO flows on behalf of another user.
            metadata_services (:obj:`list` of :obj:`str`): A list of FIDO2 Metadata service ID's that this FIDO2 Relying Party will use to retrieve metadata used for attestation validation. Can be empty to indicate no metadata service will be used.
            compound_all_valid (`bool`, optional): True if all attestation statements in a compound attestatation must
                                                    be valid to successfully register a given authenticator. Only
                                                    valid if ``compound`` is included in ``attestation_statement_formats``.
            timeout (`int`, optional): Lenght of time a user has to complete a FIDO2/WebAuthn ceremony. 
                                        Default value is 300 seconds (5 mins).

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("id", id)
        data.add_value_string("name", name)
        data.add_value_string("rpId", rp_id)

        fidoServerOptions = DataObject()
        fidoServerOptions.add_value("timeout", timeout)
        fidoServerOptions.add_value_not_empty("origins", origins)
        fidoServerOptions.add_value("metadataSet", metadata_set)
        fidoServerOptions.add_value("metadataServices", metadata_services)
        fidoServerOptions.add_value_boolean("metadataSoftFail", metadata_soft_fail)
        fidoServerOptions.add_value_string("mediatorMappingRuleId", mediator_mapping_rule_id)

        attestation = DataObject()
        attestation.add_value_not_empty("statementTypes", attestation_statement_types)
        attestation.add_value_not_empty("statementFormats", attestation_statement_formats)
        attestation.add_value_not_empty("publicKeyAlgorithms", attestation_public_key_algorithms)
        attestation.add_value_not_empty("publicKeyAlgorithms", attestation_public_key_algorithms)
        attestation.add_value_boolean("compoundAttestationAllValid", compound_all_valid)
        fidoServerOptions.add_value("attestation", attestation.data)

        attestationAndroidSafetyNetOptions = DataObject()
        attestationAndroidSafetyNetOptions.add_value("attestationMaxAge", attestation_android_safety_net_max_age)
        attestationAndroidSafetyNetOptions.add_value("clockSkew", attestation_android_safetynet_clock_skew)
        attestationAndroidSafetyNetOptions.add_value_boolean("ctsProfileMatch", attestation_android_safetynet_cts_match)
        fidoServerOptions.add_value("android-safetynet", attestationAndroidSafetyNetOptions.data)

        data.add_value("fidoServerOptions", fidoServerOptions.data)

        relyingPartyOptions = DataObject()
        relyingPartyOptions.add_value("impersonationGroup", relying_party_impersonation_group)
        data.add_value("relyingPartyOptions", relyingPartyOptions.data)

        endpoint = "%s/%s" % (FIDO2_RELYING_PARTIES, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response

    def create_metadata_service(self, url, retry_interval=None, jws_truststore=None, truststore=None, username=None,
            password=None, keystore=None, certificate=None, protocol=None, timeout=None, proxy=None, headers=[]):
        '''
        Create a FIDO2 Metadata Service connection.

        Args:
            url (:obj:`str`): The URL used to connect to the metadata service (including the protocol).
            retry_interval (`int`): When the lifetime of a downloaded metadata has expired and a request to retrieve the new metadata fails, this defines the wait 
                                    interval (in seconds) before retrying the download. If not specified the default value of 3600 seconds will be used. A value of 
                                    0 will result in a retry on each attestation validation.
            jws_truststore (:obj:`str`): The name of the JWS verification truststore. The truststore contains the certificate used to verify the signature of the 
                                         downloaded metadata blob. If not specified the SSL trust store or the trust store configured in the HTTPClientV2 advanced 
                                         configuration will be used.
            truststore (:obj:`str`): The name of the truststore to use. The truststore has a dual purpose. Firstly it is used when making a HTTPS connection to the 
                                     Metadata Service. Secondly if the ``jws_truststore`` is not specified it must contain the certificate used to verify the signature of 
                                     the downloaded metadata blob. If not specified and a HTTPS connection is specified, the trust store configured in the HTTPClientV2 
                                     advanced configuration will be used.
            username (:obj:`str`): The basic authentication username. If not specified BA will not be used.
            password (:obj:`str`): The basic authentication password. If not specified BA will not be used.
            keystore (:obj:`str`): The client keystore. If not specified client certificate authentication will not be used.
            protocol (:obj:`str`): The SSL protocol to use for the HTTPS connection. Valid values are TLS, TLSv1, TLSv1.1 and TLSv1.2. If not specified the protocol 
                                   configured in the HTTPClientV2 advanced configuration will be used.
            timeout (int): The request timeout in seconds. A value of 0 will result in no timeout. If not specified the connect timeout configured in the HTTPClientV2 
                           advanced configuration will be used.
            proxy (:obj:`str`): Yes	The URL of the proxy server used to connect to the metadata service (including the protocol).
            headers (:obj:`list` of :obj:`str`): A list of HTTP headers to be added to the HTTP request when retrieving the metadata from the service.


        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created FIDO2 metadata service can be accessed from the 
            response.id_from_location attribute

        '''
        data = DataObject()
        data.add_value_string("url", url)
        data.add_value("retryInterval", retry_interval)
        data.add_value_string("jwsTruststore", jws_truststore)
        data.add_value_string("truststore", truststore)
        data.add_value_string("username", username)
        data.add_value_string("password", password)
        data.add_value_string("keystore", keystore)
        data.add_value_string("certificate", certificate)
        data.add_value_string("protocol", protocol)
        data.add_value("timeout", timeout)
        data.add_value_string("proxy", proxy)
        data.add_value_not_empty("headers", headers)

        response = self.client.post_json(FIDO2_METADATA_SERVICE, data.data)
        response.success = response.status_code == 201

        return response


    def update_metadata_service(self, mds_id, url=None, retry_interval=None, jws_truststore=None, truststore=None, username=None,
            password=None, keystore=None, certificate=None, protocol=None, timeout=None, proxy=None, headers=[]) -> Response:
        '''
        Update an existing FIDO2 Metadata Service connection.

        Args:
            mds_id (:obj:`str`): The Verify Identity Access assigned identifier.
            url (:obj:`str`): The URL used to connect to the metadata service (including the protocol).
            retry_interval (`int`): When the lifetime of a downloaded metadata has expired and a request to retrieve the new metadata fails, this defines the wait 
                                    interval (in seconds) before retrying the download. If not specified the default value of 3600 seconds will be used. A value of 
                                    0 will result in a retry on each attestation validation.
            jws_truststore (:obj:`str`): The name of the JWS verification truststore. The truststore contains the certificate used to verify the signature of the 
                                         downloaded metadata blob. If not specified the SSL trust store or the trust store configured in the HTTPClientV2 advanced 
                                         configuration will be used.
            truststore (:obj:`str`): The name of the truststore to use. The truststore has a dual purpose. Firstly it is used when making a HTTPS connection to the 
                                     Metadata Service. Secondly if the ``jws_truststore`` is not specified it must contain the certificate used to verify the signature of 
                                     the downloaded metadata blob. If not specified and a HTTPS connection is specified, the trust store configured in the HTTPClientV2 
                                     advanced configuration will be used.
            username (:obj:`str`): The basic authentication username. If not specified BA will not be used.
            password (:obj:`str`): The basic authentication password. If not specified BA will not be used.
            keystore (:obj:`str`): The client keystore. If not specified client certificate authentication will not be used.
            protocol (:obj:`str`): The SSL protocol to use for the HTTPS connection. Valid values are TLS, TLSv1, TLSv1.1 and TLSv1.2. If not specified the protocol 
                                   configured in the HTTPClientV2 advanced configuration will be used.
            timeout (int): The request timeout in seconds. A value of 0 will result in no timeout. If not specified the connect timeout configured in the HTTPClientV2 
                           advanced configuration will be used.
            proxy (:obj:`str`): Yes	The URL of the proxy server used to connect to the metadata service (including the protocol).
            headers (:obj:`list` of :obj:`str`): A list of HTTP headers to be added to the HTTP request when retrieving the metadata from the service.


        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("url", url)
        data.add_value("retryInterval", retry_interval)
        data.add_value_string("jwsTruststore", jws_truststore)
        data.add_value_string("truststore", truststore)
        data.add_value_string("username", username)
        data.add_value_string("password", password)
        data.add_value_string("keystore", keystore)
        data.add_value_string("certificate", certificate)
        data.add_value_string("protocol", protocol)
        data.add_value("timeout", timeout)
        data.add_value_string("proxy", proxy)
        data.add_value_not_empty("headers", headers)

        endpoint = "{}/{}".format(FIDO2_METADATA_SERVICE, mds_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def get_metadata_service(self, mds_id) -> Response:
        '''
        Get a configured metadata service.

        Args:
            mds_id (:obj:`str`): The Verify Identity Access assigned identifier.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the metadata service is returned as JSON and can be accessed from
            the response.json attribute.
        '''
        endpoint = "{}/{}".format(FIDO2_METADATA_SERVICE, mds_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_metadata_services(self) -> Response:
        '''
        List the configured metadata services.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the metadata services are returned as JSON and can be accessed from
            the response.json attribute.        
        '''
        response = self.client.get_json(FIDO2_METADATA_SERVICE)
        response.success = response.status_code == 200

        return response


    def delete_metadata_service(self, mds_id) -> Response:
        '''
        Delete a configured metadata service.

        Args:
            mds_id (:obj:`str`): The Verify Identity Access assigned identifier.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = "{}/{}".format(FIDO2_METADATA_SERVICE, mds_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
