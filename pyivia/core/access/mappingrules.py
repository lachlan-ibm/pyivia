"""
@copyright: IBM
"""

import logging
import json

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


MAPPING_RULES = "/iam/access/v8/mapping-rules"

logger = logging.getLogger(__name__)


class MappingRules(object):

    def __init__(self, base_url, username, password):
        super(MappingRules, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_rule(self, rule_name=None, category=None, content=None):
        '''
        Create a JavaScript mapping rule.

        Args:
            rule_name (:obj:`str`): The name of the new mapping rule.
            category (:obj:`str`): Type of mapping rule to create.
            contents (:obj:`str`): The JavaScript content of the new mapping rule.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created mapping rule can be accessed from the
            response.id_from_location attribute.

        '''
        data = DataObject()
        data.add_value_string("fileName", ("%s_%s.js" % (category, rule_name)))
        data.add_value_string("category", category)
        data.add_value_string("name", rule_name)
        data.add_value_string("content", content)
        endpoint = MAPPING_RULES

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response


    def import_rule(self, rule_name=None, category=None, file_name=None):
        '''
        Create a JavaScript mapping rule from a file.

        Args:
            rule_name (:obj:`str`): The name of the rule to be created.
            category (:obj:`str`): Type of mapping rule to create.
            file_name (:obj:`str`): The absolute path to the JavaScript mapping rule.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created obligation can be accessed from the
            response.id_from_location attribute.

        '''
        response = Response()
        try:
            data = DataObject()
            data.add_value_string("fileName", ("%s_%s.js" % (category, rule_name)))
            data.add_value_string("category", category)
            data.add_value_string("name", rule_name)
            with open(file_name, 'rb') as content:
                data.add_value_string("content", content.read().decode('utf-8'))
            endpoint = MAPPING_RULES

            response = self.client.post_json(endpoint, data.data)
            response.success = response.status_code == 201

        except IOError as e:
            logger.error(e)
            response.success = False

        return response


    def update_rule(self, rule_id, file_name=None, content=None):
        '''
        Update an existing JavaScript mapping rule with new contents

        Args:
            rule_id (:obj:`str`): The id of the rule to be updated.
            file_name (:obj:`str`, optional): Absolute path to file containing new mapping rule. Must specify either
                                            file_name or content.
            content (:obj:`str`, optional): The javascript code to replace current mapping rule. Must specify either
                                            file_name or content.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        response = Response()
        try:
            data = DataObject()
            if content == None:
                with open(file_name, 'rb') as content:

                    data.add_value_string("content", content.read().decode('utf-8'))
            else:
                data.add_value_string("content", content)

            endpoint = ("%s/%s" % (MAPPING_RULES, rule_id))

            response = self.client.put_json(endpoint, data.data)
            response.success = response.status_code == 204

        except IOError as e:
            logger.error(e)
            response.success = False

        return response


    def get_rule(self, rule_id=None,):
        '''
        Get a mapping rule based on a rule id.

        Args:
            rule_id (:obj:`str`, optional): The id of the mapping rule to return.


        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the mapping rule is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = "{}/{}".format(MAPPING_RULES, rule_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_rules(self, filter=None):
        '''
        Return a list of all mapping rules.

        Args:
            filter (:obj:`str`, optional): Filter to apply to returned rules. eg. "name startswith Test".

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the mapping rules are returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = ("%s%s" % (MAPPING_RULES, "?filter=" + filter if isinstance(filter, str) else ""))
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def delete_rule(self, rule_id=None):
        '''
        Delete the specified mapping rule if it exists.

        Args:
            rule_id (:obj:`str`): The id of the mapping rule to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "{}/{}".format(MAPPING_RULES, rule_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
