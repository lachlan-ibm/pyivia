"""
@copyright: IBM
"""

import logging
import uuid

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient

ACCESS_POLICY = "/iam/access/v8/access-policies/"

logger = logging.getLogger(__name__)

class AccessPolicy(object):

    def __init__(self, base_url, username, password):
        super(AccessPolicy, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def list_policies(self, _filter=None):
        """
        Get the configured access policies.

        Args:
            _filter (:obj:`str`, optional

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the access policies are returned as JSON and can be accessed from
            the response.json attribute.

        """
        endpoint = ACCESS_POLICY
        if _filter != None:
            endpoint += "?filter=%s" % (_filter)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_policy(self, policy_id=None):
        """
        Get a specific access policy.

        Args:
            policy_id (:obj:`str`): The id of the policy to fetch.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the access policy is returned as JSON and can be accessed from
            the response.json attribute.

        """

        endpoint = "%s/%s" % (ACCESS_POLICY, policy_id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_policy(self, policy_name=None, category=None, policy_type="JavaScript", content=None):
        """
        Create an access policy for single sign-on federations

        Args:
            policy_name (:obj:`str`): A unique name for the access policy.
            category (:obj:`str`): A grouping of related access policies. Valid values are: "InfoMap", "AuthSVC", "OAUTH","OTP", "OIDC" and "SAML2_0".
            policy_type (:obj:`str`, optional): System default type for each access policy.
            content (:obj:`str`): Contents of the access policy rule.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the create access policy can be accessed from the
            response.id_from_location attribute.

        """
        data = DataObject()
        data.add_value_string('category',category)
        data.add_value_string('type',policy_type)
        data.add_value_string('name',policy_name)
        data.add_value_string("content", content)
        endpoint = ACCESS_POLICY
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response


    def update_policy(self, policy_id=None, content=None):
        """
        Update asn existing access policy

        Args:
            policy_id (:obj:`str`): The name of the access policy to be updated.
            content (:obj:`str`): The serialized content of the new JavaScript access policy.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        """
        data = DataObject()
        data.add_value_string("content", content)
        endpoint = "%s/%s" % (ACCESS_POLICY, policy_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204
        return response


    def delete_policy(self, policy_id=None):
        """
        Delete a specific access policy.

        Args:
            policy_id (:obj:`str`): The id of the policy to fetch.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        """

        endpoint = "%s/%s" % (ACCESS_POLICY, policy_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response