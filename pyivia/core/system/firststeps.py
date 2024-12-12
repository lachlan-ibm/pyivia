"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


SETUP_COMPLETE = "/setup_complete"
SERVICE_AGREEMENTS_ACCEPTED = "/setup_service_agreements/accepted"

logger = logging.getLogger(__name__)


class FirstSteps(object):

    def __init__(self, base_url, username, password):
        super(FirstSteps, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_setup_status(self):
        """
        Get the status of the appliance setup.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the current status is returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(SETUP_COMPLETE)
        response.success = response.status_code == 200

        return response

    def set_setup_complete(self):
        """
        Complete the first steps setup process.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        response = self.client.put_json(SETUP_COMPLETE)
        response.success = response.status_code == 200

        return response

    def get_sla_status(self):
        """
        Get the SLA status.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the SLA status is returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(SERVICE_AGREEMENTS_ACCEPTED)
        response.success = response.status_code == 200

        return response

    def set_sla_status(self, accept=True):
        """
        Accept the SLA.

        Args:
            accept (`bool`): Accept the SLA

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        data.add_value("accepted", accept)

        response = self.client.put_json(SERVICE_AGREEMENTS_ACCEPTED, data.data)
        response.success = response.status_code == 200

        return response
