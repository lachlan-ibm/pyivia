""""
@copyright: IBM
"""

import logging
import urllib

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

RATELIMIT = "/wga/ratelimiting"

class RateLimit(object):

    def __init__(self, base_url, username, password):
        super(RateLimit, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, content=None):
        '''
        Update an existing JavaScript mapping rule with new contents

        Args:
            name (:obj:`str`): Name of the rate limiting policy to be created.
            content (:obj:`str`): The rate limiting policy to be created.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("content", content)

        response = self.client.post_json(RATELIMIT, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, rlimit_id=None, content=None):
        """
        Update an existing rate limiting policy with new contents

        Args:
            rlimit_id (:obj:`str`): The id of the rule to be updated.
            content (:obj:`str`): The new rate limiting policy contents.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        data = DataObject()
        data.add_value("content", content)
        endpoint = RATELIMIT + "/{}".format(rlimit_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self, rlimit_id=None):
        '''
        Delete the specified rate limiting policy if it exists.

        Args:
            rlimit_id (:obj:`str`): The id of the policy to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = RATELIMIT + "/{}".format(rlimit_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, rlimit_id):
        """
        Get a rate limiting policy.

        Args:
            rlimit_id (:obj:`str`): The unique id of the policy to return.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the rate limiting policy is returned as JSON and can be accessed from
            the response.json attribute

        """
        endpoint = RATELIMIT + "/{}".format(rlimit_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        """
        List the rate limiting policies.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the rate limiting policies are returned as JSON and can be accessed from
            the response.json attribute

        """
        response = self.client.get_json(RATELIMIT)
        response.success = response.status_code == 200

        return response
