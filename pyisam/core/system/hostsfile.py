"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


HOST_RECORDS = "/isam/host_records"

logger = logging.getLogger(__name__)


class HostsFile(object):

    def __init__(self, base_url, username, password):
        super(HostsFile, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def add_hostname(self, address, hostname=None):
        data = DataObject()
        data.add_value_string("name", hostname)

        endpoint = "%s/%s/hostnames" % (HOST_RECORDS, address)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def create_record(self, address, hostname_list):
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
        endpoint = "%s/%s/hostnames" % (HOST_RECORDS, address)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def delete_record(self, address, hostname=None):
        endpoint = "%s/%s" % (HOST_RECORDS, address)
        if hostname != None:
            endpoint += "/hostnames/%s" % (hostname)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response
