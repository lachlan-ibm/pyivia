""""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


FIPS_CONFIG = "/fips_cfg"

logger = logging.getLogger(__name__)


class FIPS(object):

    def __init__(self, base_url, username, password):
        super(FIPS, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def update_settings(self, fips_enabled=None, tls_v10_enabled=None, tls_v11_enabled=None):
        '''
        Enable FIPS compliance on a Verify Identity Access appliance.

        .. note: If FIPS mode is enabled then a restart of the appliance may be required.

        Args:
            fips_enabled (`bool`): Enable FIPS 140-2 Mode
            tls_v10_enabled (`bool`): Allow TLS v1.0 for LMI sessions
            tls_v11_enabled (`bool`): Allow TLS v1.1 for LMI sessions

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the updated FIPS settings are returned as JSON and can be accessed from
            the response.json attribute
        '''
        data = DataObject()
        data.add_value_boolean("fipsEnabled", fips_enabled)
        data.add_value_boolean("tlsv10Enabled", tls_v10_enabled)
        data.add_value_boolean("tlsv11Enabled", tls_v11_enabled)

        response = self.client.put_json(FIPS_CONFIG, data.data)
        response.success = response.status_code == 200

        return response


    def get_settings(self):
        '''
        Get the current FIPS configuration.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the updated FIPS settings are returned as JSON and can be accessed from
            the response.json attribute
        '''
        response = self.client.get_json(FIPS_CONFIG)
        response.success = response.status_code == 200

        return response
