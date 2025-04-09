"""
@copyright: IBM
"""

import logging
import json

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


MAPPING_RULES = "/iam/access/v8/mapping-rules"

logger = logging.getLogger(__name__)


class MappingRules(object):

    def __init__(self, base_url, username, password):
        super(MappingRules, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_rule(self, file_name=None, rule_name=None, category=None, content=None):
        response = Response()
        try:
            data = DataObject()
            data.add_value_string("fileName", ("%s_%s.js" % (category, rule_name)))
            data.add_value_string("category", category)
            data.add_value_string("name", rule_name)
            if content == None:
                with open(file_name, 'rb') as content:
                    data.add_value_string("content", content.read().decode('utf-8'))
            else:
                data.add_value_string("content", content)
            endpoint = MAPPING_RULES

            response = self.client.post_json(endpoint, data.data)
            response.success = response.status_code == 201

        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def update_rule(self, rule_id, file_name=None):
        response = Response()
        try:
            with open(file_name, 'rb') as content:
                data = DataObject()

                data.add_value_string("content", content.read().decode('utf-8'))

                endpoint = ("%s/%s" % (MAPPING_RULES, rule_id))

                json.dumps(data.data, sort_keys=True, indent=4, separators=(',', ': '))

                response = self.client.put_json(endpoint, data.data)
                response.success = response.status_code == 204

        except IOError as e:
            logger.error(e)
            response.success = False

        return response


    def get_rule(self, rule_id=None, filter=None):

        endpoint = ("%s/%s?filter=%s" % (MAPPING_RULES, rule_id if rule_id != None else "", filter))

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_rules(self):
        '''
        Return JSON list of all mapping rules
        '''
        response = self.client.get_json(MAPPING_RULES)
        response.success = response.status_code == 200

        return response


    def delete_rule(self, rule_id=None):
        endpoint = MAPPING_RULES + "/{}".format(rule_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
