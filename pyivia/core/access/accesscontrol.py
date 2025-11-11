"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


POLICIES = "/iam/access/v8/policies"
POLICY_ATTACHMENTS = "/iam/access/v8/policyattachments"
POLICY_ATTACHMENTS_PDADMIN = "/iam/access/v8/policyattachments/pdadmin"
OBLIGATIONS = "/iam/access/v8/obligations"
POLICY_SETS = '/iam/access/v8/policysets/'

logger = logging.getLogger(__name__)


class AccessControl(object):

    def __init__(self, base_url, username, password):
        super(AccessControl, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_policy(self, name=None, description=None, dialect="urn:oasis:names:tc:xacml:2.0:policy:schema:os", 
                    policy=None, attributes_required=False):
        '''
        Create an AAC Access Policy. 

        Args:
            name (:obj:`str`): Name of policy to be created.
            description (:obj:`str`, optional): Description of policy to be created
            dialect (:obj:`str`, optional): Format of policy XML. Only "urn:oasis:names:tc:xacml:2.0:policy:schema:os" is supported
            policy (:obj:`str`, optional): XML of policy steps.
            attributes_required (`bool`): True if all attributes msut be present in the request before
                                        the policy can be evaluated.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created policy can be access from the 
            response.id_from_location attribute.

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("dialect", dialect)
        data.add_value_string("policy", policy)
        data.add_value_boolean("predefined", False)
        data.add_value_boolean("attributesrequired", attributes_required)

        response = self.client.post_json(POLICIES, data.data)
        response.success = response.status_code == 201

        return response


    def delete_policy(self, id=None):
        '''
        Delete an AAC Access Policy.

        Args:
            id (:obj:`str`): Policy id to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "%s/%s" % (POLICIES, id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def list_policies(self, sort_by=None, filter=None):
        '''
        List all of the configured AAC Access Policies.

        Args:
            sort_by (:obj:`str`, optional): Optional sorting of returned policies
            filter (:obj:`str`, optional): Optional filter for returned policies

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the policies are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(POLICIES, parameters.data)
        response.success = response.status_code == 200

        return response


    def create_policy_set(self, name, description, predefined=False, policies=[], policy_combining_alg="denyOverrides"):
        '''
        Create an AAC Access Policy Set. 

        Args:
            name (:obj:`str`): Name of policy set to be created.
            description (:obj:`str`, optional): Description of policy set to be created
            predefined (`bool`, optional): False to indicate the policy set is custom defined.
            policies (:obj:`str`, optional): An array of policy IDs which belong to this policy set. The 
                                           order that the policies appear in this list is used when the 
                                           ``policy_combining_alg`` is set to "firstApplicable".
            policy_combining_alg (:obj:`str`, optional): Defines the combined action for the policies in 
                                                        the set. "firstApplicable" to indicate that the 
                                                        policy set will return the result of the first 
                                                        policy in the set that returns permit or deny, 
                                                        "denyOverrides" to indicate that the policy set 
                                                        should deny access if any policy in the set returns 
                                                        a response of deny , or "permitOverrides" to 
                                                        indicate that the policy set should permit access 
                                                        if any policy in the set returns a response of 
                                                        permit. Default is "denyOverrides". 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created policy set can be access from the 
            response.id_from_location attribute.

        '''
        parameters = DataObject()
        parameters.add_value_string("name", name)
        parameters.add_value_string("description", description)
        parameters.add_value_boolean("predefined", predefined)
        parameters.add_value("policies", policies)
        parameters.add_value_string("policyCombiningAlgorithm", policy_combining_alg)

        response = self.client.post_json(POLICY_SETS, parameters.data)
        response.success = response.status_code == 200

        return response


    def update_policy_set(self, set_id, name, description, predefined=False, policies=[], 
                          policy_combining_alg="denyOverrides"):
        '''
        Create an AAC Access Policy Set. 

        Args:
            name (:obj:`str`): Name of policy set to be created.
            description (:obj:`str`, optional): Description of policy set to be created
            predefined (`bool`, optional): False to indicate the policy set is custom defined.
            policies (:obj:`str`, optional): An array of policy IDs which belong to this policy set. The 
                                           order that the policies appear in this list is used when the 
                                           ``policy_combining_alg`` is set to "firstApplicable".
            policy_combining_alg (:obj:`str`, optional): Defines the combined action for the policies in 
                                                        the set. "firstApplicable" to indicate that the 
                                                        policy set will return the result of the first 
                                                        policy in the set that returns permit or deny, 
                                                        "denyOverrides" to indicate that the policy set 
                                                        should deny access if any policy in the set returns 
                                                        a response of deny , or "permitOverrides" to 
                                                        indicate that the policy set should permit access 
                                                        if any policy in the set returns a response of 
                                                        permit. Default is "denyOverrides". 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created policy set can be access from the 
            response.id_from_location attribute.

        '''
        parameters = DataObject()
        parameters.add_value_string("name", name)
        parameters.add_value_string("description", description)
        parameters.add_value_boolean("predefined", predefined)
        parameters.add_value("policies", policies)
        parameters.add_value_string("policyCombiningAlgorithm", policy_combining_alg)

        endpoint ='{}/{}'.format(POLICY_SETS, set_id)
        response = self.client.post_json(endpoint, parameters.data)
        response.success = response.status_code == 204

        return response


    def get_policy_set(self, set_id):
        '''
        Get a configured AAC Access Policies Set.

        Args:
            set_id (:obj:`str`, optional): Verify Identity Access assigned id for the policy set.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the policy set is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = '{}/{}'.format(POLICY_SETS, set_id)
        response = self.client.get_json(POLICY_SETS)
        response.success = response.status_code == 200

        return response


    def list_policy_sets(self, sort_by=None, filter=None):
        '''
        List all of the configured AAC Access Policies Sets.

        Args:
            sort_by (:obj:`str`, optional): Optional sorting of returned policies
            filter (:obj:`str`, optional): Optional filter for returned policies

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the policy sets are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(POLICY_SETS, parameters.data)
        response.success = response.status_code == 200

        return response


    def delete_policy_set(self, set_id):
        '''
        Delete a configured AAC Access Policies Set.

        Args:
            set_id (:obj:`str`): Verify Identity Access assigned id for the policy set.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = '{}/{}'.format(POLICY_SETS, set_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def authenticate_security_access_manager(self, username=None, password=None, domain=None):
        '''
        Authenticate to the Verify Identity Access policy server. This is required before an administrator can modify 
        mapping from policies to resources.

        Args:
            username (:obj:`str`): Username used to authenticate to the policy server.
            password (:obj:`str`): Password used to authenticate to the policy server.
            domain (:obj:`str`): Security domain to authenticate to.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("username", username)
        data.add_value_string("password", password)
        data.add_value_string("domain", domain)
        data.add_value_string("command", "setCredential")

        response = self.client.post_json(POLICY_ATTACHMENTS_PDADMIN, data.data)
        response.success = response.status_code == 200

        return response

    def configure_resource(
            self, server=None, resource_uri=None,
            policy_combining_algorithm=None, policies=None):
        '''
        Create a new resource in the policy server which can be attached to an authentication policy.

        Args:
            server (:obj:`str`): Name of WebSEAL instance in the policy server where resource will be created.
            resource_uri (:obj:`str`): URI of resource to be created.
            policy_combining_algorithm (:obj:`str`): Algorithm to use: "denyOverrides" or "permitOverrides".
            policies (:obj:`list` of :obj:`str`): List of policies, policy sets or API protection clients.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created policy can be accessed from the
            response.id_from_location attribute.

        '''
        data = DataObject()
        data.add_value_string("server", server)
        data.add_value_string("resourceUri", resource_uri)
        data.add_value_string("policyCombiningAlgorithm", policy_combining_algorithm)
        data.add_value("policies", policies)

        response = self.client.post_json(POLICY_ATTACHMENTS, data.data)
        response.success = response.status_code == 201

        return response


    def remove_resource(self, id):
        '''
        Delete a resource from the policy server.

        Args:
            id (:obj:`str`): The id of the resource to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "%s/%s" % (POLICY_ATTACHMENTS, id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def list_resources(self, sort_by=None, filter=None):
        '''
        Return the list of configured resources.

        Args:
            sort_by (:obj:`str`, optional): Optionally specify the attribute to sort the returned list by.
            filter (:obj:`str`): Optionally specify whether the returned list shouldb e filtered based on an attribute.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(POLICY_ATTACHMENTS, parameters.data)
        response.success = response.status_code == 200

        return response


    def publish_policy_attachment(self, id):
        '''
        Publish the changes to the policy server. This will require a restart of the corresponding WebSEAL instance.

        Args:
            id (:obj:`str`): The id of the resource to publish.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "%s/deployment/%s" % (POLICY_ATTACHMENTS, id)

        response = self.client.put_json(endpoint)
        response.success = response.status_code == 204

        return response


    def publish_multiple_policy_attachments(self, ids=[]):
        '''
        Publish the changes to the policy server for one or more resources. This will require a restart of the
        corresponding WebSEAL instance.

        Args:
            ids (:obj:`list` of :obj:`str`): List of resource ids to publish.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        id_string = ""
        for id in ids:

            if len(id_string) > 0:
                id_string += ", "
            id_string += str(id)

        data = DataObject()
        data.add_value_string("policyAttachmentIds", id_string)

        endpoint = "%s/deployment" % POLICY_ATTACHMENTS

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def list_obligations(self, sort_by=None, filter=None):
        '''
        Return the list of configured obligations for AAC.

        Args:
            sort_by (:obj:`str`, optional): Optional sorting of returned policies.
            filter (:obj:`str`, optional): Optional filter for returned policies.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the obligations are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(OBLIGATIONS, parameters.data)
        response.success = response.status_code == 200

        return response


    def create_obligation(self, name=None, description=None, obligation_uri=None,
                        type="Obligation", type_id="1", parameters=None, properties=None):
        '''
        Create a new obligation for use with RBA.

        Args:
            name (:obj:`str`): Name of obligation.
            description (:obj:`str`, optional): Description of the obligation.
            obligation_uri (:obj:`str`): URI of the obligation.
            type (:obj:`str`): The obligation type, "Obligation".
            type_id (:obj:`str`, optional): The obligation type id. If not provided, the value will be set to "1", which is the "Enforcement Point" type.
            parameters (:obj:`list` of :obj:`str`, optional): List of parameters used by the obligation when making a decision.
            properties (:obj:`list` of :obj:`str`, optional): Properties used by the obligation.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created obligation can be accessed from the 
            response.id_from_location attribute.

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("obligationURI", obligation_uri)
        data.add_value_string("type", type)
        data.add_value("parameters", parameters)
        data.add_value_string("typeId", type_id)
        data.add_value("properties", properties)

        response = self.client.post_json(OBLIGATIONS, data.data)
        response.success = response.status_code == 201

        return response


    def update_obligation(self, id, name=None, description=None, obligation_uri=None,
                        type="Obligation", type_id=None, parameters=None, properties=None):
        '''
        Update an existing obligation for use with RBA

        Args:
            id (:obj:`str`): The generated unique id of the obligation to update.
            name (:obj:`str`): Name of obligation.
            description (:obj:`str`, optional): Description of the obligation.
            obligationURI (:obj:`str`): URI of the obligation.
            type (:obj:`str`, optional): The obligation type, "Obligation".
            parameters (:obj:`list` of :obj:`str`, optional): List of parameters used by the obligation when making a decision.
            properties (:obj:`list` of :obj:`str`, optional): Properties used by the obligation.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created obligation can be accessed from the 
            response.id_from_location attribute.

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("obligationURI", obligation_uri)
        data.add_value_string("type", type)
        data.add_value("parameters", parameters)
        data.add_value_string("typeId", type_id)
        data.add_value("properties", properties)

        response = self.client.post_json(OBLIGATIONS, data.data)
        response.success = response.status_code == 201

        return response


    def delete_obligation(self, id):
        '''
        Delete an existing obligation from the policy server

        Args:
            id (:obj:`str`): The id of the obligation to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "%s/%s" % (OBLIGATIONS, id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


class AccessControl9030(AccessControl):

    def __init__(self, base_url, username, password):
        super(AccessControl9030, self).__init__(base_url, username, password)


    def configure_resource(self, server=None, resource_uri=None, policy_combining_algorithm=None, 
                        policies=None, type="reverse_proxy"):
        '''
        Create a new resource in the policy server which can be attached to an authentication policy.

        Args:
            server (:obj:`str`): Name of WebSEAL instance in the policy server where resource will be created.
            resource_uri (:obj:`str`): URI of resource to be created.
            policy_combining_algorithm (:obj:`str`): Algorithm to use: "denyOverrides" or "permitOverrides".
            policies (:obj:`list` of :obj:`str`): List of policies, policy sets or API protection clients.
            type (:obj:`str`, optional): Resource type to be created. Default is "reverse_proxy".

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("server", server)
        data.add_value_string("resourceUri", resource_uri)
        data.add_value_string(
            "policyCombiningAlgorithm", policy_combining_algorithm)
        data.add_value("policies", policies)
        data.add_value_string("type", type)

        response = self.client.post_json(POLICY_ATTACHMENTS, data.data)
        response.success = response.status_code == 201

        return response


class AccessControl10000(AccessControl9030):

    def __init__(self, base_url, username, password):
        super(AccessControl10000, self).__init__(base_url, username, password)


    def configure_resource(self, server=None, resource_uri=None, policy_combining_algorithm=None, 
                        policies=None, type="reverse_proxy", cache=None):
        '''
        Create a new resource in the policy server which can be attached to an authentication policy.

        Args:
            server (:obj:`str`): Name of WebSEAL instance in the policy server where resource will be created.
            resource_uri (:obj:`str`): URI of resource to be created.
            policy_combining_algorithm (:obj:`str`): Algorithm to use: "denyOverrides" or "permitOverrides".
            policies (:obj:`list` of :obj:`str`): List of policies, policy sets or API protection clients.
            type (:obj:`str`, optional): Resource type to be created. Default is "reverse_proxy".
            cache (`int`, optional): 0 to disable the cache for this resource, -1 to cache the decision for 
                                    the lifetime of the session or any number greater than 1 to set a 
                                    specific timeout (in seconds) for the cached decision. If not specified 
                                    a default of 0 will be used. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("server", server)
        data.add_value_string("resourceUri", resource_uri)
        data.add_value_string(
            "policyCombiningAlgorithm", policy_combining_algorithm)
        data.add_value("policies", policies)
        data.add_value_string("type", type)
        data.add_value("cache", cache)

        response = self.client.post_json(POLICY_ATTACHMENTS, data.data)
        response.success = response.status_code == 201

        return response
