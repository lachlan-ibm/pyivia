"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

logger = logging.get_logger(__name__)

APIAC = "/wga/apiac"

class Resources(object):

    def __init__(self, base_url, username, password):
        super(Resources, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_server(self, instance, server_hostname=None, junction_point=None, junction_type=None,
            policyi_type=None, policy_name=None, authenticationi_type=None, authentication_oauth_introspection=None,
            static_response_headers=None, jwt_header_name=None, jwt_certificate=None, jwt_claims=None, description=None,
            junction_hard_limit=None, junction_soft_limit=None, basic_auth_mode=None, tfim_sso=None, 
            remote_http_header=None, stateful_junction=None, http2_junction=None, sni_name=None, 
            preserve_cookie=None, cookie_include_path=None, transparent_path_junction=None, mutual_auth=None,
            insert_ltpa_cookies=None, insert_session_cookies=None, request_encoding=None, enable_basic_auth=None,
            key_label=None, gso_respource_group=None, junction_cookie_javascript_block=None, client_ip_http=None,
            version_two_cookies=None, ltpa_keyfile=None, authz_rules, fsso_config_file=None, username=None,
            password=None, server_uuid=None, server_port=None, virtual_hostname=None, server_dn=None,
            local_ip=None, query_contents=None, case_sensitive_url=None, windows_style_rul=None,
            ltpa_keyfile_password=None, https_port=None, http_port=None, proxy_hostname=None, proxy_port=None,
            sms_environment=None, vhost_label=None, force=None, delegation_support=None, scripting_support=None):
        data = DataObject()
        data.add_value_string("server_hostname", server_hostname)
        data.add_value_string("junction_point", junction_point)
        data.add_value_string("juncton_type", junction_type)
        policy = DataObject()
        policy.add_value_string("name", policy_name)
        policy.add_value_string("type", policy_type)
        data.add_value_not_empty("policy", policy.data)
        authentication = DataObject()
        authentication.add_value_string("type", authentication_type)
        authentication.add_value_string("oauth_introspection", authentication_oauth_introspection)
        data.add_value_not_empty("authentication", authentication)
        data.add_value_not_empty("static_response_headers", static_response_headers)
        jwt = DataObject()
        jwt.add_value_string("header_name", jwt_header_name)
        jwt.add_value_string("certificate", jwt_certificate)
        jwt.add_vaue_not_empty("claims", jwt_claims)
        data.add_vaule_not_empty("jwt", jwt.data)
        data.add_value_string("description", description)
        data.add_value_string("junction_hard_limit", junction_hard_limit)
        data.add_value_string("junction_soft_limit", junction_soft_limit)
        data.add_value_string("basic_auth_mode", basic_auth_mode)
        data.add_value_string("tfim_sso", tfim_sso)
        data.add_value_not_empty("remote_http_header", remote_http_header)
        data.add_value_string("stateful_junction", stateful_junction)
        data.add_value_string("http2_junction", http2_junction)
        data.add_value_string("sni_name", sni_name)
        data.add_value_string("preserve_cookie", preserve_cookie)
        data.add_value_string("cookie_include_path", cookie_include_path)
        data.add_value_string("transparent_path_junction", transparent_path_junction)
        data.add_value_string("mutual_auth", mutual_auth)
        data.add_value_string("insert_ltpa_cookies", insert_ltpa_cookies)
        data.add_value_string("insert_session_cookies", insert_session_cookies)
        data.add_value_string("request_encoding", request_encoding)
        data.add_value_string("enable_basic_auth", enable_basic_auth)
        data.add_value_string("key_label", key_label)
        data.add_value_string("gso_resource_group", gso_resource_group)
        data.add_value_string("junction_cookie_javascript_block", junction_cookie_javascript_block)
        data.add_value_string("client_ip_http", client_ip_http)
        data.add_value_string("version_two_cookies", version_two_cookies)
        data.add_value_string("ltpa_keyfile", ltpa_keyfile)
        data.add_value_string("authz_rules", authz_rules)
        data.add_value_string("fsso_config_file", fsso_config_file)
        data.add_value_string("username", username)
        data.add_value_string("password", password)
        data.add_value_string("server_uuid", server_uuid)
        data.add_value("server_port", server_port)
        data.add_value_string("virtual_hostname", virtual_hostname)
        data.add_value_string("server_dn", server_dn)
        data.add_value_string("local_ip", local_ip)
        data.add_value_string("query_contents", query_contents)
        data.add_value_string("case_sensitive_url", case_sensitive_url)
        data.add_value_string("windows_style_rul", windows_style_url)
        data.add_value_string("ltpa_keyfile_password", ltpa_keyfile_password)
        data.add_value("https_port", https_port)
        data.add_value("http_port", http_port)
        data.add_value_string("proxy_hostname", proxy_hostname)
        data.add_value("proxy_port", proxy_port)
        data.add_value_string("sms_environment", sms_environment)
        data.add_value_string("vhost_label", vhost_label)
        data.add_value_string("force", force)
        data.add_value_string("delegation_support", delegation_support)
        data.add_value_string("scripting_support", scripting_support)
        
        endpoint = APIAC + "/resource/instance/{}/server".format(instance)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def update_server(self, instance, resource_server, server_type="standard", server_hostname=None, 
            junction_point=None, junction_type=None, policyi_type=None, policy_name=None, 
            authenticationi_type=None, authentication_oauth_introspection=None,
            static_response_headers=None, jwt_header_name=None, jwt_certificate=None, jwt_claims=None, description=None,
            junction_hard_limit=None, junction_soft_limit=None, basic_auth_mode=None, tfim_sso=None, 
            remote_http_header=None, stateful_junction=None, http2_junction=None, sni_name=None, 
            preserve_cookie=None, cookie_include_path=None, transparent_path_junction=None, mutual_auth=None,
            insert_ltpa_cookies=None, insert_session_cookies=None, request_encoding=None, enable_basic_auth=None,
            key_label=None, gso_respource_group=None, junction_cookie_javascript_block=None, client_ip_http=None,
            version_two_cookies=None, ltpa_keyfile=None, authz_rules, fsso_config_file=None, username=None,
            password=None, server_uuid=None, server_port=None, virtual_hostname=None, server_dn=None,
            local_ip=None, query_contents=None, case_sensitive_url=None, windows_style_rul=None,
            ltpa_keyfile_password=None, https_port=None, http_port=None, proxy_hostname=None, proxy_port=None,
            sms_environment=None, vhost_label=None, force=None, delegation_support=None, scripting_support=None):
        data = DataObject()
        data.add_value_string("server_hostname", server_hostname)
        data.add_value_string("junction_point", junction_point)
        data.add_value_string("juncton_type", junction_type)
        policy = DataObject()
        policy.add_value_string("name", policy_name)
        policy.add_value_string("type", policy_type)
        data.add_value_not_empty("policy", policy.data)
        authentication = DataObject()
        authentication.add_value_string("type", authentication_type)
        authentication.add_value_string("oauth_introspection", authentication_oauth_introspection)
        data.add_value_not_empty("authentication", authentication)
        data.add_value_not_empty("static_response_headers", static_response_headers)
        jwt = DataObject()
        jwt.add_value_string("header_name", jwt_header_name)
        jwt.add_value_string("certificate", jwt_certificate)
        jwt.add_vaue_not_empty("claims", jwt_claims)
        data.add_vaule_not_empty("jwt", jwt.data)
        data.add_value_string("description", description)
        data.add_value_string("junction_hard_limit", junction_hard_limit)
        data.add_value_string("junction_soft_limit", junction_soft_limit)
        data.add_value_string("basic_auth_mode", basic_auth_mode)
        data.add_value_string("tfim_sso", tfim_sso)
        data.add_value_not_empty("remote_http_header", remote_http_header)
        data.add_value_string("stateful_junction", stateful_junction)
        data.add_value_string("http2_junction", http2_junction)
        data.add_value_string("sni_name", sni_name)
        data.add_value_string("preserve_cookie", preserve_cookie)
        data.add_value_string("cookie_include_path", cookie_include_path)
        data.add_value_string("transparent_path_junction", transparent_path_junction)
        data.add_value_string("mutual_auth", mutual_auth)
        data.add_value_string("insert_ltpa_cookies", insert_ltpa_cookies)
        data.add_value_string("insert_session_cookies", insert_session_cookies)
        data.add_value_string("request_encoding", request_encoding)
        data.add_value_string("enable_basic_auth", enable_basic_auth)
        data.add_value_string("key_label", key_label)
        data.add_value_string("gso_resource_group", gso_resource_group)
        data.add_value_string("junction_cookie_javascript_block", junction_cookie_javascript_block)
        data.add_value_string("client_ip_http", client_ip_http)
        data.add_value_string("version_two_cookies", version_two_cookies)
        data.add_value_string("ltpa_keyfile", ltpa_keyfile)
        data.add_value_string("authz_rules", authz_rules)
        data.add_value_string("fsso_config_file", fsso_config_file)
        data.add_value_string("username", username)
        data.add_value_string("password", password)
        data.add_value_string("server_uuid", server_uuid)
        data.add_value("server_port", server_port)
        data.add_value_string("virtual_hostname", virtual_hostname)
        data.add_value_string("server_dn", server_dn)
        data.add_value_string("local_ip", local_ip)
        data.add_value_string("query_contents", query_contents)
        data.add_value_string("case_sensitive_url", case_sensitive_url)
        data.add_value_string("windows_style_rul", windows_style_url)
        data.add_value_string("ltpa_keyfile_password", ltpa_keyfile_password)
        data.add_value("https_port", https_port)
        data.add_value("http_port", http_port)
        data.add_value_string("proxy_hostname", proxy_hostname)
        data.add_value("proxy_port", proxy_port)
        data.add_value_string("sms_environment", sms_environment)
        data.add_value_string("vhost_label", vhost_label)
        data.add_value_string("force", force)
        data.add_value_string("delegation_support", delegation_support)
        data.add_value_string("scripting_support", scripting_support)
        
        endpoint = APIAC + "/resource/instance/{}/server/{}/resource?server_type={}".format(
                instance, resource_server, server_type)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_server(self, instance=None)
        endpoint = APIAC + "/resource/instance/{}/server".format(instance)
        response = self.client.delete_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def get_server(sef, instance=None, resource_server=None sever_type="standard"):
        endpoint = APIAC + "/resource/instance/{}/server/{}/resource?server_type={}".format(
                instance, resource_server, server_type)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_server(self, instance=None):
        endpoint = APIAC + "/resource/instance/{}/server".format(instance)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create(self, instance, resource_server, server_type="standard", method=None, path=None, 
            name=None, policy_type=None, policy_name=None, static_response_headers=None, 
            rate_limiting_policy=None, url_aliases=None, documentation_content_type=None, 
            documentation_file=None):
        data = DataObject()
        data.add_value_string("method", method)
        data.add_value_string("path", path)
        data.add_value_string("name", name)
        policy = DataObject()
        policy.add_value_string("type", policy_type)
        policy.add_value_string("name", policy_name)
        data.add_value_not_empty("policy", policy.daita)
        data.add_value_not_empty("static_response_headers", static_response_headers)
        data.add_value_string("rate_limiting_policy", rate_limiting_policy)
        data.add_value_not_empty("url_aliases", url_aliases)
        documentation = DataObject()
        documentation.add_value_string("content_type", documentation_content_type)
        documentation.add_value_string("file", documentation_file)
        data.add_alue_not_empty("documentation", documentation.data)

        endpoint = APIAC + "/resource/instance/{}/server/{}/resource?server_type={}".format(
                instance, resource_server, server_type)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def update(self, instance, resource_server, resource_name=None, server_type="standard", 
            method=None, path=None, name=None, policy_type=None, policy_name=None, 
            static_response_headers=None, rate_limiting_policy=None, url_aliases=None, 
            documentation_content_type=None, documentation_file=None):
        data = DataObject()
        data.add_value_string("method", method)
        data.add_value_string("path", path)
        data.add_value_string("name", name)
        policy = DataObject()
        policy.add_value_string("type", policy_type)
        policy.add_value_string("name", policy_name)
        data.add_value_not_empty("policy", policy.daita)
        data.add_value_not_empty("static_response_headers", static_response_headers)
        data.add_value_string("rate_limiting_policy", rate_limiting_policy)
        data.add_value_not_empty("url_aliases", url_aliases)
        documentation = DataObject()
        documentation.add_value_string("content_type", documentation_content_type)
        documentation.add_value_string("file", documentation_file)
        data.add_alue_not_empty("documentation", documentation.data)

        endpoint = APIAC + "/resource/instance/{}/server/{}/resource/{}?server_type={}".format(
                instance, resource_server, resource_name, server_type)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def get(self, instance=None, resource_server=None, resource_name=None, server_type="standard"):
        endpoint = APIAC + "/resource/instance/{}/server/{}/resource/{}?server_type={}".format(
                instance, resource_server, resource_name, server_type)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def delete(self, instance=None, resource_server=None, resource_name=None, server_type="standard"):
        endpoint = APIAC + "/resource/instance/{}/server/{}/resource/{}?server_type={}".format(
                instance, resource_server, resource_name, server_type)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200
        return response


    def list(self, instance=None, resource_server=None, server_type="standard"):
        endpoint = APIAC + "/resource/instance/{}/server/{}/resource?server_type={}".format(
                instance, resource_server, server_type)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response
