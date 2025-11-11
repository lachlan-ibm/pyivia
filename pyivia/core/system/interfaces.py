"""
@copyright: IBM
"""

from typing import Never


import logging
import uuid

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


NET_INTERFACES = "/net/ifaces"

logger = logging.getLogger(__name__)


class Interfaces(object):

    def __init__(self, base_url, username, password):
        super(Interfaces, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_address(self, interface_label, address=None, mask_or_prefix=None, enabled=True, 
            allow_management=False, broadcast_address=None, override_subnet_checking=False) -> Response:
        """
        Add a new address to an existing interface.
        
        Args:
            interface_label (:obj:`str`): Name of the existing interface to add a new address to
            address (:obj:`str`): IPv4 address to add
            mask_or_prefix (:obj:`str`): subnet mask or prefix. e.g. "255.255.255.0", "24".
            enabled (`bool`): true to enabled this address, otherwise false. 
            allow_management (`bool`): true if this is the primary management address.
            broadcast_address (:obj:`str`): Broadcast address on the subnet.
            override_subnet_checking (`bool`): true to indicate that the check for overlapping subnets should not be executed. 
                            The default value of false is used if this data is not supplied.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the interface configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.list_interfaces()

        if response.success and response.json:
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
                    address_data.add_value_string("broadcastAddress", broadcast_address)
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

    def list_interfaces(self) -> Response:
        """
        List all known interface properties.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the interfaces are returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(NET_INTERFACES)
        response.success = response.status_code == 200

        return response


    def create_interface(self, name=None, comment=None, label=None, enabled=True, vlan_id=None, ipv4={}, ipv6={}) -> Response:
        """
        Create a new network interface

        Args:
            name (:obj:`str`): Name of the interface
            comment (:obj:`str`): Comment to identify the interface object.
            label (:obj:`str`): System label of the interface. e.g. "1.1".
            enabled (`bool`): true if the interface should be used, otherwise false.
            vlan_id (:obj:`str`): vlan id of interface in range "0".."4094".
            ipv4 (:obj:`dict`): ipv4 configuration of the interface
            ipv6 (:obj:`dict`): ipv6 configuration of the interface

        Example Request::

            {
                "name"    : "Demo",
                "objType" : "interface",
                "label"   : "1.1",
                "enabled" : true,
                "bondingMode": "none",
                "ipv4"    : {
                  "dhcp"      : {
                    "enabled" : false,
                    "allowManagement" : false,
                    "providesDefaultRoute": false
                  },
                  "addresses" : [{
                    "uuid"            : "1e107d3b-0748-4e02-96f7-581cb8655356",
                    "objType"         : "ipv4Address",
                    "address"         : "10.0.254.1",
                    "maskOrPrefix"    : "24",
                    "broadcastAddress": null,
                    "allowManagement" : false,
                    "isPrimary"       : false,
                    "enabled"         : true
                  }]
                },
                "ipv6"    : {
                  "dhcp"      : {
                    "enabled" : false,
                    "allowManagement" : false
                  },
                  "addresses" : []
                }
            }

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the interface is returned as JSON and can be accessed from
            the response.json attribute

        """
        raise RuntimeError("Not implemented")


    def update_interface(self, uuid, name=None, comment=None, enabled=True, vlan_id=0, bonding_mode=None,
            bonded_to=None, ipv4_address=None, ipv4_mask_or_prefix=None, ipv4_broadcast_address=None,
            ipv4_allow_management=False, ipv4_enabled=True, ipv4_dhcp_enabled=True, 
            ipv4_dhcp_allow_management=False, ipv4_dhcp_default_route=False, ipv4_dhcp_route_metric=0,
            ipv4_override_subnet_checking=False, ipv6_address=None, ipv6_prefix_length=None, 
            ipv6_allow_management=False, ipv6_enabled=False, ipv6_dhcp_enabled=False, ipv6_dhcp_allow_management=False) -> Response:
        """
        Update the configuration of an existing interface

        Args:
            uuid (:obj:`str`): unique id of the object.
            name (:obj:`str`): name of the object.
            comment (:obj:`str`, optional): comment to identify the interface object.
            enabled `bool`): true if the interface should be used, otherwise false.
            vlan_id (`int`): optional vlan id of interface in range "0".."4094".
            bonding_mode (:obj:`str`): none|slave|balance-rr|active-backup|balance-xor|broadcast|802.3ad|balance-tlb|balance-alb. 
                            Defaults to none if not provided.
            bonded_to (:obj:`str`): Only required when bondingMode == 'slave'. Set to UUID of interface bonded to.
            ipv4_address (:obj:`str`): static address configuration details. 
            ipv4_mask_or_prefix (:obj:`str`): subnet mask or prefix. e.g. "255.255.255.0", "24".
            ipv4_broadcast_address (:obj:`str`): broadcast address on the subnet.
            ipv4_allow_management (`boolean`): true to allow management access on this address.
            ipv4_dhcp_default_route (`boolean`): true if the dhcp configuration should specify a default route.
            ipv4_dhcp_route_metric (`int`): optional default route metric if providesDefaultRoute is true. 
            ipv4_override_subnet_checking (`boolean`): true to indicate that the check for overlapping subnets should not be executed. 
                            The default value of false is used if this data is not supplied. 
            ipv6_address (:obj:`str`): IPv6 address value.
            ipv6_prefix_length (:obj:`str`): prefix length in range "1".."128".
            ipv6_allow_management (`bool`): true to allow management access on this address.
            ipv6_enabled (`bool`): true to enabled this address, otherwise false. 
            ipv6_dhcp_allow_management (`bool`): true to allow management access on this address.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the updated interface is returned as JSON and can be accessed from
            the response.json attribute
        """
        raise RuntimeError("Not implemented")

    def delete_interface(self, uuid) -> Response:
        """
        Delete a VLAN interface configuration

        Args:
            uuid (:obj:`str`): Unique id of the interface to delete.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        raise RuntimeError("Not implemented")

class Interfaces10000(Interfaces):


    def create_interface(self, name=None, comment=None, label=None, enabled=True, vlan_id=None, ipv4={}, ipv6={}) -> Response:
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("comment", comment)
        data.add_value_string("label", label)
        data.add_value_boolean("enabled", enabled)
        data.add_value_string("vlanId", vlan_id)
        data.add_value_not_empty("ipv4", ipv4)
        data.add_value_not_empty("ipv6", ipv6)

        response = self.client.post_json(NET_INTERFACES, data.data)
        response.success = response.status_code == 200

        return response


    def delete_interface(self, uuid) -> Response:
        endpoint = "{}/{}".format(NET_INTERFACES, uuid)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204
        return response


    def update_interface(self, uuid, name=None, comment=None, enabled=True, vlan_id=None, bonding_mode=None,
            bonded_to=None, ipv4_address=None, ipv4_mask_or_prefix=None,
            ipv4_broadcast_address=None, ipv4_allow_management=False, ipv4_enabled=True, ipv4_dhcp_enabled=True, 
            ipv4_dhcp_allow_management=False, ipv4_dhcp_default_route=False, ipv4_dhcp_route_metric=0,
            ipv4_override_subnet_checking=False, ipv6_address=None, ipv6_prefix_length=None, 
            ipv6_allow_management=False, ipv6_enabled=False, ipv6_dhcp_enabled=False, ipv6_dhcp_allow_management=False) -> Response:
        data = DataObject()
        ipv4 = DataObject()
        if ipv4_address:
            ipv4_address_data = DataObject()
            ipv4_address_data.add_value_string("uuid", uuid)
            ipv4_address_data.add_value_string("address", ipv4_address)
            ipv4_address_data.add_value_string(
                    "maskOrPrefix", ipv4_mask_or_prefix)
            ipv4_address_data.add_value_string("objType", "ipv4Address")
            ipv4_address_data.add_value_string(
                    "broadcastAddress", ipv4_broadcast_address)
            ipv4_address_data.add_value_boolean("enabled", ipv4_enabled)
            ipv4_address_data.add_value_boolean("allowManagement", ipv4_allow_management)
            ipv4.add_value_not_empty("addresses", [ipv4_address_data.data])
        
        ipv4_dhcp_data = DataObject()
        ipv4_dhcp_data.add_value_boolean("enabled", ipv4_dhcp_enabled)
        ipv4_dhcp_data.add_value_boolean("allowManagement", ipv4_dhcp_allow_management)
        ipv4_dhcp_data.add_value_boolean("providesDefaultRoute", ipv4_dhcp_default_route)
        if ipv4_dhcp_route_metric != None:
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
        data.add_value_boolean('enabled', enabled)
        data.add_value_string('vlanId', vlan_id)
        data.add_value_string('bondingMode', bonding_mode)
        data.add_value_string('bondedTo', bonded_to)

        endpoint = ("%s/%s" % (NET_INTERFACES, uuid))
        logger.debug("interface: {}".format(data.data))
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200
        return response
