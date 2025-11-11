"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


AUTHENTICATION_MECHANISMS = "/iam/access/v8/authentication/mechanisms"
AUTHENTICATION_MECHANISM_TYPES = "/iam/access/v8/authentication/mechanism/types"
AUTHENTICATION_POLICIES = "/iam/access/v8/authentication/policies"

logger = logging.getLogger(__name__)


class Authentication(object):

    def __init__(self, base_url, username, password):
        super(Authentication, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_mechanism(self, description=None, name=None, uri=None, type_id=None,
            properties=[], attributes=[]):
        '''
        Create an authentication mechanism.

        Args:
            description: (:obj:`str`): Description of the mechanism.
            name (:obj:`str`): Name of the mechanism.
            uri (:obj:`str`): URI of the mechanism.
            type_id (:obj:`str`): Mechanism type to inherit from
            properties (:obj:`list` of :obj:`dict`): List of properties for the mechanism. Properties are determined by 
                                                    the mechanism type. Properties should follow the 
                                                    format::

                                                            [
                                                                {"key":"property.key.name", 
                                                                 "value":"property.value"
                                                                }
                                                            ]

            attributes: (:obj:`list` of :obj:`dict`): List of attributes to retrieve from the request context before 
                                                    executing the mechanism. Attributes should follow the 
                                                    format::

                                                            [
                                                                {"selector":"Context.REQUEST", 
                                                                 "namespace": "urn:ibm:security:asf:request:parameter", 
                                                                 "name": "parameter"
                                                                }
                                                            ]

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created mechanism can be accessed from the 
            response.id_from_location attribute.

        '''
        data = DataObject()
        data.add_value_string("description", description)
        data.add_value_string("name", name)
        data.add_value_string("uri", uri)
        data.add_value_string("typeId", type_id)
        data.add_value_not_empty("properties", properties)
        data.add_value_not_empty("attributes", attributes)

        response = self.client.post_json(AUTHENTICATION_MECHANISMS, data.data)
        response.success = response.status_code == 201

        return response


    def list_mechanism_types(self, sort_by=None, count=None, start=None, filter=None):
        '''
        Get the list of available mechanism types

        Args:
            sort_by (:obj:`str`, optional): Attribute to sort results by.
            count (:obj:`str`, optional): Maximum number of results to fetch.
            start (:obj:`str`, optional): Pagination offset of returned results.
            filter (:obj:`str`): Attribute to filter results by.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the authentication mechanism types are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("count", count)
        parameters.add_value_string("start", start)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(
            AUTHENTICATION_MECHANISM_TYPES, parameters.data)
        response.success = response.status_code == 200

        return response


    def list_mechanisms(self, sort_by=None, count=None, start=None, filter=None):
        '''
        Get the list of available mechanisms

        Args:
            sort_by (:obj:`str`, optional): Attribute to sort results by.
            count (:obj:`str`, optional): Maximum number of results to fetch.
            start (:obj:`str`, optional): Pagination offset of returned results.
            filter (:obj:`str`): Attribute to filter results by.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the authentication mechanism are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("count", count)
        parameters.add_value_string("start", start)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(
            AUTHENTICATION_MECHANISMS, parameters.data)
        response.success = response.status_code == 200

        return response


    def update_mechanism(self, id, description=None, name=None, uri=None, type_id=None,
            predefined=True, properties=None, attributes=None):
        '''
        Update an authentication mechanism.

        Args:
            description: (:obj:`str`): Description of the mechanism.
            name (:obj:`str`): Name of the mechanism.
            uri (:obj:`str`): URI of the mechanism.
            type_id (:obj:`str`): Mechanism type to inherit from.
            predefined (bool, optional): If this mechanism is pre-defined by Verify Identity Access. Default value is ``true``.
            properties (:obj:`list` of :obj:`dict`): List of properties for the mechanism. Properties are determined by 
                                                    the mechanism type. Properties should use the 
                                                    format::

                                                            [
                                                                {"key":"property.key.name", 
                                                                 "value":"property.value"
                                                                }
                                                            ]

            attributes: (:obj:`list` of :obj:`dict`): List of attributes to retrieve from the request context before 
                                                    executing the mechanism. Attributes should use the 
                                                    format::

                                                            [
                                                                {"selector":"Context.REQUEST", 
                                                                 "namespace": "urn:ibm:security:asf:request:parameter", 
                                                                 "name": "parameter"
                                                                }
                                                            ]

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created mechanism can be accessed from the 
            response.id_from_location attribute

        '''
        data = DataObject()
        data.add_value_string("id", id)
        data.add_value_string("description", description)
        data.add_value_string("name", name)
        data.add_value_string("uri", uri)
        data.add_value_string("typeId", type_id)
        data.add_value_boolean("predefined", predefined)
        data.add_value_not_empty("properties", properties)
        data.add_value_not_empty("attributes", attributes)

        endpoint = "%s/%s" % (AUTHENTICATION_MECHANISMS, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete_mechanism(self, mechanism_id):
        '''
        Delete an existing authentication mechanism. Only  administrator created (not pre-defined) mechanisms can be deleted.

        Args:
            mechanism_id (:obj:`str`): The identifier for the mechanism to be removed.
        
        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "{}/{}".format(AUTHENTICATION_MECHANISMS, id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def create_policy(self, name=None, policy=None, uri=None, description=None,
            dialect="urn:ibm:security:authentication:policy:1.0:schema", enabled=True):
        '''
        Create an authentication policy.

        Args:
            name (:obj:`str`): Name of the policy to be created.
            policy (:obj:`str`): XML config of the policy.
            uri (:obj:`str`): URI used to identify the policy.
            description (:obj:`str`, optional): Description of the policy.
            dialect (:obj:`str`, optional): Schema used to create policy. use the default "urn:ibm:security:authentication:policy:1.0:schema".
            enabled (bool): Flag to enable the policy for use by the AAC runtime.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created mechanism can be accessed from the 
            response.id_from_location attribute.

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("policy", policy)
        data.add_value_string("uri", uri)
        data.add_value_string("description", description)
        data.add_value_string("dialect", dialect)
        data.add_value_boolean("enabled", enabled)

        response = self.client.post_json(AUTHENTICATION_POLICIES, data.data)
        response.success = response.status_code == 201

        return response


    def get_policy(self, id):
        '''
        Retrieve a policy configuration.

        Args:
            id (:obj:`str`): the id of the policy to be deleted.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the obligations are returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = "%s/%s" % (AUTHENTICATION_POLICIES, id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_policies(self, sort_by=None, count=None, start=None, filter=None):
        '''
        Get a list of all of hte configured AAC policies.

        Args:
            sort_by (:obj:`str`, optional): Attribute to sort results by.
            count (:obj:`str`, optional): Maximum number of results to fetch.
            start (:obj:`str`, optional): Pagination offset of returned results.
            filter (:obj:`str`): Attribute to filter results by

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the authentication policies are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("count", count)
        parameters.add_value_string("start", start)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(
            AUTHENTICATION_POLICIES, parameters.data)
        response.success = response.status_code == 200

        return response


    def update_policy(self, id, name=None, policy=None, uri=None, description=None,
            dialect="urn:ibm:security:authentication:policy:1.0:schema",
            user_last_modified=None, last_modified=None,
            date_created=None, predefined=None, enabled=True):
        '''
        Update an AAC authentication policy

        Args:
            id (:obj:`str`): The id of the policy to be updated.
            name (:obj:`str`): Name of the policy.
            policy (:obj:`str`): XML config of the policy.
            uri (:obj:`str`): URI used to identify the policy.
            description (:obj:`str`, optional): Description of the policy.
            dialect (:obj:`str`, optional): Schema used to create policy. use the default 
                                            ``urn:ibm:security:authentication:policy:1.0:schema``
            user_las_modified (:obj:`str`): User id of the user who last made modifications to the authentication policy.
            last_modified (:obj:`str`): Timestamp of when this policy was last modified.
            date_created (:obj:`str`): Timestamp of when this policy was created.
            predefined (bool): Flag to indicate if this is a default policy available out of the box.
            enabled (bool): Flag to enable the policy for use by the AAC runtime.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("policy", policy)
        data.add_value_string("uri", uri)
        data.add_value_string("description", description)
        data.add_value_string("dialect", dialect)
        data.add_value_string("id", id)
        data.add_value_boolean("enabled", enabled)
        data.add_value_string("userlastmodified", user_last_modified)
        data.add_value_string("lastmodified", last_modified)
        data.add_value_string("datecreated", date_created)
        data.add_value_boolean("predefined", predefined)

        endpoint = "%s/%s" % (AUTHENTICATION_POLICIES, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


class Authentication9021(Authentication):

    def __init__(self, base_url, username, password):
        super(Authentication9021, self).__init__(base_url, username, password)

    def create_policy(self, name=None, policy=None, uri=None, description=None,
            dialect="urn:ibm:security:authentication:policy:1.0:schema",
            enabled=True, id=None, user_last_modified=None, last_modified=None,
            date_created=None):
        '''
        Create an authentication policy.

        Args:
            name (:obj:`str`): Name of the policy to be created
            policy (:obj:`str`): XML config of the policy.
            uri (:obj:`str`): URI used to identify the policy.
            description (:obj:`str`, optional): Description of the policy.
            dialect (:obj:`str`, optional): Schema used to create policy. use the default "urn:ibm:security:authentication:policy:1.0:schema"
            enabled (bool, optional): Flag to enable the policy for use by the AAC runtime. Default is ``true``.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created mechanism can be accessed from the 
            response.id_from_location attribute

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("policy", policy)
        data.add_value_string("uri", uri)
        data.add_value_string("description", description)
        data.add_value_string("dialect", dialect)
        data.add_value_string("id", id)
        data.add_value_string("userlastmodified", user_last_modified)
        data.add_value_string("lastmodified", last_modified)
        data.add_value_string("datecreated", date_created)
        data.add_value_boolean("enabled", enabled)

        response = self.client.post_json(AUTHENTICATION_POLICIES, data.data)
        response.success = response.status_code == 201

        return response


    def update_policy(self, id, name=None, policy=None, uri=None, description=None,
            dialect="urn:ibm:security:authentication:policy:1.0:schema",
            user_last_modified=None, last_modified=None,
            date_created=None, predefined=None, enabled=True):
        '''
        Update an AAC authentication policy

        Args:
            id (:obj:`str`): The id of the policy to be updated.
            name (:obj:`str`): Name of the policy.
            policy (:obj:`str`): XML config of the policy.
            uri (:obj:`str`): URI used to identify the policy.
            description (:obj:`str`, optional): Description of the policy.
            dialect (:obj:`str`, optional): Schema used to create policy. use the default "urn:ibm:security:authentication:policy:1.0:schema"
            user_las_modified (:obj:`str`): User id of the user who last made modifications to the authentication policy.
            last_modified (:ob:`str`): Timestamp of when this policy was last modified.
            date_created (:obj:`str`): Timestamp of when this policy was created.
            predefined (bool): Flag to indicate if this is a default policy available out of the box.
            enabled (bool, optional): Flag to enable the policy for use by the AAC runtime. Default is ``true``.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("policy", policy)
        data.add_value_string("uri", uri)
        data.add_value_string("description", description)
        data.add_value_string("dialect", dialect)
        data.add_value_string("id", id)
        data.add_value_string("userlastmodified", user_last_modified)
        data.add_value_string("lastmodified", last_modified)
        data.add_value_string("datecreated", date_created)
        data.add_value_boolean("predefined", predefined)
        data.add_value_boolean("enabled", enabled)

        endpoint = "%s/%s" % (AUTHENTICATION_POLICIES, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def disable_all_policies(self):
        '''
        Disable all authentication policies.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_boolean("enabled", False)
        response = self.client.put_json(AUTHENTICATION_POLICIES, data.data)
        response.success = response.status_code == 204
        return response


    def enable_all_policies(self):
        '''
        Enable all authentication policies.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        data = DataObject()
        data.add_value_boolean("enabled", True)
        response = self.client.put_json(AUTHENTICATION_POLICIES, data.data)
        response.success = response.status_code == 204
        return response


    def delete_policy(self, _id):
        '''
        Remove an authentication policy.

        Args:
            _id (:obj:`str`): The id of the policy to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = "%s/%s" % (AUTHENTICATION_POLICIES, _id)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
