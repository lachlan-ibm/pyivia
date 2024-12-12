"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


HOST_RECORDS = "/isam/host_records"

logger = logging.getLogger(__name__)


class HostsFile(object):

    def __init__(self, base_url, username, password):
        super(HostsFile, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def update_record(self, address, hostname=None):
        """
        Add a host file entry.

        Args:
            address (:obj:`str`): The IP address of the host record.
            hostname (:obj:`str`): The hostname in the host record.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the new record is returned as JSON and can be accessed from
            the response.json attribute
        """
        data = DataObject()
        data.add_value_string("name", hostname)

        endpoint = "%s/%s/hostnames" % (HOST_RECORDS, address)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def create_record(self, address, hostname_list):
        """
        Craete a new host record and add 0 or more host names

        Args:
            address (:obj:`str`): The host IP address to create.
            hostname_list (:obj:`list` of :obj:`str`): list of host names to associate with address

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the new record is returned as JSON and can be accessed from
            the response.json attribute
        """
        hostnames = []
        for entry in hostname_list:
            hostnames.append({"name":str(entry)})

        data = DataObject()
        data.add_value_string("addr", address)
        data.add_value_not_empty("hostnames", hostnames)

        response = self.client.post_json(HOST_RECORDS, data.data)
        response.success = response.status_code == 200

        return response

    def get_record(self, address):
        """
        Get a list of host names associated with an address

        Args:
            address (:obj:`str`): The IP address of the host record.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the host records are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = "%s/%s/hostnames" % (HOST_RECORDS, address)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def list_records(self):
        """
        Get a list host addresses

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the host addresses are returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(HOST_RECORDS)
        response.success = response.status_code == 200
        return response


    def delete_record(self, address=None):
        """
        Delete a host record (address and associated host names)

        Args:
            address (:obj:`str`): The IP address of the host record.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute
        """
        endpoint = "%s/%s" % (HOST_RECORDS, address)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200
        return response

    def delete_host_name(self, address=None, host_name=None):
        """
        Delete a host name from a host address.

        Args:
            address (:obj:`str`): The IP address of the host record.
            host_name (:obj:`str`): The hostname of the host record.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute
        """
        endpoint = "%s/%s/hostnames/%s" % (HOST_RECORDS, address, host_name)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200
        return response
