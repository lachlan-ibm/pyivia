"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


TIME_CONFIG = "/core/time_cfg"

logger = logging.getLogger(__name__)


class DateTime(object):

    def __init__(self, base_url, username, password):
        super(DateTime, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def update(self, enable_ntp=True, ntp_servers=None, time_zone=None, date_time="0000-00-00 00:00:00"):
        """
        Update the date/time settings of an appliance.

        Args:
            enable_ntp (`bool`): Should NTP be enabled.
            ntp_servers (:obj:`str`): A comma-separated list of NTP server hostnames or IP addresses.
            time_zone (:obj:`str`): The id of the timezone the appliance is operating in.
            date_time (:obj:`str`): The current date and time, in the format "YYYY-MM-DD HH:mm:ss"

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the new date/time configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        data = DataObject()
        data.add_value_string("dateTime", date_time)
        data.add_value_string("ntpServers", ntp_servers)
        data.add_value_string("timeZone", time_zone)
        data.add_value("enableNtp", enable_ntp)

        response = self.client.put_json(TIME_CONFIG, data.data)
        response.success = response.status_code == 200

        return response

    def get(self):
        """
        Get the current date/time settings of an appliance.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the date/time configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(TIME_CONFIG)
        response.success = response.status_code == 200

        return response