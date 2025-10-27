""""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


CLI_COMMAND = "/core/cli"

logger = logging.getLogger(__name__)


class CLICommands(object):

    def __init__(self, base_url, username, password):
        super(CLICommands, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def run(self, command=None,input_array=None):
        """
        Run a CLI command.

        Args:
            command (:obj:`str`):The CLI command to run. The different levels of the command are separated by "/".
            input_array (:obj:`list` of :obj:`str`): An array of the user interaction responses required to run the 
                        cified response. This parameter is required if the specified CLI command requires user interaction. 
        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the command output is returned as JSON and can be accessed from
            the response.json attribute
        """
        data = DataObject()
        data.add_value_string("command", command)
        data.add_value("input", input_array)
        
        response = self.client.post_json(CLI_COMMAND, data.data)
        response.success = response.status_code == 200

        return response
