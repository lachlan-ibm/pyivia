""""
@copyright: IBM
"""

import logging
import urllib

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

HTTP_TRANSFORM = "/wga/http_transformation_rules"
HTTP_TRANSFORM_TEMPLATE = "/isam/wga_templates"
logger = logging.getLogger(__name__)


class HTTPTransform(object):

    def __init__(self, base_url, username, password):
        super(HTTPTransform, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, template=None, contents=None):
        '''
        Create a new HTTP transformation rule.

        Args:
            name (:obj:`str`): The name of the HTTP Transform rule to be created.
            template (:obj:`str`): The HTTP Transformation template to build the rule from.
            contents (:obj:`str`): The serialized XLST rule.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created obligation can be accessed from the
            response.id_from_location attribute.
        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("template", template)
        data.add_value_string("content", contents)

        response = self.client.post_json(HTTP_TRANSFORM, data.data)
        response.success = response.status_code == 200
        return response


    def update(self, rule_id, content=None):
        '''
        Update a new HTTP transformation rule.

        Args:
            rule_id (:obj:`str`): The id of the HTTP Transform rule to be updated.
            contents (:obj:`str`): The serialized XLST rule.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created obligation can be accessed from the
            response.id_from_location attribute.
        '''
        data = DataObject()
        data.add_value_string("content", content)

        endpoint = HTTP_TRANSFORM + "/{}".format(rule_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete(self, rule_id=None):
        '''
        Delete a new HTTP transformation rule.

        Args:
            rule_id (:obj:`str`): The id of the HTTP Transform rule to be removed.
            contents (:obj:`str`): The serialized XLST rule.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.
        '''
        endpoint = HTTP_TRANSFORM + "/{}".format(rule_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get(self, rule_id=None):
        '''
        Get a HTTP transformation rule based on a rule id.

        Args:
            rule_id (:obj:`str`): The id of the HTTP transformation rule to return.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the HTTP transformation rule is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = HTTP_TRANSFORM + "/{}".format(rule_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        Get a list of the HTTP transformation rules currently configured.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the HTTP transformation rules are returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = self.client.get_json(HTTP_TRANSFORM)
        response.success = response.status_code == 200

        return response
