import logging

from pyisva.util.model import DataObject, Response
from pyisva.util.restclient import RESTClient


logger = logging.getLogger(__name__)

ENDPOINT = '/snapshots'

class Snapshot(object):

    def __init__(self, base_url, username, password):
        super(Snapshot, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def upload(self, snapshot):
        response = Response()
        response.success = False
        try:
            files = {"filename": open(snapshot, 'rb')}
            response = self.client.post_files(ENDPOINT, files=files)
            response.success = True if response.json and 'status' in response.json and response.json['status'] == 200 else False
        except Exception as e:
            logger.error(e)

        return response


    def download(self, snapshot_id):
        return


    def apply(self, snapshot_id):
        return

    def delete(self, snapshot_id):
        return


    def list(self):
        return
