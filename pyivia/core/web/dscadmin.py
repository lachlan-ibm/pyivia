""""
@copyright: IBM
"""

import logging
import urllib.parse

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


DSC_ADMIN_REPLICAS = "/isam/dsc/admin/replicas"

logger = logging.getLogger(__name__)


class DSCAdmin(object):

    def __init__(self, base_url, username, password):
        super(DSCAdmin, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def list_replica_sets(self):
        """
        List the replica sets in the DSC server.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the DSC replicas are returned as JSON and can be accessed from
            the response.json attribute.

        """
        response = self.client.get_json(DSC_ADMIN_REPLICAS)
        response.success = response.status_code == 200

        return response

    def list_servers(self, replica_set):
        """
        List the servers (WebSEALs) for a replica set.

        Args:
            replica_set (:obj:`str`): The replica set to list servers for

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the DSC replica servers are returned as JSON and can be accessed from
            the response.json attribute.

        """
        replica_set = urllib.parse.quote(replica_set, safe='')
        endpoint = "%s/%s/servers" % (DSC_ADMIN_REPLICAS, replica_set)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def list_user_sessions(self, replica_set, user_name_pattern, max_results):
        """
        List user sessions in a replica set.

        Args:
            replica_set (:obj:`str`): The replica set to query
            user_name_pattern (:obj:`str`): The regex pattern used to search for user sessions
            max_results (:obj:`str`): Maximum number of sessions to return.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the DSC replica servers are returned as JSON and can be accessed from
            the response.json attribute.

        """
        parameters = DataObject()
        parameters.add_value_string("user", user_name_pattern)
        parameters.add_value_string("max", max_results)

        replica_set = urllib.parse.quote(replica_set, safe='')
        endpoint = "%s/%s/sessions" % (DSC_ADMIN_REPLICAS, replica_set)

        response = self.client.get_json(endpoint, parameters.data)
        response.success = response.status_code == 200

        return response

    def terminate_session(self, replica_set, session):
        """
        Terminate a specific session.

        Args:
            replica_set (:obj:`str`): The replica set the session is stored in
            session (:obj:`str`): The session identifier

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

        """
        replica_set = urllib.parse.quote(replica_set, safe='')
        session = urllib.parse.quote(session, safe='')
        endpoint = "%s/%s/sessions/session/%s" % (DSC_ADMIN_REPLICAS, replica_set, session)

        response = self.client.delete_json(endpoint)
        response.success = (response.status_code == 200 or response.status_code == 204)

        return response

    def terminate_user_sessions(self, replica_set, user_name):
        """
        Terminate all sessions for the specified user.

        Args:
            replica_set (:obj:`str`): The replica set the session is stored in
            user_name (:obj:`str`): The user who's session's should be invalidated.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.
        """
        replica_set = urllib.parse.quote(replica_set, safe='')
        user_name = urllib.parse.quote(user_name, safe='')
        endpoint = "%s/%s/sessions/user/%s" % (DSC_ADMIN_REPLICAS, replica_set, user_name)

        response = self.client.delete_json(endpoint)
        response.success = (response.status_code == 200 or response.status_code == 204)

        return response
