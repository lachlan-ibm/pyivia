""""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient

APPLICATION_LOGS = "/isam/application_logs"

logger = logging.getLogger(__name__)


class ApplicationLog(object):

    def __init__(self, base_url, username, password):
        super(ApplicationLog, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_application_log(self, path) -> Response:
        """
        Download a log file from an applaince

        Args:
            path (:obj:`str`): The relative path of the file to be retrieved.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the file contents is returned as JSON and can be accessed from
            the response.json attribute
        """
        parameters = DataObject()
        parameters.add_value_string("type", "File")

        endpoint = f"{APPLICATION_LOGS}/{path}"
        response = self.client.get_json(endpoint, parameters.data)
        response.success = response.status_code == 200

        return response


    def delete_application_logs(self, paths=[]) -> Response:
        """
        Delete one or more log files on an appliance

        Args:
            paths (:obj:`list` of :obj:`str`): The list of files to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        files = DataObject()
        for path in paths:
            files.add_value_string("fullname", path)

        parameters = DataObject()
        parameters.add_value_not_empty("files", files.data)

        endpoint = f"{APPLICATION_LOGS}?action=delete"

        response = self.client.put_json(endpoint, parameters.data)
        response.success = response.status_code == 200

        return response


    def clear_application_logs(self, paths=[]) -> Response:
        """
        Clear one or more log files on an appliance

        Args:
            paths (:obj:`list` of :obj:`str`): The list of files to clear.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        files = DataObject()
        for path in paths:
            files.add_value_string("fullname", path)

        parameters = DataObject()
        parameters.add_value_not_empty("files", files.data)

        endpoint = f"{APPLICATION_LOGS}?action=clear"
        response = self.client.put_json(endpoint, parameters.data)
        response.success = response.status_code == 200

        return response
