"""
@copyright: IBM
"""

import ntpath
import logging

from pyisva.util.model import DataObject, Response
from pyisva.util.restclient import RESTClient


"""
Allows basic management of FIDO2 relying party configurations and metadata
"""
FIDO2_RELYING_PARTIES="/iam/access/v8/fido2/relying-parties"
FIDO2_METADATA="/iam/access/v8/fido2/metadata"
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
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the relying parties are returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = self.client.get_json(FIDO2_RELYING_PARTIES)
        response.success = response.status_code == 200

        return response


    def get_relying_party(self, _id):
        '''
        Get the configuration of a FIDO2 relying party.

        Args:
            _id (:obj:`str`): The id of the FIDO2 relying party.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the relying party is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = "{}/{}".format(FIDO2_RELYING_PARTIES, _id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create_relying_party(self, name=None, rp_id=None, origins=None, metadata_set=None, metadata_soft_fail=True,
            mediator_mapping_rule_id=None, attestation_statement_types=None, attestation_statement_formats=None,
            attestation_public_key_algorithms=None, attestation_android_safetynet_max_age=None,
            attestation_android_safetynet_clock_skew=None, relying_party_impersonation_group="adminGroup"):
        '''
        Create a FIDO2 relying party.

        Args:
            name (:obj:`str`): Name of relying party.
            rp_id (:obj:`str`): The domain that the relying aprty acts for This shold be a valid domain name.
            origins (:obj:`list` of :obj:`str`): List of allowed origns for he relying party. 
                                    Origins must be a valid URI and https origins should be a subdomain of the ``rp_id``.
            metadata_set (:obj:`list` of :obj:`str`): List of document id's to included as metadata.
            metadata_soft_fail (bool): Flag o indicate if a registration attempt should fail if metadata cannot be found.
            mediator_mapping_rule_id (:obj:`str`): The id of the FIDO JavaScript mapping rule to use as a mediator.
            attestation_statement_types (:obj:`list` of :obj:`str`): List of allowed attestation types.
            attestation_statement_formats (:obj:`list` of :obj:`str`): List of allowed attestation formats.
            attestation_public_key_algorithms (:obj:`list` of :obj:`str`): List of supported cryptographic signing algorithms.
            attestation_android_safetynet_max_age (int): Length of time that an "android-safetynet" attestation is valid for.
            attestation_android_safetynet_clock_skew (int): Clock skew allowed for "android-safetynet" attestations.
            relying_party_impersonation_group (:obj:`str`): Group which permits users to perform FIDO flows on behalf of another user.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created obligation can be acess from the 
            response.id_from_location attribute

        '''
        data = DataObject()
        data.add_value("name", name)
        data.add_value("rpId", rp_id)

        fidoServerOptions = DataObject()
        fidoServerOptions.add_value_not_empty("origins", origins)
        fidoServerOptions.add_value("metadataSet", metadata_set)
        fidoServerOptions.add_value("metadataSoftFail", metadata_soft_fail)
        fidoServerOptions.add_value("mediatorMappingRuleId", mediator_mapping_rule_id)

        attestation = DataObject()
        attestation.add_value("statementTypes", attestation_statement_types)
        attestation.add_value("statementFormats", attestation_statement_formats)
        attestation.add_value("publicKeyAlgorithms", attestation_public_key_algorithms)
        fidoServerOptions.add_value("attestation", attestation.data)

        attestationAndroidSafetyNetOptions = DataObject()
        attestationAndroidSafetyNetOptions.add_value("attestationMaxAge", attestation_android_safetynet_max_age)
        attestationAndroidSafetyNetOptions.add_value("clockSkew", attestation_android_safetynet_clock_skew)
        fidoServerOptions.add_value("android-safetynet", attestationAndroidSafetyNetOptions.data)

        data.add_value("fidoServerOptions", fidoServerOptions.data)

        relyingPartyOptions = DataObject()
        relyingPartyOptions.add_value("impersonationGroup", relying_party_impersonation_group)
        data.add_value("relyingPartyOptions", relyingPartyOptions.data)

        response = self.client.post_json(FIDO2_RELYING_PARTIES, data.data)
        response.success = response.status_code == 201

        return response


    def update_relying_party(self, id, name=None, rp_id=None, origins=None, metadata_set=None, metadata_soft_fail=True,
            mediator_mapping_rule_id=None, attestation_statement_types=None, attestation_statement_formats=None,
            attestation_public_key_algorithms=None, attestation_android_safety_net_max_age=None,
            attestation_android_safetynet_clock_skew=None, relying_party_impersonation_group="adminGroup"):
        '''
        Update a FIDO2 relying party.

        Args:
            name (:obj:`str`): Name of relying party.
            rp_id (:obj:`str`): The domain that the relying aprty acts for This shold be a valid domain name.
            origins (:obj:`list` of :obj:`str`): List of allowed origns for he relying party. 
                                    Origins must be a valid URI and https origins should be a subdomain of the ``rp_id``.
            metadata_set (:obj:`list` of :obj:`str`): List of document id's to included as metadata.
            metadata_soft_fail (bool): Flag o indicate if a registration attempt should fail if metadata cannot be found.
            mediator_mapping_rule_id (:obj:`str`): The id of the FIDO JavaScript mapping rule to use as a mediator.
            attestation_statement_types (:obj:`list` of :obj:`str`): List of allowed attestation types.
            attestation_statement_formats (:obj:`list` of :obj:`str`): List of allowed attestation formats.
            attestation_public_key_algorithms (:obj:`list` of :obj:`str`): List of supported cryptographic signing algorithms.
            attestation_android_safetynet_max_age (int): Length of time that an "android-safetynet" attestation is valid for.
            attestation_android_safetynet_clock_skew (int): Clock skew allowed for "android-safetynet" attestations.
            relying_party_impersonation_group (:obj:`str`): Group which permits users to perform FIDO flows on behalf of another user.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value("id", id)
        data.add_value("name", name)
        data.add_value("rpId", rp_id)

        fidoServerOptions = DataObject()
        fidoServerOptions.add_value_not_empty("origins", origins)
        fidoServerOptions.add_value("metadataSet", metadata_set)
        fidoServerOptions.add_value("metadataSoftFail", metadata_soft_fail)
        fidoServerOptions.add_value("mediatorMappingRuleId", mediator_mapping_rule_id)

        attestation = DataObject()
        attestation.add_value("statementTypes", attestation_statement_types)
        attestation.add_value("statementFormats", attestation_statement_formats)
        attestation.add_value("publicKeyAlgorithms", attestation_public_key_algorithms)
        attestation.add_value("publicKeyAlgorithms", attestation_public_key_algorithms)
        fidoServerOptions.add_value("attestation", attestation.data)

        attestationAndroidSafetyNetOptions = DataObject()
        attestationAndroidSafetyNetOptions.add_value("attestationMaxAge", attestation_android_safetynet_max_age)
        attestationAndroidSafetyNetOptions.add_value("clockSkew", attestation_android_safetynet_clock_skew)
        fidoServerOptions.add_value("android-safetynet", attestationAndroidSafetyNetOptions.data)

        data.add_value("fidoServerOptions", fidoServerOptions.data)

        relyingPartyOptions = DataObject()
        relyingPartyOptions.add_value("impersonationGroup", relying_party_impersonation_group)
        data.add_value("relyingPartyOptions", relyingPartyOptions.data)

        endpoint = "%s/%s" % (FIDO2_RELYING_PARTIES, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def list_metadata(self):
        '''
        Get a list of all the configured metadata documents.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the metadata documents are returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = FIDO2_METADATA

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_metadata(self, _id):
        '''
        Get a configured metadata documents.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the metadata document is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = "{}/{}".format(FIDO2_METADATA, _id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create_metadata(self, filename=None):
        '''
        Create a metadata document from a file.

        Args:
            filename (:obj:`str`): Absolute path to a FIDO2 Metadata document

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created metadata can be acess from the 
            response.id_from_location attribute

        '''
        response = Response()
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

    def update_metadata(self, id, filename=None):
        '''
        Update an existing metadata document from a file.

        Args:
            id (:obj:`str`): The id of the FIDO2 metadata docuemtn to be updated.
            filename (:obj:`str`): Absolute path to a FIDO2 Metadata document.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        response = Response()
        try:
            with open(filename, 'rb') as content:
                files = {"file": content}

                endpoint = ("%s/%s/file" % (FIDO2_METADATA, id))

                response = self.client.post_file(endpoint, accept_type="application/json,text/html,application/*", files=files)
                response.success = response.status_code == 200

        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def delete_metadata(self, id):
        '''
        Remove an existing metadata documetn from the store

        Args:
            id (:obj:`str`): The id of the metadata document to be removed.

        Returns
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = ("%s/%s/file" % (FIDO2_METADATA, id))

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

    def create_mediator(self, name=None, filename=None):
        '''
        Create a FDIO2 mediator JavaScript mapping rule.

        Args:
            name (:obj:`str`): The name of the mapping rule to be created.
            filename (:obj:`str`): The contents of the mapping rule.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created mediator can be acess from the 
            response.id_from_location attribute
        '''
        response = Response()
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

    def update_mediator(self, id, filename=None):
        '''
        Update an exisiting mediator mapping rule with new contents

        Args:
            id (:obj:`str`): The id of the existing mapping rule.
            filename (:obj:`str`): Absolute path to the file containing the new mapping rule contents.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        response = Response()
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

    def get_mediator(self, id):
        '''
        Get the contents of a configured mediator.

        Agrs:
            id (:obj:`str`): The id of the mediator to return.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the mediator is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = ("%s/%s" % (FIDO2_MEDIATOR, id))
        response = self.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def list_mediators(self):
        '''
        Get a list of all of the configured mediators.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the metadata document is returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = self.client.get_json(FIDO2_MEDIATOR)
        rsponse.success = response.status_code == 200

        return response


    def delete_mediator(self, id):
        '''
        Remove a configured mediator mapping rule.

        Args:
            id (:obj:`str`): The id of the mediator mapping rule to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = ("%s/%s" % (FIDO2_MEDIATOR, id))
        response = self.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
