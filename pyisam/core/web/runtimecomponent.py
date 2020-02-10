"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


EMBEDDED_LDAP_PASSWORD = "/isam/embedded_ldap/change_pwd/v1"
RUNTIME_COMPONENT = "/isam/runtime_components"
UNCONFIGURE_RUNTIME_COMPONENT = RUNTIME_COMPONENT + "/RTE"

logger = logging.getLogger(__name__)


class RuntimeComponent(object):

    def __init__(self, base_url, username, password):
        super(RuntimeComponent, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def configure(
            self, ps_mode=None, user_registry=None, admin_password=None,
            ldap_password=None, admin_cert_lifetime=None, ssl_compliance=None,
            ldap_host=None, ldap_port=None, isam_domain=None, ldap_dn=None,
            ldap_suffix=None, ldap_ssl_db=None, ldap_ssl_label=None,
            isam_host=None, isam_port=None, clean_ldap=None):
        data = DataObject()
        data.add_value_string("ps_mode", ps_mode)
        data.add_value_string("user_registry", user_registry)
        data.add_value_string("admin_cert_lifetime", admin_cert_lifetime)
        data.add_value_string("ssl_compliance", ssl_compliance)
        data.add_value_string("admin_pwd", admin_password)
        data.add_value_string("ldap_pwd", ldap_password)
        data.add_value_string("ldap_host", ldap_host)
        data.add_value_string("domain", isam_domain)
        data.add_value_string("ldap_dn", ldap_dn)
        data.add_value_string("ldap_suffix", ldap_suffix)
        data.add_value_string("clean_ldap", clean_ldap)
        if ldap_ssl_db is not None:
            data.add_value_string("ldap_ssl_db", ldap_ssl_db if ldap_ssl_db.endswith(".kdb") else ldap_ssl_db+".kdb")
            data.add_value_string("usessl", "on")
        data.add_value_string("ldap_ssl_label", ldap_ssl_label)
        data.add_value_string("isam_host", isam_host)
        data.add_value("ldap_port", ldap_port)
        data.add_value("isam_port", isam_port)

        response = self.client.post_json(RUNTIME_COMPONENT, data.data)

        response.success = response.status_code == 200

        return response

    def get_status(self):
        """
        Query the ISAM API to get the runtime components list.
        :return: PyISAM Response
        """
        response = self.client.get_json(RUNTIME_COMPONENT)
        response.success = response.status_code == 200

        return response

    def update_embedded_ldap_password(self, password):
        data = DataObject()
        data.add_value_string("password", password)

        response = self.client.post_json(EMBEDDED_LDAP_PASSWORD, data.data)
        response.success = response.status_code == 200

        return response


    def unconfigure(self, operation="unconfigure", ldap_dn=None, ldap_pwd=None, clean=False, force=False):
        data = DataObject()
        data.add_value_string("operation", operation)
        data.add_value_string("ldap_dn", ldap_dn)
        data.add_value_string("ldap_pwd", ldap_pwd)
        data.add_value_string("clean", clean)
        data.add_value_string("force", force)

        response = self.client.post_json(UNCONFIGURE_RUNTIME_COMPONENT, data.data)

        response.success = response.status_code == 200

        return response
