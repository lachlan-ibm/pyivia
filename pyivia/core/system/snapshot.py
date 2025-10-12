import logging

from pyivia.util.model import Response
from pyivia.util.restclient import RESTClient


logger = logging.getLogger(__name__)

SNAPSHOT = '/snapshots'
SNAPSHOT_APPLY = SNAPSHOT + '/apply'

class Snapshot(object):

    def __init__(self, base_url, username, password):
        super(Snapshot, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def upload(self, snapshot):
        '''
        Upload the given file to an appliance as a configuration snapshot.
        File should follow the naming convention ``ivia_<version>.<snapshot id>.snapshot``

        Args:
            snapshot (:obj:`str`): Path to file to be imported as configuration snapshot file.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        response = Response()
        response.success = False
        try:
            files = {"filename": open(snapshot, 'rb')}
            response = self.client.post_file(SNAPSHOT, files=files)
            response.success = True if response.json and 'status' in response.json and response.json['status'] == 200 else False
        except Exception as e:
            logger.error(e)

        return response


    def download(self, snapshot_id, snapshot):
        '''
        Download the given file to an appliance as a configuration snapshot.

        Args:
            snapshot_id (:obj:`str`): The id of the snapshot to be downloaded. Id should 
                                    follow the naming convention ``ivia_<version>.<snapshot id>.snapshot``
            snapshot (:obj:`str`): Path to file to be imported as configuration snapshot file.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        response = Response()
        response.success = False
        try:
            endpoint = "{}/{}".format(SNAPSHOT, snapshot_id)
            response = self.client.get_file(endpoint, snapshot)
            response.success = response.status_code == 200
        except Exception as e:
            logger.error(e)

        return response


    def apply(self, snapshot_id):
        '''
        Apply a configuration snapshot.

        Args:
            snapshot_id (:obj:`str`): The id of the snapshot to be applied.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = "{}/{}".format(SNAPSHOT_APPLY, snapshot_id)
        response = self.client.post_json(endpoint)
        response.success = response.status_code == 204

        return response


    def delete(self, snapshot_id):
        '''
        Delete an existing configuration snapshot.

        Args:
            snapshot_id (:obj:`str`): The id of the snapshot to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = "{}/{}".format(SNAPSHOT, snapshot_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def list(self):
        '''
        Get a list of all known configuration snapshots.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the snapshot files are returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = self.client.get_json(SNAPSHOT)
        response.success = response.status_code == 200

        return response
