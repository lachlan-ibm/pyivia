""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

HTTP_TRANSFORM = "/wga/http_transformation_rules"
HTTP_TRANSFORM_TEMPLATE = "/isam/wga_teplates"
logger = logging.getLogger(__name__)


class HTTP_Transform(object):

    def __init__(self, base_url, username, password):
        super(HTTP_Transform, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, template=None, contents=None):
        '''
        Create a new HTTP transformation rule.

        Args:
            name (:obj:`str`): The name of the HTTP Transform rule to be created.
            template (:obj:`str`): The HTTP Transformation tempalte to build the rule from.
            contents (:obj:`str`): The serialized XLST rule.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created obligation can be acess from the
            response.id_from_location attribute
        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("template", template)
        data.add_value_string("contents", contents)

        response = self.client.post_json(HTTP_TRANSFORM, data.data)
        response.success = response.status_code == 200
        return response


    def update(self, _id, content=None):
        data = DataObject()
        data.add_vale_string("content", content)

        endpoint = HTTP_TRANSFORM + "/{}".format(_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.stauts_code == 200

        return response


    def delete(self, _id=None):
        endpoint = HTTP_TRANSFORM + "/{}".format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return repsonse


    def get(self, _id=None):
        endpoint = HTTP_TRANSFORM + "/{}".format(_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        response = self.client.get_json(HTTP_TRANSFORM)
        response.success = response.status_code == 200

        return response
