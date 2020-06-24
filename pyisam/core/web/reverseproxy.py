"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient
import urllib


REVERSEPROXY = "/wga/reverseproxy"
WGA_DEFAULTS = "/isam/wga_templates/defaults"
JUNCTIONS_QUERY = "junctions_id"
JMT_CONFIG = "/wga/jmt_config"

logger = logging.getLogger(__name__)


class ReverseProxy(object):

    def __init__(self, base_url, username, password):
        super(ReverseProxy, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_instance(
            self, inst_name=None, host=None, admin_id=None, admin_pwd=None,
            ssl_yn=None, key_file=None, cert_label=None, ssl_port=None,
            http_yn=None, http_port=None, https_yn=None, https_port=None,
            nw_interface_yn=None, ip_address=None, listening_port=None,
            domain=None):
        data = DataObject()
        data.add_value_string("inst_name", inst_name)
        data.add_value_string("host", host)
        data.add_value_string("listening_port", listening_port)
        data.add_value_string("domain", domain)
        data.add_value_string("admin_id", admin_id)
        data.add_value_string("admin_pwd", admin_pwd)
        data.add_value_string("ssl_yn", ssl_yn)
        if key_file != None and not key_file.endswith(".kdb"):
            key_file = key_file+".kdb"
        data.add_value_string("key_file", key_file)
        data.add_value_string("cert_label", cert_label)
        data.add_value_string("ssl_port", ssl_port)
        data.add_value_string("http_yn", http_yn)
        data.add_value_string("http_port", http_port)
        data.add_value_string("https_yn", https_yn)
        data.add_value_string("https_port", https_port)
        data.add_value_string("nw_interface_yn", nw_interface_yn)
        data.add_value_string("ip_address", ip_address)

        response = self.client.post_json(REVERSEPROXY, data.data)
        response.success = response.status_code == 200

        return response

    def delete_instance(self, id, admin_id, admin_pwd):
        data = DataObject()
        data.add_value_string("admin_id", admin_id)
        data.add_value_string("admin_pwd", admin_pwd)
        data.add_value_string("operation", "unconfigure")

        endpoint = "%s/%s" % (REVERSEPROXY, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def list_instances(self):
        response = self.client.get_json(REVERSEPROXY)
        response.success = response.status_code == 200

        return response

    def get_wga_defaults(self):
        response = self.client.get_json(WGA_DEFAULTS)
        response.success = response.status_code == 200

        return response

    def restart_instance(self, id):
        data = DataObject()
        data.add_value_string("operation", "restart")

        endpoint = "%s/%s" % (REVERSEPROXY, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def configure_mmfa(
            self, webseal_id, lmi_hostname=None, lmi_port=None,
            lmi_username=None, lmi_password=None, runtime_hostname=None,
            runtime_port=None, runtime_username=None, runtime_password=None,
            reuse_certs=None,reuse_acls=None, reuse_pops=None):
        lmi_data = DataObject()
        lmi_data.add_value_string("hostname", lmi_hostname)
        lmi_data.add_value_string("username", lmi_username)
        lmi_data.add_value_string("password", lmi_password)
        lmi_data.add_value("port", lmi_port)

        runtime_data = DataObject()
        runtime_data.add_value_string("hostname", runtime_hostname)
        runtime_data.add_value_string("username", runtime_username)
        runtime_data.add_value_string("password", runtime_password)
        runtime_data.add_value("port", runtime_port)

        data = DataObject()
        data.add_value("reuse_certs", reuse_certs)
        data.add_value("reuse_acls", reuse_acls)
        data.add_value("reuse_pops", reuse_pops)
        data.add_value_not_empty("lmi", lmi_data.data)
        data.add_value_not_empty("runtime", runtime_data.data)

        endpoint = "%s/%s/mmfa_config" % (REVERSEPROXY, webseal_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response

    def configure_fed(self,webseal_id,federation_id=None,reuse_certs=False,reuse_acls=False,
        runtime_hostname=None,runtime_port=None,runtime_username=None,runtime_password=None):


        data = DataObject()
        data.add_value_string("federation_id", federation_id)
        data.add_value("reuse_certs", reuse_certs)
        data.add_value("reuse_acls", reuse_acls)

        runtime_data = DataObject()
        runtime_data.add_value_string("hostname", runtime_hostname)
        runtime_data.add_value_string("port", runtime_port)
        runtime_data.add_value_string("username", runtime_username)
        runtime_data.add_value_string("password", runtime_password)

        data.add_value_not_empty("runtime", runtime_data.data)

        endpoint = "%s/%s/fed_config" % (REVERSEPROXY, webseal_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response

    def configure_aac(self,webseal_id,junction=None,reuse_certs=False,reuse_acls=False,
        runtime_hostname=None,runtime_port=None,runtime_username=None,runtime_password=None):

        data = DataObject()
        data.add_value("reuse_certs", reuse_certs)
        data.add_value("reuse_acls", reuse_acls)
        data.add_value("junction", junction)
        data.add_value_string("hostname", runtime_hostname)
        data.add_value_string("port", runtime_port)
        data.add_value_string("username", runtime_username)
        data.add_value_string("password", runtime_password)
        endpoint = "%s/%s/authsvc_config" % (REVERSEPROXY, webseal_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response

    def add_configuration_stanza(self, webseal_id, stanza_id):
        endpoint = ("%s/%s/configuration/stanza/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id))

        response = self.client.post_json(endpoint, data=data)
        response.success = response.status_code == 200

    def delete_configuration_stanza(self, webseal_id, stanza_id):
        endpoint = ("%s/%s/configuration/stanza/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id))

        response = self.client.delete_json(endpoint, data=data)
        response.success = response.status_code == 200

    def add_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value):
        data = {"entries": [[str(entry_name), str(value)]]}

        endpoint = ("%s/%s/configuration/stanza/%s/entry_name"
                    % (REVERSEPROXY, webseal_id, stanza_id))

        response = self.client.post_json(endpoint, data=data)
        response.success = response.status_code == 200

        return response

    def delete_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value=None):
        endpoint = ("%s/%s/configuration/stanza/%s/entry_name/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id, entry_name))
        if value:
            endpoint = "%s/value/%s" % (endpoint, value)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_configuration_stanza_entry(self, webseal_id, stanza_id, entry_name):
        endpoint = ("%s/%s/configuration/stanza/%s/entry_name/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id, entry_name))

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def update_configuration_stanza_entry(
            self, webseal_id, stanza_id, entry_name, value):
        data = DataObject()
        data.add_value_string("value", value)

        endpoint = ("%s/%s/configuration/stanza/%s/entry_name/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id, entry_name))

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def create_junction(
            self, webseal_id, server_hostname=None, junction_point=None,
            junction_type=None, description=None, basic_auth_mode=None, 
            tfim_sso=None, stateful_junction=None, preserve_cookie=None,
            cookie_include_path=None, transparent_path_junction=None,
            mutual_auth=None, insert_ltpa_cookies=None,
            insert_session_cookies=None, request_encoding=None,
            enable_basic_auth=None, key_label=None, gso_resource_group=None,
            junction_cookie_javascript_block=None, client_ip_http=None,
            version_two_cookies=None, ltpa_keyfile=None, authz_rules=None,
            fsso_config_file=None, username=None, password=None,
            server_uuid=None, virtual_hostname=None, server_dn=None,
            local_ip=None, query_contents=None, case_sensitive_url=None,
            windows_style_url=None, ltpa_keyfile_password=None,
            proxy_hostname=None, sms_environment=None, vhost_label=None,
            force=None, delegation_support=None, scripting_support=None,
            junction_hard_limit=None, junction_soft_limit=None,
            server_port=None, https_port=None, http_port=None, proxy_port=None,
            remote_http_header=None):
        data = DataObject()
        data.add_value_string("server_hostname", server_hostname)
        data.add_value_string("junction_point", junction_point)
        data.add_value_string("junction_type", junction_type)
        data.add_value_string("description", description)
        data.add_value_string("basic_auth_mode", basic_auth_mode)
        data.add_value_string("tfim_sso", tfim_sso)
        data.add_value_string("stateful_junction", stateful_junction)
        data.add_value_string("preserve_cookie", preserve_cookie)
        data.add_value_string("cookie_include_path", cookie_include_path)
        data.add_value_string(
            "transparent_path_junction", transparent_path_junction)
        data.add_value_string("mutual_auth", mutual_auth)
        data.add_value_string("insert_ltpa_cookies", insert_ltpa_cookies)
        data.add_value_string(
            "insert_session_cookies", insert_session_cookies)
        data.add_value_string("request_encoding", request_encoding)
        data.add_value_string("enable_basic_auth", enable_basic_auth)
        data.add_value_string("key_label", key_label)
        data.add_value_string("gso_resource_group", gso_resource_group)
        data.add_value_string(
            "junction_cookie_javascript_block",
            junction_cookie_javascript_block)
        data.add_value_string("client_ip_http", client_ip_http)
        data.add_value_string("version_two_cookies", version_two_cookies)
        data.add_value_string("ltpa_keyfile", ltpa_keyfile)
        data.add_value_string("authz_rules", authz_rules)
        data.add_value_string("fsso_config_file", fsso_config_file)
        data.add_value_string("username", username)
        data.add_value_string("password", password)
        data.add_value_string("server_uuid", server_uuid)
        data.add_value_string("virtual_hostname", virtual_hostname)
        data.add_value_string("server_dn", server_dn)
        data.add_value_string("local_ip", local_ip)
        data.add_value_string("query_contents", query_contents)
        data.add_value_string("case_sensitive_url", case_sensitive_url)
        data.add_value_string("windows_style_url", windows_style_url)
        data.add_value_string(
            "ltpa_keyfile_password", ltpa_keyfile_password)
        data.add_value_string("proxy_hostname", proxy_hostname)
        data.add_value_string("sms_environment", sms_environment)
        data.add_value_string("vhost_label", vhost_label)
        data.add_value_string("force", force)
        data.add_value_string("delegation_support", delegation_support)
        data.add_value_string("scripting_support", scripting_support)
        data.add_value("junction_hard_limit", junction_hard_limit)
        data.add_value("junction_soft_limit", junction_soft_limit)
        data.add_value("server_port", server_port)
        data.add_value("https_port", https_port)
        data.add_value("http_port", http_port)
        data.add_value("proxy_port", proxy_port)
        data.add_value("remote_http_header", remote_http_header)

        endpoint = "%s/%s/junctions" % (REVERSEPROXY, str(webseal_id))

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def delete_junction(self, webseal_id, junction_point):
        query = urllib.parse.urlencode({ JUNCTIONS_QUERY : junction_point})
        endpoint = "%s/%s/junctions?%s" % (REVERSEPROXY, webseal_id, query)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response

    def list_junctions(self, webseal_id):
        endpoint = "%s/%s/junctions" % (REVERSEPROXY, webseal_id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def import_management_root_files(self, webseal_id, file_path):
        response = Response()

        endpoint = ("%s/%s/management_root" % (REVERSEPROXY, webseal_id))

        try:
            with open(file_path, 'rb') as pages:
                files = {"file": pages}

                response = self.client.post_file(endpoint, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def update_management_root_file(self, webseal_id, page_id, contents):
        data = DataObject()
        data.add_value_string("type", "file")
        data.add_value_string("contents", contents)

        endpoint = ("%s/%s/management_root/%s"
                    % (REVERSEPROXY, webseal_id, page_id))

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    # Upload a single file (eg HTML or ico), rather than a zip.
    def import_management_root_file(self, webseal_id, page_id, file_path):
        response = Response()

        endpoint = ("%s/%s/management_root/%s" % (REVERSEPROXY, webseal_id, page_id))

        try:
            with open(file_path, 'rb') as contents:
                files = {"file": contents}

                response = self.client.post_file(endpoint, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def import_junction_mapping_file(self, file_path):

        response = Response()

        try:
            with open(file_path, 'rb') as contents:
                jmt_config_file = {"jmt_config_file": contents}

                response = self.client.post_file(JMT_CONFIG, files=jmt_config_file)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def update_junction_mapping_file(self, file_id, jmt_config_data):

        data = DataObject()
        data.add_value_string("id", file_id)
        data.add_value_string("jmt_config_data", jmt_config_data)

        endpoint = ("%s/%s"
                    % (JMT_CONFIG, file_id))

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

class ReverseProxy9040(ReverseProxy):

    def __init__(self, base_url, username, password):
        super(ReverseProxy, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def configure_api_protection(
            self, webseal_id, hostname=None, port=None,
            username=None, password=None, reuse_certs=None,reuse_acls=None, api=None,
            browser=None, junction=None):
        data = DataObject()
        data.add_value_string("hostname", hostname)
        data.add_value_string("username", username)
        data.add_value_string("password", password)
        data.add_value("port", port)
        data.add_value("junction", junction if junction != None else "/mga")

        data.add_value_boolean("reuse_certs", reuse_certs)
        data.add_value_boolean("reuse_acls", reuse_acls)
        data.add_value_boolean("api", api)
        data.add_value_boolean("browser", browser)

        endpoint = "%s/%s/oauth_config" % (REVERSEPROXY, webseal_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204
        return response

    def configure_mmfa(
            self, webseal_id, lmi_hostname=None, lmi_port=None,
            lmi_username=None, lmi_password=None, runtime_hostname=None,
            runtime_port=None, runtime_username=None, runtime_password=None,
            reuse_certs=None,reuse_acls=None, reuse_pops=None, channel=None):
        lmi_data = DataObject()
        lmi_data.add_value_string("hostname", lmi_hostname)
        lmi_data.add_value_string("username", lmi_username)
        lmi_data.add_value_string("password", lmi_password)
        lmi_data.add_value("port", lmi_port)

        runtime_data = DataObject()
        runtime_data.add_value_string("hostname", runtime_hostname)
        runtime_data.add_value_string("username", runtime_username)
        runtime_data.add_value_string("password", runtime_password)
        runtime_data.add_value("port", runtime_port)

        data = DataObject()
        data.add_value('channel', channel)
        data.add_value("reuse_certs", reuse_certs)
        data.add_value("reuse_acls", reuse_acls)
        data.add_value("reuse_pops", reuse_pops)
        data.add_value_not_empty("lmi", lmi_data.data)
        data.add_value_not_empty("runtime", runtime_data.data)

        endpoint = "%s/%s/mmfa_config" % (REVERSEPROXY, webseal_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


class ReverseProxy10020(ReverseProxy9040):

    def __init__(self, base_url, username, password):
        super(ReverseProxy9040, self).__init__(base_url, username, password)
        self.client = RESTClient(base_url, username, password)


    def configure_verify_gateway(self, webseal_id, mmfa=None, junction=None):
        data = DataObject()
        data.add_value_boolean("mmfa", mmfa)
        data.add_value_string("junction", junction);

        endpoint = "{}/{}/verify_gateway_config".format(REVERSEPROXY, webseal_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response
