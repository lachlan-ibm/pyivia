"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


SSL_CERTIFICATES = "/isam/ssl_certificates"

logger = logging.getLogger(__name__)


class SSLCertificates(object):

    def __init__(self, base_url, username, password):
        super(SSLCertificates, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def import_personal(self, kdb_id, file_path, password=None, label=None):
        """
        Import a personal certificate (private key & X509 certificate) into a SSL database

        Args:
            kdb_id (:obj:`str`): Name of the certificate database.
            file_path (:obj:`str`): Absolute path to file containing #PKCS12 PKI
            password (:obj:`str`): Password to unlock personal certificate

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        response = Response()

        try:
            with open(file_path, 'rb') as certificate:
                data = DataObject()
                data.add_value_string("operation", "import")
                data.add_value_string("password", password)
                data.add_value_string("label", label)

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
        """
        Import a X509 certificate into a SSL database

        Args:
            kdb_id (:obj:`str`): Name of the certificate database.
            file_path (:obj:`str`): Absolute path to file containing PEM encoded certificate.
            label (:obj:`str`): Alias for certificate in SSL database

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
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
        """
        Load a X509 certificate from a TLS connection.

        Args:
            kdb_id (:obj:`str`): Name of the certificate database.
            server (:obj:`str`): The name or address of the server which holds the server certificate.
            port (`int`): The port over which the certificate request will be made to the server. 
            label (:obj:`str`): The label which will be used to identify the certificate within the key file.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the loaded certificate is returned as JSON and can be accessed from
            the response.json attribute
        """
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
        """
        Get a SSL certificate database details

        Args:
            kdb_id (:obj:`str`): Name of the certificate database.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the SSL database details are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = ("%s/%s/details" % (SSL_CERTIFICATES, kdb_id))

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_databases(self):
        """
        List the SSL databases

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the SSL databases are returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = SSL_CERTIFICATES

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_personal(self, kdb_id, label=None):
        """
        Get the X509 certificate from a personal certificate in a SSL database

        Args:
            kdb_id (:obj:`str`): Name of the certificate database.
            label (:obj:`str`): Name of the personal certificate to retrieve.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the certificate is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = ("%s/%s/personal_cert" % (SSL_CERTIFICATES, kdb_id))

        if label is not None:
            endpoint += "/%s" %(label)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_signer(self, kdb_id, label=None):
        """
        Get a X509 certificate from the list of signer certificates.

        Args:
            kdb_id (:obj:`str`): Name of the certificate database.
            label (:obj;`str`): Name of the signer certificate.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the X509 certificate is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = ("%s/%s/signer_cert" % (SSL_CERTIFICATES, kdb_id))

        if label is not None:
            endpoint += "/%s" %(label)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_database(self, kdb_name, db_type=None, token_label=None, passcode=None, hsm_type=None, ip=None, port=None, 
            kneti_hash=None, esn=None, secondary_ip=None, secondary_port=None, secondary_kneti_hash=None, secondary_esn=None,
            use_rfs=None, rfs=None, rfs_port=None, rfs_auth=None, update_zip=None, safenet_pw=None):
        """
        Create a SSL database

        Args:
            kdb_name (:obj:`str`): The new certificate database name that is used to uniquely identify the certificate 
                            database.
            db_type (:obj:`str`): The type of the new certificate database. Valid options are "kdb" for local databases 
                            and "p11" for network databases.
            token_label (:obj:`str`): The token label of the certificate database.
            passcode (:obj:`str`): The passcode of the certificate database.
            hsm_type (:obj:`str`): The type of network HSM device which is being used. Required if the database type is 
                            "p11". Valid types are "ncipher" or "safenet".
            ip (:obj:`str`): The IP address of the module. Required if the database type is "p11".
            port (`int`, optional) :The port of the module. Only valid if the hsm_type is "ncipher".
            kneti_hash (:obj:`str`, optional): The hash of the KNETI key. Only valid if the hsm_type is "ncipher".
            esn (:obj:`str`, optional): The Electronic Serial Number (ESN) of the module. Only valid if the hsm_type is 
                            "ncipher".
            secondary_ip (:obj:`str`, optional): The IP address of the secondary module. Only valid if the hsm_type is 
                            "ncipher".
            secondary_port (`int`, optional): The port of the secondary module. Only valid if the hsm_type is "ncipher"
            secondary_kneti_hash (:obj:`str`): The hash of the secondary's KNETI key. Only valid if the hsm_type is "ncipher".
            secondary_esn (:obj:`str`, optional): The Electronic Serial Number (ESN) of the secondary module. Only valid 
                            if the hsm_type is "ncipher".
            use_rfs (`bool`, optional): A flag indicating if an RFS will be used. Default is true. Only valid if the 
                            hsm_type is "ncipher".
            rfs (:obj:`str`, optional): The IP address of the Remote File System (RFS). Required if the hsm_type is "ncipher" 
                            and use_rfs is "true".
            rfs_port (`int`, optional): The port of the Remote File System (RFS). Only valid if the hsm_type is "ncipher".
            rfs_auth (`bool`, optional): Specifies whether KNETI authentication is used when connecting to the RFS.
            update_zip (:obj:`str`, optional): A zip file containing local data to be uploaded from the device. Only 
                            valid if the hsm_type is "ncipher" and use_rfs is "false".
            safenet_pw (:obj:`str`, optional): The password of the SafeNet device admin account. Only valid if the HSM 
                            type is "safenet". 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the SSL database is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = SSL_CERTIFICATES

        data = DataObject()
        data.add_value_string("kdb_name", kdb_name)
        data.add_value_string("token_label", token_label)
        data.add_value_string("passcode", passcode)
        data.add_value_string("type", db_type)
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


    def import_database(self, kdb_file=None, sth_file=None):
        '''
        Import a SSL database.

        Args:
            kdb_file (:obj:`str`): Path to KDB file to import. This file should either be in KDB or PKCS#12 format.
            sth_file (:obj:`str`): Path to the corresponding stash file for the SSL database.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the SSL database is returned as JSON and can be accessed from
            the response.json attribute
        '''
        if not kdb_file or not sth_file:
            response = Response()
            setattr(response, 'status_code', 404)
            setattr(response, 'content', 'Both kdb_file and sth_file must be provided')
            setattr(response, 'success', False)
            return response
        files = {"kdb": open(kdb_file, 'rb'), "stash": open(sth_file, 'rb')}
        response = self.client.post_file(SSL_CERTIFICATES, files=files)
        response.success = response.status_code == 200

        return response
