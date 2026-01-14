""""
@copyright: IBM
"""

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


MANAGEMENT_CERTIFICATE = "/isam/management_ssl_certificate"

class ManagementCertificate(object):

    def __init__(self, base_url, username, password):
        super(ManagementCertificate, self).__init__()
        self._client = RESTClient(base_url, username, password)

    def get_certificate(self) -> Response:
        """Get the management certificate.

        Returns:
            :obj:`~requests.Response`: The management certificate.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the certificate attributes are returned as
            JSON and can be accessed from the response.json attribute
        """
        response = self._client.get_json(MANAGEMENT_CERTIFICATE)
        response.success = response.status_code == 200
        return response

    def update_certificate(self, certificate, password=None) -> Response:
        """Set the management certificate using a PKCS12 file and password.

        Note: The CN attribute of the X509 Certificate must match the hostname of the appliance.

        Args:
            certificate (str): Path to a PKCS12 file to import as the management key/certificate.
            password (str, optional): The password for the PKCS12 file.

        Returns:
            :obj:`~requests.Response`: The response from the server.

            Success can be checked by examining the response.success boolean attribute
        """

        with open(certificate, 'rb') as f:
            files = {"cert": f}
            data = DataObject()
            data.add_value_string("password", password)
            response = self._client.post_file(MANAGEMENT_CERTIFICATE, accept_type="text/html", data=data.data, files=files)

            response.success = response.status_code == 200
            return response