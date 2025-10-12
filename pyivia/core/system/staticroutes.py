"""
@copyright: IBM
"""

from typing import Never


import logging
import uuid

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


ROUTES = "/net/routes"

logger = logging.getLogger(__name__)


class StaticRoutes(object):

    def __init__(self, base_url, username, password):
        super(StaticRoutes, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_route(self, address=None, mask_or_prefix=None, enabled=True, gateway=None, interface_uuid=None,
            metric=0, comment=None, table=None):
        """
        Create a new networking route.

        Args:
            address (:obj:`str`): route address (ipv4 or ipv6) or keyword "default"
            mask_or_prefix (:obj:`str`): optional mask or prefix of the address.
            enabled (`bool`): true if the route should be used, otherwise false.
            gateway (:obj:`str`): optional route gateway
            interface_uuid (:obj:`str`): interface for the route. If not defined, the operating system will determine 
                            the correct interface.
            metric (`int`): optional route metric
            comment (:obj:`str`, optional): comment to identify the static route.
            table (:obj:`str`, optional): "main" or uuid of address. If not defined "main" is assumed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created mechanism can be access from the 
            response.id_from_location attribute
        """
        data = DataObject()
        data.add_value_string("address", address)
        data.add_value_string("maskOrPrefix", mask_or_prefix)
        data.add_value("enabled", enabled)
        data.add_value("metric", metric)
        data.add_value_string("gateway", gateway)
        data.add_value_string("interfaceUUID", interface_uuid)
        data.add_value_string("metric", metric)
        data.add_value_string("comment", comment)
        data.add_value_string("table", table)

        response = self.client.post_json(ROUTES, data.data)
        response.success = response.status_code == 201

        return response

    def list_routes(self):
        """
        List the current networking routes.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the networking route configurations are returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(ROUTES)
        response.success = response.status_code == 200

        return response

    def update_route(self, uuid, enabled=None, address=None, mask_or_prefix=None, gateway=None, interface_uuid=None, 
            metric=0, comment=None, table=None) -> Response:
        """
        Update a networking route configuration.

        Args:
            uuid (:obj:`str`): unique id of the static route to update
            enabled (`bool`): true if the route should be used, otherwise false.
            address (:obj:`str`): route address (ipv4 or ipv6) or keyword "default"
            mask_or_prefix (:obj:`str`): optional mask or prefix of the address.
            gateway (:obj:`str`): optional route gateway
            interface_uuid (:obj:`str`): interface for the route. If not defined, the operating system will determine 
                                        the correct interface.
            metric (`int`): optional route metric
            comment (:obj:`str`, optional): comment to identify the static route.
            table (:obj:`str`, optional): "main" or uuid of address. If not defined "main" is assumed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the networking route configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        raise Exception("Not yet implemented")

class StaticRoutes10000(StaticRoutes):

    def update_route(self, uuid, enabled=None, address=None, mask_or_prefix=None, gateway=None, interface_uuid=None, 
            metric=0, comment=None, table=None) -> Response:
        """
        Update a networking route configuration.

        Args:
            uuid (:obj:`str`): unique id of the static route to update
            enabled (`bool`): true if the route should be used, otherwise false.
            address (:obj:`str`): route address (ipv4 or ipv6) or keyword "default"
            mask_or_prefix (:obj:`str`): optional mask or prefix of the address.
            gateway (:obj:`str`): optional route gateway
            interface_uuid (:obj:`str`): interface for the route. If not defined, the operating system will determine 
                                        the correct interface.
            metric (`int`): optional route metric
            comment (:obj:`str`, optional): comment to identify the static route.
            table (:obj:`str`, optional): "main" or uuid of address. If not defined "main" is assumed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the networking route configuration is returned as JSON and can be accessed from
            the response.json attribute
        """

        data = DataObject()
        data.add_value_string("address", address)
        data.add_value_string("maskOrPrefix", mask_or_prefix)
        data.add_value("enabled", enabled)
        data.add_value("metric", metric)
        data.add_value_string("gateway", gateway)
        data.add_value_string("interfaceUUID", interface_uuid)
        data.add_value_string("metric", metric)
        data.add_value_string("comment", comment)
        data.add_value_string("table", table)

        url = ROUTES + '/' + uuid

        response = self.client.put_json(url, data.data)
        response.success = response.status_code == 200

        return response
