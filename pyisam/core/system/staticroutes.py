"""
@copyright: IBM
"""

import logging
import uuid

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


ROUTES = "/net/routes"

logger = logging.getLogger(__name__)


class StaticRoutes(object):

    def __init__(self, base_url, username, password):
        super(StaticRoutes, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_route(
            self, address=None, mask_or_prefix=None,
            enabled=True, gateway=None, interface_uuid=None,
            metric=0, comment=None, table=None):

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
        response = self.client.get_json(ROUTES)
        response.success = response.status_code == 200

        return response

class StaticRoutes10000(StaticRoutes):

    def update_route(self, uuid, enabled=None, address=None, mask_or_prefix=None,
            gateway=None, interface_uuid=None, metric=0, comment=None, table=None):

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
