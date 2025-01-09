"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


PDADMIN = "/isam/pdadmin"

logger = logging.getLogger(__name__)


class PolicyAdmin(object):

    def __init__(self, base_url, username, password):
        super(PolicyAdmin, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def execute(self, admin_id, admin_pwd, commands):
        '''
        Execute a command using the pdadmin command line utility on a Verify Identity Access Appliance or Container.

        Args:
            admin_id (:obj:`str`): The user to authenticate to the policy directory with.
            admin_pwd (:obj:`str`): The password to authenticate to the policy directory with.
            commands (:obj:`list` of :obj:`str`): A list of commands to run with the pdadmin tool.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the stdout and stderr from the completed commands is returned as JSON 
            and can be accessed from the response.json attribute
        '''
        data = DataObject()
        data.add_value_string("admin_id", admin_id)
        data.add_value_string("admin_pwd", admin_pwd)
        data.add_value("commands", commands)

        response = self.client.post_json(PDADMIN, data.data)
        response.success = response.status_code == 200

        return response
