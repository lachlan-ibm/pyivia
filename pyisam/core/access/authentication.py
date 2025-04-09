"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


AUTHENTICATION_MECHANISMS = "/iam/access/v8/authentication/mechanisms"
AUTHENTICATION_MECHANISM_TYPES = "/iam/access/v8/authentication/mechanism/types"
AUTHENTICATION_POLICIES = "/iam/access/v8/authentication/policies"

logger = logging.getLogger(__name__)


class Authentication(object):

    def __init__(self, base_url, username, password):
        super(Authentication, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_mechanism(
            self, description=None, name=None, uri=None, type_id=None,
            properties=[], attributes=[]):
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

    def list_mechanism_types(
            self, sort_by=None, count=None, start=None, filter=None):
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("count", count)
        parameters.add_value_string("start", start)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(
            AUTHENTICATION_MECHANISM_TYPES, parameters.data)
        response.success = response.status_code == 200

        return response

    def list_mechanisms(
            self, sort_by=None, count=None, start=None, filter=None):
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("count", count)
        parameters.add_value_string("start", start)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(
            AUTHENTICATION_MECHANISMS, parameters.data)
        response.success = response.status_code == 200

        return response

    def update_mechanism(
            self, id, description=None, name=None, uri=None, type_id=None,
            predefined=None, properties=None, attributes=None):
        data = DataObject()
        data.add_value_string("id", id)
        data.add_value_string("description", description)
        data.add_value_string("name", name)
        data.add_value_string("uri", uri)
        data.add_value_string("typeId", type_id)
        data.add_value("predefined", predefined)
        data.add_value("properties", properties)
        data.add_value("attributes", attributes)

        endpoint = "%s/%s" % (AUTHENTICATION_MECHANISMS, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response

    def create_policy(
            self, name=None, policy=None, uri=None, description=None,
            dialect="urn:ibm:security:authentication:policy:1.0:schema",
            enabled=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("policy", policy)
        data.add_value_string("uri", uri)
        data.add_value_string("description", description)
        data.add_value_string("dialect", dialect)
        data.add_value_string("enabled", enabled)

        response = self.client.post_json(AUTHENTICATION_POLICIES, data.data)
        response.success = response.status_code == 201

        return response

    def get_policy(self, id):
        endpoint = "%s/%s" % (AUTHENTICATION_POLICIES, id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def list_policies(
            self, sort_by=None, count=None, start=None, filter=None):
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("count", count)
        parameters.add_value_string("start", start)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(
            AUTHENTICATION_POLICIES, parameters.data)
        response.success = response.status_code == 200

        return response

    def update_policy(
            self, id, name=None, policy=None, uri=None, description=None,
            dialect="urn:ibm:security:authentication:policy:1.0:schema",
            user_last_modified=None, last_modified=None,
            date_created=None, predefined=None, enabled=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("policy", policy)
        data.add_value_string("uri", uri)
        data.add_value_string("description", description)
        data.add_value_string("dialect", dialect)
        data.add_value_string("id", id)
        data.add_value_string("enabled", enabled)
        data.add_value_string("userlastmodified", user_last_modified)
        data.add_value_string("lastmodified", last_modified)
        data.add_value_string("datecreated", date_created)
        data.add_value("predefined", predefined)

        endpoint = "%s/%s" % (AUTHENTICATION_POLICIES, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


class Authentication9021(Authentication):

    def __init__(self, base_url, username, password):
        super(Authentication9021, self).__init__(base_url, username, password)

    def create_policy(
            self, name=None, policy=None, uri=None, description=None,
            dialect="urn:ibm:security:authentication:policy:1.0:schema",
            id=None, user_last_modified=None, last_modified=None,
            date_created=None, enabled=True):
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
        data.add_value("enabled", enabled)

        response = self.client.post_json(AUTHENTICATION_POLICIES, data.data)
        response.success = response.status_code == 201

        return response

    def update_policy(
            self, id, name=None, policy=None, uri=None, description=None,
            dialect="urn:ibm:security:authentication:policy:1.0:schema",
            user_last_modified=None, last_modified=None,
            date_created=None, predefined=None, enabled=True):
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
        data.add_value("predefined", predefined)
        data.add_value("enabled", enabled)

        endpoint = "%s/%s" % (AUTHENTICATION_POLICIES, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def disable_all_policies(self):
        data = DataObject()
        data.add_value("enabled", False)
        response = self.client.put_json(AUTHENTICATION_POLICIES, data.data)
        response.success = response.status_code == 204
        return response


    def delete_policy(self, _id):
        endpoint = "%s/%s" % (AUTHENTICATION_POLICIES, _id)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def delete_mechanism(self, _id):
        endpoint = "%s/%s" % (AUTHENTICATION_MECHANISMS, _id)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
