""""
@copyright: IBM
"""

import logging
import urllib

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.getLogger(__name__)

CLIENT_CERT_CDAS = "/wga/client_cert_cdas"

class ClientCertMapping(object):

    def __init__(self, base_url, username, password):
        super(ClientCertMapping, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, name=None, content=None):
        '''
        Create a new client certificate mapping

        Args:
            name (:obj:`str`): The name of the client certificate mapping rule
            content (:obj:`str`): XLST rule to be applied for certificate to user mapping

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("content", content)

        response = self.client.post_json(CLIENT_CERT_CDAS, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, _id=None, content=None):
        '''
        Update a client certificate mapping

        Args:
            _id (:obj:`str`): The id of hte certificate mapping rule to update
            content (:obj:`str`): The new XLST rule to be uploaded

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value("content", content)
        data.add_value_string("id", _id)
        endpoint = CLIENT_CERT_CDAS + "/{}".format(_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete(self, _id=None):
        '''
        Delete an existing certificate mapping rule

        Args:
            _id (:obj:`str`): The id of the certificate mapping rule to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = CLIENT_CERT_CDAS + "/{}".format(_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, _id):
        '''
        Get a configured user certificate mapping.

        Args:
            _id (:obj:`str`): The id of the user certificate mapping to return

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the XLST rule is returned as JSON and can be accessed from
            the response.json attribute


        '''
        endpoint = CLIENT_CERT_CDAS + "/{}".format(_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_template(self, tempalte_id=None):
        '''
        Get a template user certificate mapping rule

        Args:
            template_id (:obj:`str`): The id of the template rule to return

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the XLST rule is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoit = "/isam/wga_templates/client_cert_cdas_template"
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        Return a list of all of the configured user certificate mapping rules.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the XLST rules are returned as JSON and can be accessed from
            the response.json attribute

        '''

        '''
        response = self.client.get_json(CLIENT_CERT_CDAS)
        response.success = response.status_code == 200

        return response
