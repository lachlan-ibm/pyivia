""""
@copyright: IBM
"""

import logging
import time

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


LMI = "/lmi"
LMI_RESTART = "/core/restarts/restart_server"
APPLIANCE_RESTART = "/diagnostics/restart_shutdown/reboot"
RUNTIME = "/mga/runtime_profile/v1"
RUNTIME_RESTART = "/mga/runtime_profile/local/v1"

logger = logging.getLogger(__name__)


class RestartShutdown(object):

    def __init__(self, base_url, username, password):
        super(RestartShutdown, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def get_lmi_status(self):
        """
        Get the current status of the management interface.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the status of the management interface is returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(LMI)
        response.success = response.status_code == 200

        return response


    def get_runtime_status(self):
        """
        Get the status of the federated runtime server.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the status of the runtime server is returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(RUNTIME)
        response.success = True if response.status_code == 200 \
                and response.json \
                and response.json.get('return_code') == 0 \
                    else False

        return response


    def restart_lmi(self):
        """
        Restart the management interface.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        last_start = -1

        response = self.get_lmi_status()
        if response.success and response.json:
            last_start = response.json[0].get("start_time", -1)

        if last_start > 0:
            data = DataObject()
            data.add_value_boolean("restart", True)
            response = self.client.post_json(LMI_RESTART, data.data)
            response.success = True if response.status_code == 200 \
                    and response.json \
                    and response.json.get("restart", False) == True \
                        else False

            if response.success:
                logger.info("Waiting for LMI to restart...")
                self._wait_on_lmi(last_start)
        else:
            logger.error("Invalid start time was retrieved: %i", last_start)
            response.success = False

        return response


    def _wait_on_lmi(self, last_start, sleep_interval=3):
        count = 0
        if last_start > 0:
            restart_time = last_start

            while (restart_time <= 0 or restart_time == last_start) and (count < 10):
                logger.debug(
                    "last_start: %i, restart_time: %i", last_start,
                    restart_time)
                time.sleep(sleep_interval)

                try:
                    response = self.get_lmi_status()

                    if response.success and response.json:
                        restart_time = response.json[0].get("start_time", -1)
                except:
                    restart_time = -1
                count += 1 #Wait at most 30 seconds; sleep_interval * 10

            time.sleep(sleep_interval)
        else:
            logger.error("Invalid last start time: %i", last_start)
        logger.debug("Wait for lmi to stabilize")
        time.sleep(sleep_interval)


    def restart_appliance(self):
        last_start = -1

        response = self.get_lmi_status()
        if response.success and response.json:
            last_start = response.json[0].get("start_time", -1)

        if last_start > 0:
            response = self.client.post_json(APPLIANCE_RESTART)
            response.success = True if response.status_code == 200 \
                    and response.json \
                    and response.json.get("status", False) == True \
                        else False

            if response.success:
                logger.info("Waiting for LMI to restart...")
                self._wait_on_lmi(last_start)
        else:
            logger.error("Invalid start time was retrieved: %i", last_start)
            response.success = False

        return response


    def _wait_on_runtime(self, last_start, sleep_interval=3):
        if last_start > 0:
            restart_time = last_start
            count = 0

            while restart_time <= 0 or restart_time == last_start:
                logger.debug("last_start: %i, restart_time: %i", last_start,
                        restart_time)
                time.sleep(sleep_interval)

                try:
                    response = self.get_runtime_status()
                    if response.success and response.json:
                        restart_time = response.json.get("last_start", -1)

                except:
                    restart_time = -1

                count += 1
                if count > 10: # defaults to 30s total loop
                    logger.error("Failed to restart runtime after %i seconds", sleep_interval * count)
                    break

        else:
            logger.error("Invalid runtime status was retrieved: %i", last_start)


    def restart_runtime(self):
        """
        Restart the federated runtime server

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        last_start = -1

        response = self.get_runtime_status()
        if response.success and response.json:
            last_start = response.json.get("last_start", -1)

        if last_start >= 0:
            response = self.client.put_json(RUNTIME_RESTART, {"operation":"restart"})
            response.success = response.status_code == 200

            if response.success:
                logger.info("Waiting for Runtime to restart. . .")
                self._wait_on_runtime(last_start)

        else:
            logger.error("Invalid start time was retrieved: %i", last_start)
            response.success = False

        return response
