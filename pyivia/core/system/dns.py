"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


NET_DNS = "/net/dns"

logger = logging.getLogger(__name__)


class DNS(object):

    def __init__(self, base_url, username, password):
        super(DNS, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get(self):
        """
        Get the current DNS configuration.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the DNS configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(NET_DNS)
        response.success = response.status_code == 200

        return response

    def update(self, auto=True, auto_from_interface=None, primary_server=None, secondary_server=None, 
            tertiary_server=None, search_domains=None):
        """
        Update the DNS configuration.

        Args:
            auto (`bool`): true if DNS should be auto configured via dhcp.
            auto_from_interface (:obj:`str`): Uuid of interface whose dhcp will defined the dns settings.
            primary_server (:obj:`str`): Primary DNS Server address.
            secondary_server (:obj:`str`): Secondary DNS Server address.
            tertiary_server (:obj:`str`): Tertiary DNS Server address.
            search_domains (:obj:`str`): Comma-separated list of DNS search domains.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        data.add_value("auto", auto)
        data.add_value_string("autoFromInterface", auto_from_interface)
        data.add_value_string("primaryServer", primary_server)
        data.add_value_string("secondaryServer", secondary_server)
        data.add_value_string("tertiaryServer", tertiary_server)
        data.add_value_string("searchDomains", search_domains)

        response = self.client.put_json(NET_DNS, data.data)
        response.success = response.status_code == 200

        return response
