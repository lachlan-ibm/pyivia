""""
@copyright: IBM
"""

import logging
import urllib

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

CLIENT_CERT_CDAS = "/wga/client_cert_cdas"

class ClientCertMapping(object):

    def __init__(self, base_url, username, password):
        super(ClientCertMapping, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_rule(self, name=None, content=None):
        '''
        Create a new client certificate mapping

        Args:
            name (:obj:`str`): The name of the client certificate mapping rule
            content (:obj:`str`): XLST rule to be applied for certificate to user mapping

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("content", content)

        response = self.client.post_json(CLIENT_CERT_CDAS, data.data)
        response.success = response.status_code == 200

        return response


    def update_rule(self, rule_id=None, content=None):
        '''
        Update a client certificate mapping

        Args:
            rule_id (:obj:`str`): The id of the certificate mapping rule to update
            content (:obj:`str`): The new XLST rule to be uploaded

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("content", content)
        endpoint = CLIENT_CERT_CDAS + "/{}".format(rule_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def delete_rule(self, rule_id=None):
        '''
        Delete an existing certificate mapping rule

        Args:
            rule_id (:obj:`str`): The id of the certificate mapping rule to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = CLIENT_CERT_CDAS + "/{}".format(rule_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get_rule(self, rule_id):
        '''
        Get a configured user certificate mapping.

        Args:
            rule_id (:obj:`str`): The id of the user certificate mapping to return

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the XLST rule is returned as JSON and can be accessed from
            the response.json attribute


        '''
        endpoint = CLIENT_CERT_CDAS + "/{}".format(rule_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_template(self):
        '''
        Get the Client Cert CDAS template mapping rule

        Args:
            template_id (:obj:`str`): The id of the template rule to return

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the XLST rule is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = "/isam/wga_templates/client_cert_cdas_template"
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_rules(self):
        '''
        Return a list of all of the configured user certificate mapping rules.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the XLST rules are returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = self.client.get_json(CLIENT_CERT_CDAS)
        response.success = response.status_code == 200

        return response
