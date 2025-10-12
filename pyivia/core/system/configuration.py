"""
@copyright: IBM
"""

import logging
import re

from requests import get

from pyivia.util.restclient import RESTClient
from .restartshutdown import RestartShutdown


PENDING_CHANGES = "/isam/pending_changes"
PENDING_CHANGES_DEPLOY = "/isam/pending_changes/deploy"

logger = logging.getLogger(__name__)


class Configuration(object):

    def __init__(self, base_url, username, password):
        super(Configuration, self).__init__()
        self.client = RESTClient(base_url, username, password)
        self._base_url = base_url
        self._username = username
        self._password = password

    def deploy_pending_changes(self):
        """
        Deploy the current set of pending changes. This may result in additional actions such as LMI restart or 
        appliance restart.


        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the obligations are returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.get_pending_changes()

        if response.success and response.json:
            if response.json.get("changes", []):
                response = self._deploy_pending_changes()
            else:
                logger.info("No pending changes to be deployed.")

        return response

    def revert_pending_changes(self):
        """
        Revert the current set of pending changes.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        response = self.client.delete_json(PENDING_CHANGES)
        response.success = response.status_code == 200

        return response

    def get_pending_changes(self):
        """
        Get a list of the pending changes for the configured username.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the pending changes are returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(PENDING_CHANGES)
        response.success = response.status_code == 200

        return response

    def _deploy_pending_changes(self):
        response = self.client.get_json(PENDING_CHANGES_DEPLOY)
        if response.json:
            response.success = (response.status_code == 200 and
                                    response.json.get("result", -1) == 0)
        else:
            response.success = False
            return response

        if response.success:
            status = response.json.get("status")
            """
            status (`int`): A status code for the result. The status code is a bitmask indicating if the deployment 
                        operation succeeded and if any additional action is needed for the changes to take affect. 
                        The options are: 
                            0 - successful; 
                            1: failure; 
                            2: an appliance restart is required; 
                            4: an LMI restart is required; 
                            8: an LMI restart is required; 
                            16: either web reverse proxy or authorization server instances now require a restart 
                                (the message will indicate the instance names); 
                            32: the runtime profile was restarted as a result of the operation; 
                            64: the runtime profile failed to restart; 
                            128: a runtime profile restart is required; 
                            256: the runtime profile was reloaded as a result of the operation; 
                            512: the runtime profile failed to reload; 
                            1024: a runtime profile reload is require
            """
            if status == 0:
                logger.info("Successful operation. No further action needed.")
            else:
                if (status & 1) != 0:
                    logger.error(
                        "Deployment of changes resulted in good result but failure status: %i",
                        status)
                    response.success = False
                if (status & 2) != 0:
                    logger.error(
                        "Appliance restart required - halting: %i", status)
                    response.success = False
                if (status & 4) != 0 or (status & 8) != 0:
                    logger.info(
                        "Restarting LMI as required for status: %i", status)
                    self._restart_lmi()
                if (status & 16) != 0:
                    logger.info(
                        "Deployment of changes indicates a server needs restarting: %i",
                        status)
                if (status & 32) != 0:
                    logger.info(
                        "Runtime restart was performed for status: %i", status)
                    self._restart_runtime()

        return response

    def _restart_lmi(self):
        restart_shutdown = RestartShutdown(
                self._base_url, self._username, self._password)
        restart_shutdown.restart_lmi()


    def _restart_runtime(self):
        restart_shutdown = RestartShutdown(
                self._base_url, self._username, self._password)
        restart_shutdown.restart_runtime()
