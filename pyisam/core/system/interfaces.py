"""
@copyright: IBM
"""

import logging
import uuid

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


NET_INTERFACES = "/net/ifaces"

logger = logging.getLogger(__name__)


class Interfaces(object):

    def __init__(self, base_url, username, password):
        super(Interfaces, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_address(
            self, interface_label, address=None, mask_or_prefix=None,
            enabled=True, allow_management=False, override_subnet_checking=False):
        
        response = self.list_interfaces()

        if response.success:
            found = False
            for entry in response.json.get("interfaces", []):
                if entry.get("label") == interface_label:
                    found = True
                    data = entry

                    address_data = DataObject()
                    address_data.add_value_string("uuid", uuid.uuid4())
                    address_data.add_value_string("address", address)
                    address_data.add_value_string(
                        "maskOrPrefix", mask_or_prefix)
                    address_data.add_value("enabled", enabled)
                    address_data.add_value("allowManagement", allow_management)

                    data["ipv4"]["addresses"].append(address_data.data)
                    data["ipv4"]["overrideSubnetChecking"] = override_subnet_checking

                    endpoint = ("%s/%s" % (NET_INTERFACES, data.get("uuid")))

                    response = self.client.put_json(endpoint, data)
                    response.success = response.status_code == 200
            if not found:
                response.success = False

        return response

    def list_interfaces(self):
        response = self.client.get_json(NET_INTERFACES)
        response.success = response.status_code == 200

        return response

class Interfaces10000(Interfaces):

    def update_interface(self, uuid, name=None, comment=None, enabled=True, vlan_id=0, bonding_mode=None,
            bonded_to=None, ipv4_address=None, ipv4_mask_or_prefix=None, ipv4_boradcast_address=None,
            ipv4_allow_management=False, ipv4_enabled=True, ipv4_dhcp_enabled=True, 
            ipv4_dhcp_allow_management=False, ipv4_dhcp_default_route=False, ipv4_dhcp_route_metric=0,
            ipv4_override_subnet_checking=False, ipv6_address=None, ipv6_prefix_length=None, 
            ipv6_allow_management=None, ipv6_enabled=None, ipv6_dhcp_enabled=False, ipv6_dhcp_allow_management=False):
        

        data = DataObject()
        ipv4 = DataObject()
        if ipv4_address:
            ipv4_address_data = DataObject()
            ipv4_address_data.add_value_string("address", ipv4_address)
            ipv4_address_data.add_value_string(
                "maskOrPrefix", ipv4_mask_or_prefix)
            ipv4_address_data.add_value_string(
                    "broadcastAddress", ipv4_boradcast_address)
            ipv4_address_data.add_value_boolean("enabled", ipv4_enabled)
            ipv4_address_data.add_value_boolean("allowManagement", ipv4_allow_management)
            ipv4.add_value("addresses", [ipv4_address_data.data])
        
        ipv4_dhcp_data = DataObject()
        ipv4_dhcp_data.add_value_boolean("enabled", ipv4_dhcp_enabled)
        ipv4_dhcp_data.add_value_boolean("allowManagement", ipv4_dhcp_allow_management)
        ipv4_dhcp_data.add_value_boolean("providesDefaultRoute", ipv4_dhcp_default_route)
        ipv4_dhcp_data.add_value_string("routeMetric", ipv4_dhcp_route_metric)
        ipv4.add_value_not_empty("dhcp", ipv4_dhcp_data.data)
        ipv4.add_value_boolean("overrideSubnetChecking", ipv4_override_subnet_checking)
        data.add_value_not_empty("ipv4", ipv4.data)

        ipv6 = DataObject()
        if ipv6_address:
            ipv6_address_data = DataObject()
            ipv6_address_data.add_value_string("address", ipv6_address)
            ipv6_address_data.add_value_string("prefixLength", ipv6_prefix_length)
            ipv6_address_data.add_value_boolean("allowManagement", ipv6_allow_management)
            ipv6_address_data.add_value_boolean("enabled", ipv6_enabled)
            ipv6.add_value("addresses", [ipv6_address_data.data])
        
        ipv6_dhcp_data = DataObject()
        ipv6_dhcp_data.add_value_boolean("enabled", ipv6_dhcp_enabled)
        ipv6_dhcp_data.add_value_boolean("allowManagement", ipv6_dhcp_allow_management)
        ipv6.add_value("dhcp", ipv6_dhcp_data.data)
        data.add_value_not_empty("ipv6", ipv6.data)
        data.add_value_string('name', name)
        data.add_value_string('comment', comment)
        data.add_value('enabled', enabled)
        data.add_value_string('vlanId', vlan_id)
        data.add_value_string('bondingMode', bonding_mode)
        data.add_value_string('bondedTo', bonded_to)

        endpoint = ("%s/%s" % (NET_INTERFACES, uuid))
        logger.debug("interface: {}".format(data.data))
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200
        return response
