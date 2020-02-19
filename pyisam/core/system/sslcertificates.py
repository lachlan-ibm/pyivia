"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


SSL_CERTIFICATES = "/isam/ssl_certificates"

logger = logging.getLogger(__name__)


class SSLCertificates(object):

    def __init__(self, base_url, username, password):
        super(SSLCertificates, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def import_personal(self, kdb_id, file_path, password=None):
        response = Response()

        try:
            with open(file_path, 'rb') as certificate:
                data = DataObject()
                data.add_value_string("operation", "import")
                data.add_value_string("password", password)

                files = {"cert": certificate}

                endpoint = ("%s/%s/personal_cert" % (SSL_CERTIFICATES, kdb_id))

                response = self.client.post_file(
                    endpoint, data=data.data, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def import_signer(self, kdb_id, file_path, label=None):
        response = Response()

        try:
            with open(file_path, 'rb') as certificate:
                data = DataObject()
                data.add_value_string("label", label)

                files = {"cert": certificate}

                endpoint = ("%s/%s/signer_cert" % (SSL_CERTIFICATES, kdb_id))

                response = self.client.post_file(
                    endpoint, data=data.data, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def load_signer(self, kdb_id, server=None, port=None, label=None):
        data = DataObject()
        data.add_value_string("operation", "load")
        data.add_value_string("label", label)
        data.add_value_string("server", server)
        data.add_value("port", port)

        endpoint = ("%s/%s/signer_cert" % (SSL_CERTIFICATES, kdb_id))

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def get_database(self, kdb_id):
        endpoint = ("%s/%s/details" % (SSL_CERTIFICATES, kdb_id))

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_databases(self):
        endpoint = SSL_CERTIFICATES

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_personal(self, kdb_id, label=None):
        endpoint = ("%s/%s/personal_cert" % (SSL_CERTIFICATES, kdb_id))

        if label is not None:
            endpoint += "/%s" %(label)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_signer(self, kdb_id, label=None):
        endpoint = ("%s/%s/signer_cert" % (SSL_CERTIFICATES, kdb_id))

        if label is not None:
            endpoint += "/%s" %(label)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_database(self, kdb_name,
            type=None, token_label=None, passcode=None, hsm_type=None,
            ip=None, port=None, kneti_hash=None, esn=None,
            secondary_ip=None, secondary_port=None,
            secondary_kneti_hash=None, secondary_esn=None,
            use_rfs=None, rfs=None, rfs_port=None,
            rfs_auth=None, update_zip=None, safenet_pw=None):
        endpoint = SSL_CERTIFICATES

        data = DataObject()
        data.add_value_string("kdb_name", kdb_name)
        data.add_value_string("token_label", token_label)
        data.add_value_string("passcode", passcode)
        data.add_value_string("type", type)
        data.add_value_string("token_label", token_label)
        data.add_value_string("passcode", passcode)
        data.add_value_string("hsm_type", hsm_type)
        data.add_value_string("ip", ip)
        data.add_value("port", port)
        data.add_value_string("kneti_hash", kneti_hash)
        data.add_value_string("esn", esn)
        data.add_value_string("secondary_ip", secondary_ip)
        data.add_value("secondary_port", secondary_port)
        data.add_value_string("secondary_kneti_hash", secondary_kneti_hash)
        data.add_value_string("secondary_esn", secondary_esn)
        data.add_value_string("use_rfs", use_rfs)
        data.add_value("rfs", rfs)
        data.add_value("rfs_port", rfs_port)
        data.add_value("rfs_auth", rfs_auth)
        data.add_value_string("safenet_pw", safenet_pw)

        if update_zip:
            raise NotImplementedError

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response
