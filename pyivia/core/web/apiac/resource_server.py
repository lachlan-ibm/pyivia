"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

APIAC = "/wga/apiac"

class ResourceServer(object):

    def __init__(self, base_url, username, password):
        super(ResourceServer, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_server(self, instance, server_hostname=None, junction_point=None, junction_type=None,
            policy_type=None, policy_name=None, authentication_type=None, oauth_introspection_transport=None,
            oauth_introspection_proxy=None, oauth_introspection_auth_method=None, oauth_introspection_endpoint=None, 
            oauth_introspection_client_id=None, oauth_introspection_client_secret=None, 
            oauth_introspection_client_id_hdr=None, oauth_introspection_token_type_hint=None, 
            oauth_introspection_mapped_id=None, oauth_introspection_external_user=None, 
            oauth_introspection_response_attributes=None, static_response_headers=None, jwt_header_name=None, 
            jwt_certificate=None, jwt_claims=None, description=None, junction_hard_limit=None, 
            junction_soft_limit=None, basic_auth_mode=None, tfim_sso=None, remote_http_header=None, 
            stateful_junction=None, http2_junction=None, http2_proxy=None, sni_name=None, preserve_cookie=None, 
            cookie_include_path=None, transparent_path_junction=None, mutual_auth=None, insert_ltpa_cookies=None, 
            insert_session_cookies=None, request_encoding=None, enable_basic_auth=None, key_label=None, 
            gso_resource_group=None, junction_cookie_javascript_block=None, client_ip_http=None, 
            version_two_cookies=None, ltpa_keyfile=None, authz_rules=None, fsso_config_file=None, username=None, 
            password=None, server_uuid=None, server_port=None, virtual_hostname=None, server_dn=None, server_cn=None, 
            local_ip=None, query_contents=None, case_sensitive_url=None, windows_style_url=None, 
            ltpa_keyfile_password=None, https_port=None, http_port=None, proxy_hostname=None, proxy_port=None, 
            sms_environment=None, vhost_label=None, force=None, delegation_support=None, scripting_support=None):
        '''
        Create a new API Access Control resource server.

        Args:
            instance (:obj:`str`): Name of WebSEAL Reverse Proxy instance being configured.
            server_hostname (:obj:`str`): The DNS host name or IP address of the target back-end server.
            junction_point (:obj:`str`): Name of the location in the Reverse Proxy namespace where the root of the 
                                        back-end application server namespace is mounted.
            junction_type (:obj:`str`): Type of junction.
            policy_type (:obj:`str`): The type of the policy.
            policy_name (:obj:`str`): The name of the custom policy if the type is custom.
            authentication_type (:obj:`str`): The type of Oauth authentication. The valid values are default or oauth.
            oauth_introspection_transport (:obj:`str`): The transport type.
            oauth_introspection_proxy (:obj:`str`): The proxy, if any, used to reach the introspection endpoint.
            oauth_introspection_auth_method (:obj:`str`): The method for passing the authentication data to the 
                                                          introspection endpoint.
            oauth_introspection_endpoint (:obj:`str`): This is the introspection endpoint which will be called to handle 
                                                       the token introspection.
            oauth_introspection_client_id (:obj:`str`): The client identifier which is used for OAuth introspection 
                                                        authentication.
            oauth_introspection_client_secret (:obj:`str`): The client secret which is used for OAuth introspection 
                                                            authentication.
            oauth_introspection_client_id_hdr (:obj:`str`): The name of the HTTP header which contains the client 
                                                            identifier which is used to authenticate to the introspection 
                                                            endpoint.
            oauth_introspection_token_type_hint (:obj:`str`): A hint about the type of the token submitted for introspection.
            oauth_introspection_mapped_id (:obj:`str`): A formatted string which is used to construct the Verify Identity Access 
                                                        principal name from elements of the introspection response. 
            oauth_introspection_external_user (bool): A boolean which is used to indicate whether the mapped identity 
                                                      should correspond to a known Verify Identity Access identity or not.
            oauth_introspection_response_attributes (:obj:`list` of :obj:`dict`): A list of rules indicating which parts 
                                                                                  of the json response should be added to 
                                                                                  the credential. eg::

                                                                                            {
                                                                                                 "pos":1,
                                                                                                 "action":"put",
                                                                                                 "attribute":"givenName"
                                                                                            }

            static_response_headers (:obj:`list` of :obj:`dict`): A list of header names and values that should be 
                                                                  added to the HTTP response. eg:: 

                                                                                            {
                                                                                                "name":"HeaderName",
                                                                                                "value":"HeaderValue"
                                                                                            }

            jwt_header_name (:obj:`str`): The name of the HTTP header that will contain the JWT.
            jwt_certificate (:obj:`str`): The label of the personal certificate that will sign the JWT.
            jwt_claims (:obj:`list` of :obj:`dict`): The list of claims to add to the JWT.
            description (:obj:`str`, optional): An optional description for this junction.
            junction_hard_limit (:obj:`str`): Defines the hard limit percentage for consumption of worker threads. 
                                              Valid value is an integer from "0" to "100".
            junction_soft_limit (:obj:`str`): Defines the soft limit percentage for consumption of worker threads.
            basic_auth_mode (:obj:`str`): Defines how the Reverse Proxy server passes client identity information in 
                                          HTTP basic authentication (BA) headers to the back-end server. 
            tfim_sso (:obj:`str`): Enables IBM Security Federated Identity Manager single sign-on.
            remote_http_header (:obj:`str`): Controls the insertion of Verify Identity Access specific client identity 
                                             information in HTTP headers across the junction.
            stateful_junction (:obj:`str`): Specifies whether the junction supports stateful applications.
            http2_junction (:obj:`str`): Specifies whether the junction supports the HTTP/2 protocol.
            http2_proxy (:obj:`str`): Specifies whether the junction proxy support the HTTP/2 protocol.
            sni_name (:obj:`str`): The server name indicator (SNI) to send to TLS junction servers.
            preserve_cookie (:obj:`str`): Specifies whether modifications of the names of non-domain cookies are to be made.
            cookie_include_path (:obj:`str`): Specifies whether script generated server-relative URLs are included in 
                                              cookies for junction identification.
            transparent_path_junction (:obj:`str`): Specifies whether a transparent path junction is created.
            mutual_auth (:obj:`str`): Specifies whether to enforce mutual authentication between a front-end Reverse 
                                      Proxy server and a back-end Reverse Proxy server over SSL.
            insert_ltpa_cookies (:obj:`str`): Controls whether LTPA cookies are passed to the junctioned Web server.
            insert_session_cookies (:obj:`str`): Controls whether to send the session cookie to the junctioned Web server.
            request_encoding (:obj:`str`): Specifies the encoding to use when the system generates HTTP headers for junctions.
            enable_basic_auth (:obj:`str`): Specifies whether to use BA header information to authenticate to back-end server.
            key_label (:obj:`str`): The key label for the client-side certificate that is used when the system 
                                    authenticates to the junctioned Web server.
            gso_resource_group (:obj:`str`): The name of the GSO resource or resource group.
            junction_cookie_javascript_block (:obj:`str`): Controls the junction cookie JavaScript block.
            client_ip_http (:obj:`str`): Specifies whether to insert the IP address of the incoming request into an 
                                         HTTP header for transmission to the junctioned Web server.
            version_two_cookies (:obj:`str`): Specifies whether LTPA version 2 cookies (LtpaToken2) are used.
            ltpa_keyfile (:obj:`str`): Location of the key file that is used to encrypt the LTPA cookie data.
            authz_rules (:obj:`str`): Specifies whether to allow denied requests and failure reason information from 
                                      authorization rules to be sent in the Boolean Rule header (AM_AZN_FAILURE) across 
                                      the junction.
            fsso_config_file (:obj:`str`): The name of the configuration file that is used for forms based single sign-on.
            username (:obj:`str`): The Reverse Proxy user name.
            password (:obj:`str`): The Reverse Proxy password.
            server_uuid (:obj:`str`): Specifies the UUID that will be used to identify the junctioned Web server.
            server_port (int): TCP port of the back-end third-party server.
            virtual_hostname (:obj:`str`): Virtual host name that is used for the junctioned Web server.
            server_dn (:obj:`str`): Specifies the distinguished name of the junctioned Web server.
            server_cn (:obj:`str`): Specifies the common name, or subject alternative name, of the junctioned Web server.
            local_ip (:obj:`str`): Specifies the local IP address that the Reverse Proxy uses when the system 
                                   communicates with the target back-end server. 
            query_contents (:obj:`str`): Provides the Reverse Proxy with the correct name of the query_contents program 
                                         file and where to find the file.
            case_sensitive_url (:obj:`str`): Specifies whether the Reverse Proxy server treats URLs as case sensitive.
            windows_style_url (:obj:`str`): Specifies whether Windows style URLs are supported.
            ltpa_keyfile_password (:obj:`str`): Password for the key file that is used to encrypt LTPA cookie data.
            https_port (int): HTTPS port of the back-end third-party server.
            http_port (int): HTTP port of the back-end third-party server.
            proxy_hostname (:obj:`str`): The DNS host name or IP address of the proxy server.
            proxy_port (int): The TCP port of the proxy server.
            sms_environment (:obj:`str`): Only applicable for virtual junctions. Specifies the replica set that sessions 
                                          on the virtual junction are managed under.
            vhost_label (:obj:`str`): Only applicable for virtual junctions. Causes a second virtual junction to share 
                                      the protected object space with the initial virtual junction.
            force (:obj:`str`): Specifies whether to overwrite an existing junction of the same name.
            delegation_support (:obj:`str`): Indicates single sign-on from a front-end Reverse Proxy server to a 
                                             back-end Reverse Proxy server.
            scripting_support (:obj:`str`): Supplies junction identification in a cookie to handle script-generated 
                                            server-relative URLs.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("server_hostname", server_hostname)
        data.add_value_string("junction_point", junction_point)
        data.add_value_string("junction_type", junction_type)
        policy = DataObject()
        policy.add_value_string("name", policy_name)
        policy.add_value_string("type", policy_type)
        data.add_value_not_empty("policy", policy.data)
        authentication = DataObject()
        authentication.add_value_string("type", authentication_type)
        oauth_introspection = DataObject()
        oauth_introspection.add_value_string("transport", oauth_introspection_transport)
        oauth_introspection.add_value_string("endpoint", oauth_introspection_endpoint)
        oauth_introspection.add_value_string("proxy", oauth_introspection_proxy)
        oauth_introspection.add_value_string("auth_method", oauth_introspection_auth_method)
        oauth_introspection.add_value_string("client_id", oauth_introspection_client_id)
        oauth_introspection.add_value_string("client_secret", oauth_introspection_client_secret)
        oauth_introspection.add_value_string("client_id_hdr", oauth_introspection_client_id_hdr)
        oauth_introspection.add_value_string("token_type_hint", oauth_introspection_token_type_hint)
        oauth_introspection.add_value_string("mapped_id", oauth_introspection_mapped_id)
        oauth_introspection.add_value_string("external_user", oauth_introspection_external_user)
        oauth_introspection.add_value_not_empty("response_attributes", oauth_introspection_response_attributes)
        authentication.add_value_string("oauth_introspection", oauth_introspection.data)
        data.add_value_not_empty("authentication", authentication.data)
        data.add_value_not_empty("static_response_headers", static_response_headers)
        jwt = DataObject()
        jwt.add_value_string("header_name", jwt_header_name)
        jwt.add_value_string("certificate", jwt_certificate)
        jwt.add_value_not_empty("claims", jwt_claims)
        data.add_value_not_empty("jwt", jwt.data)
        data.add_value_string("description", description)
        data.add_value_string("junction_hard_limit", junction_hard_limit)
        data.add_value_string("junction_soft_limit", junction_soft_limit)
        data.add_value_string("basic_auth_mode", basic_auth_mode)
        data.add_value_string("tfim_sso", tfim_sso)
        data.add_value_not_empty("remote_http_header", remote_http_header)
        data.add_value_string("stateful_junction", stateful_junction)
        data.add_value_string("http2_junction", http2_junction)
        data.add_value_string("http2_proxy", http2_proxy)
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
        data.add_value_string("server_cn", server_cn)
        data.add_value_string("local_ip", local_ip)
        data.add_value_string("query_contents", query_contents)
        data.add_value_string("case_sensitive_url", case_sensitive_url)
        data.add_value_string("windows_style_url", windows_style_url)
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
            junction_point=None, junction_type=None, policy_type=None, policy_name=None, 
            authentication_type=None, authentication_oauth_introspection=None,
            static_response_headers=None, jwt_header_name=None, jwt_certificate=None, jwt_claims=None, description=None,
            junction_hard_limit=None, junction_soft_limit=None, basic_auth_mode=None, tfim_sso=None, 
            remote_http_header=None, stateful_junction=None, http2_junction=None, sni_name=None, 
            preserve_cookie=None, cookie_include_path=None, transparent_path_junction=None, mutual_auth=None,
            insert_ltpa_cookies=None, insert_session_cookies=None, request_encoding=None, enable_basic_auth=None,
            key_label=None, gso_resource_group=None, junction_cookie_javascript_block=None, client_ip_http=None,
            version_two_cookies=None, ltpa_keyfile=None, authz_rules=None, fsso_config_file=None, username=None,
            password=None, server_uuid=None, server_port=None, virtual_hostname=None, server_dn=None, server_cn=None,
            local_ip=None, query_contents=None, case_sensitive_url=None, windows_style_url=None,
            ltpa_keyfile_password=None, https_port=None, http_port=None, proxy_hostname=None, proxy_port=None,
            sms_environment=None, vhost_label=None, force=None, delegation_support=None, scripting_support=None):
        '''
        Update an existing API Access Control resource server.

        Args:
            instance (:obj:`str`): Name of WebSEAL Reverse Proxy instance being configured.
            resource_server (:obj:`str`): The name of the API Access Control Resource Server.
            server_hostname (:obj:`str`): The DNS host name or IP address of the target back-end server.
            junction_point (:obj:`str`): Name of the location in the Reverse Proxy namespace where the root of the 
                        back-end application server namespace is mounted.
            junction_type (:obj:`str`): Type of junction.
            policy_type (:obj:`str`): The type of the policy.
            policy_name (:obj:`str`): The name of the custom policy if the type is custom.
            authentication_type (:obj:`str`): The type of Oauth authentication. The valid values are default or oauth.
            oauth_introspection_transport (:obj:`str`): The transport type.
            oauth_introspection_proxy (:obj:`str`): The proxy, if any, used to reach the introspection endpoint.
            oauth_introspection_auth_method (:obj:`str`): The method for passing the authentication data to the 
                                                        introspection endpoint.
            oauth_introspection_endpoint (:obj:`str`): This is the introspection endpoint which will be called to handle 
                                                        the token introspection.
            oauth_introspection_client_id (:obj:`str`): The client identifier which is used for OAuth introspection 
                                                        authentication.
            oauth_introspection_client_secret (:obj:`str`): The client secret which is used for OAuth introspection 
                                                            authentication.
            oauth_introspection_client_id_hdr (:obj:`str`): The name of the HTTP header which contains the client 
                                                            identifier which is used to authenticate to the introspection 
                                                            endpoint.
            oauth_introspection_token_type_hint (:obj:`str`): A hint about the type of the token submitted for introspection.
            oauth_introspection_mapped_id (:obj:`str`): A formatted string which is used to construct the Verify Identity Access 
                                                        principal name from elements of the introspection response. 
            oauth_introspection_external_user (bool): A boolean which is used to indicate whether the mapped identity 
                                                    should correspond to a known Verify Identity Access identity or not.
            oauth_introspection_response_attributes (:obj:`list` of :obj:`dict`): A list of rules indicating which parts 
                                                                        of the json response should be added to the credential. 
                                                                        eg::

                                                                            {"pos":1,"action":"put","attribute":"givenName"}

            static_response_headers (:obj:`list` of :obj:`dict`): A list of header names and values that should be 
                                                                added to the HTTP response. eg::

                                                                                    {"name":"HeaderName","value":"HeaderValue"}

            jwt_header_name (:obj:`str`): The name of the HTTP header that will contain the JWT.
            jwt_certificate (:obj:`str`): The label of the personal certificate that will sign the JWT.
            jwt_claims (:obj:`list` of :obj:`dict`): The list of claims to add to the JWT.
            description (:obj:`str`, optional): An optional description for this junction.
            junction_hard_limit (:obj:`str`): Defines the hard limit percentage for consumption of worker threads. 
                                              Valid value is an integer from "0" to "100".
            junction_soft_limit (:obj:`str`): Defines the soft limit percentage for consumption of worker threads.
            basic_auth_mode (:obj:`str`): Defines how the Reverse Proxy server passes client identity information in 
                                          HTTP basic authentication (BA) headers to the back-end server. 
            tfim_sso (:obj:`str`): Enables IBM Security Federated Identity Manager single sign-on.
            remote_http_header (:obj:`str`): Controls the insertion of Verify Identity Access specific client identity 
                                              information in HTTP headers across the junction.
            stateful_junction (:obj:`str`): Specifies whether the junction supports stateful applications.
            http2_junction (:obj:`str`): Specifies whether the junction supports the HTTP/2 protocol.
            http2_proxy (:obj:`str`): Specifies whether the junction proxy support the HTTP/2 protocol.
            sni_name (:obj:`str`): The server name indicator (SNI) to send to TLS junction servers.
            preserve_cookie (:obj:`str`): Specifies whether modifications of the names of non-domain cookies are to be made.
            cookie_include_path (:obj:`str`): Specifies whether script generated server-relative URLs are included in 
                                              cookies for junction identification.
            transparent_path_junction (:obj:`str`): Specifies whether a transparent path junction is created.
            mutual_auth (:obj:`str`): Specifies whether to enforce mutual authentication between a front-end Reverse 
                                      Proxy server and a back-end Reverse Proxy server over SSL.
            insert_ltpa_cookies (:obj:`str`): Controls whether LTPA cookies are passed to the junctioned Web server.
            insert_session_cookies (:obj:`str`): Controls whether to send the session cookie to the junctioned Web server.
            request_encoding (:obj:`str`): Specifies the encoding to use when the system generates HTTP headers for junctions.
            enable_basic_auth (:obj:`str`): Specifies whether to use BA header information to authenticate to back-end server.
            key_label (:obj:`str`): The key label for the client-side certificate that is used when the system 
                                    authenticates to the junctioned Web server.
            gso_resource_group (:obj:`str`): The name of the GSO resource or resource group.
            junction_cookie_javascript_block (:obj:`str`): Controls the junction cookie JavaScript block.
            client_ip_http (:obj:`str`): Specifies whether to insert the IP address of the incoming request into an 
                                         HTTP header for transmission to the junctioned Web server.
            version_two_cookies (:obj:`str`): Specifies whether LTPA version 2 cookies (LtpaToken2) are used.
            ltpa_keyfile (:obj:`str`): Location of the key file that is used to encrypt the LTPA cookie data.
            authz_rules (:obj:`str`): Specifies whether to allow denied requests and failure reason information from 
                                      authorization rules to be sent in the Boolean Rule header (AM_AZN_FAILURE) across the junction.
            fsso_config_file (:obj:`str`): The name of the configuration file that is used for forms based single sign-on.
            username (:obj:`str`): The Reverse Proxy user name.
            password (:obj:`str`): The Reverse Proxy password.
            server_uuid (:obj:`str`): Specifies the UUID that will be used to identify the junctioned Web server.
            server_port (int): TCP port of the back-end third-party server.
            virtual_hostname (:obj:`str`): Virtual host name that is used for the junctioned Web server.
            server_dn (:obj:`str`): Specifies the distinguished name of the junctioned Web server.
            server_cn (:obj:`str`): Specifies the common name, or subject alternative name, of the junctioned Web server.
            local_ip (:obj:`str`): Specifies the local IP address that the Reverse Proxy uses when the system 
                                   communicates with the target back-end server. 
            query_contents (:obj:`str`): Provides the Reverse Proxy with the correct name of the query_contents program 
                                         file and where to find the file.
            case_sensitive_url (:obj:`str`): Specifies whether the Reverse Proxy server treats URLs as case sensitive.
            windows_style_url (:obj:`str`): Specifies whether Windows style URLs are supported.
            ltpa_keyfile_password (:obj:`str`): Password for the key file that is used to encrypt LTPA cookie data.
            https_port (int): HTTPS port of the back-end third-party server.
            http_port (int): HTTP port of the back-end third-party server.
            proxy_hostname (:obj:`str`): The DNS host name or IP address of the proxy server.
            proxy_port (int): The TCP port of the proxy server.
            sms_environment (:obj:`str`): Only applicable for virtual junctions. Specifies the replica set that sessions 
                                          on the virtual junction are managed under.
            vhost_label (:obj:`str`): Only applicable for virtual junctions. Causes a second virtual junction to share 
                                      the protected object space with the initial virtual junction.
            force (:obj:`str`): Specifies whether to overwrite an existing junction of the same name.
            delegation_support (:obj:`str`): Indicates single sign-on from a front-end Reverse Proxy server to a 
                                             back-end Reverse Proxy server.
            scripting_support (:obj:`str`): Supplies junction identification in a cookie to handle script-generated 
                                            server-relative URLs.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        data = DataObject()
        data.add_value_string("server_hostname", server_hostname)
        data.add_value_string("junction_point", junction_point)
        data.add_value_string("junction_type", junction_type)
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
        jwt.add_value_not_empty("claims", jwt_claims)
        data.add_value_not_empty("jwt", jwt.data)
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


    def delete_server(self, instance=None, resource_server=None):
        '''
        Delete an existing API Access Control Resource Server.

        Args:
            instance (:obj:`str`): The name of the Reverse Proxy Instance.
            resource_server (:obj:`str`): The name of the API Access Control Resource Server.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        endpoint = APIAC + "/resource/instance/{}/server/{}".format(instance, resource_server)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_server(self, instance=None, resource_server=None, server_type="standard"):
        '''
        Get an existing API Access Control Resource Server.

        Args:
            instance (:obj:`str`): The name of the Reverse Proxy Instance.
            resource_server (:obj:`str`): The name of the API Access Control Resource Server.
            server_type (:obj:`str`): The type of the specified resource server junction. Valid 
                                    values are ``vhj`` for a virtual junction or ``standard`` for 
                                    a standard junction. Defaults to ``standard`` if not specified.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the resource server is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = APIAC + "/resource/instance/{}/server/{}/resource?server_type={}".format(
                instance, resource_server, server_type)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_server(self, instance=None):
        '''
        Retrieve a list of all API Access Control Resource Servers

        Args:
            instance (:obj:`str`): The name of the Reverse Proxy Instance.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the resource servers are returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = APIAC + "/resource/instance/{}/server".format(instance)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create_resource(self, instance, resource_server, server_type='standard', method=None, path=None, 
            name=None, policy_type=None, policy_name=None, static_response_headers=None, 
            rate_limiting_policy=None, url_aliases=None, documentation_content_type=None, 
            documentation_file=None):
        '''
        Create a new API Access Control Resource.

        Args:
            instance (:obj:`str`): The name of the Reverse Proxy Instance.
            resource_server (:obj:`str`): The name of the API Access Control Resource Server.
            server_type (:obj:`str`): The type of the specified resource server junction. Valid 
                                    values are ``vhj`` for a virtual junction or ``standard`` for 
                                    a standard junction. Defaults to ``standard`` if not specified.
            method (:obj:`str`): The HTTP action for this resource.
            path (:obj:`str`): The URI path for this resource. This is a full server relative path including the 
                            junction point.
            name (:obj:`str`): A description for this resource.
            policy_type (:obj:`str`): The type of Policy. The valid values are ``unauthenticated``, ``anyauthenticated``, 
                                    ``none``, ``default`` or ``custom``.
            policy_name (:obj:`str`): The name of the custom policy if the type is ``custom``.
            static_response_headers (:obj:`list` of :obj:`dict`): A list of header names and values that should 
                                                                be added to the HTTP response. The expected format of
                                                                the headers list is::

                                                                                    {"name":"CORS-Header","value":"static_value"}

            rate_limiting_policy (:obj:`str`): The name of the rate limiting policy that has been set for this resource.
            url_aliases (:obj:`list` of :obj:`str`): A list of aliases that all map to the path of this resource.
            documentation_content_type (:obj:`str`): The value of the accept header that will trigger a documentation response.
            documentation_file (:obj:`str`): The name and path of the documentation file to respond with, relative to 
                                            the junction root. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("method", method)
        data.add_value_string("path", path)
        data.add_value_string("name", name)
        policy = DataObject()
        policy.add_value_string("type", policy_type)
        policy.add_value_string("name", policy_name)
        data.add_value_not_empty("policy", policy.data)
        data.add_value_not_empty("static_response_headers", static_response_headers)
        data.add_value_string("rate_limiting_policy", rate_limiting_policy)
        data.add_value_not_empty("url_aliases", url_aliases)
        documentation = DataObject()
        documentation.add_value_string("content_type", documentation_content_type)
        documentation.add_value_string("file", documentation_file)
        data.add_value_not_empty("documentation", documentation.data)
        if not server_type:
            server_type = "standard"
        endpoint = APIAC + "/resource/instance/{}/server/{}/resource?server_type={}".format(
                instance, resource_server, server_type)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def update_resource(self, instance, resource_server, resource_name=None, server_type="standard", 
            method=None, path=None, name=None, policy_type=None, policy_name=None, 
            static_response_headers=None, rate_limiting_policy=None, url_aliases=None, 
            documentation_content_type=None, documentation_file=None):
        '''
        Update an API Access Control Resource.

        Args:
            instance (:obj:`str`): The name of the Reverse Proxy Instance.
            resource_server (:obj:`str`): The name of the API Access Control Resource Server.
            server_type (:obj:`str`): The type of the specified resource server junction. Valid 
                                    values are ``vhj`` for a virtual junction or ``standard`` for 
                                    a standard junction. Defaults to ``standard`` if not specified.
            resource_name (:obj:`str`): The name of the API Access Control Resource.
            method (:obj:`str`): The HTTP action for this resource.
            path (:obj:`str`): The URI path for this resource. This is a full server relative path including the 
                            junction point.
            name (:obj:`str`): A description for this resource.
            policy_type (:obj:`str`): The type of Policy. The valid values are ``unauthenticated``, ``anyauthenticated``, 
                                    ``none``, ``default`` or ``custom``.
            policy_name (:obj:`str`): The name of the custom policy if the type is ``custom``.
            static_response_headers (:obj:`list` of :obj:`dict`): A list of header names and values that should 
                                                                be added to the HTTP response. The expected format of
                                                                the headers list is::

                                                                                    {"name":"CORS-Header","value":"static_value"}

            rate_limiting_policy (:obj:`str`): The name of the rate limiting policy that has been set for this resource.
            url_aliases (:obj:`list` of :obj:`str`): A list of aliases that all map to the path of this resource.
            documentation_content_type (:obj:`str`): The value of the accept header that will trigger a documentation response.
            documentation_file (:obj:`str`): The name and path of the documentation file to respond with, relative to 
                                            the junction root. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("method", method)
        data.add_value_string("path", path)
        data.add_value_string("name", name)
        policy = DataObject()
        policy.add_value_string("type", policy_type)
        policy.add_value_string("name", policy_name)
        data.add_value_not_empty("policy", policy.data)
        data.add_value_not_empty("static_response_headers", static_response_headers)
        data.add_value_string("rate_limiting_policy", rate_limiting_policy)
        data.add_value_not_empty("url_aliases", url_aliases)
        documentation = DataObject()
        documentation.add_value_string("content_type", documentation_content_type)
        documentation.add_value_string("file", documentation_file)
        data.add_value_not_empty("documentation", documentation.data)

        endpoint = APIAC + "/resource/instance/{}/server/{}/resource/{}?server_type={}".format(
                instance, resource_server, resource_name, server_type)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def get_resource(self, instance=None, resource_server=None, resource_name=None, server_type="standard"):
        '''
        Retrieve an API Access Control Resources from a given server.

        Args:
            instance (:obj:`str`): The name of the Reverse Proxy Instance.
            resource_server (:obj:`str`): The name of the API Access Control Resource Server.
            server_type (:obj:`str`): The type of the specified resource server junction. Valid 
                                    values are ``vhj`` for a virtual junction or ``standard`` for 
                                    a standard junction. Defaults to ``standard`` if not specified.
            resource_name (:obj:`str`): The name of the API Access Control Resource.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the resource is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = APIAC + "/resource/instance/{}/server/{}/resource/{}?server_type={}".format(
                instance, resource_server, resource_name, server_type)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def delete_resource(self, instance=None, resource_server=None, resource_name=None, server_type="standard"):
        '''
        Delete an API Access Control Resources from a given server.

        Args:
            instance (:obj:`str`): The name of the Reverse Proxy Instance.
            resource_server (:obj:`str`): The name of the API Access Control Resource Server.
            server_type (:obj:`str`): The type of the specified resource server junction. Valid 
                                    values are ``vhj`` for a virtual junction or ``standard`` for 
                                    a standard junction. Defaults to ``standard`` if not specified.
            resource_name (:obj:`str`): The name of the API Access Control Resource.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = APIAC + "/resource/instance/{}/server/{}/resource/{}?server_type={}".format(
                instance, resource_server, resource_name, server_type)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200
        return response


    def list_resources(self, instance=None, resource_server=None, server_type="standard"):
        '''
        Retrieve a list of all API Access Control Resources for a given server.

        Args:
            instance (:obj:`str`): The name of the Reverse Proxy Instance.
            resource_server (:obj:`str`): The name of the API Access Control Resource Server.
            server_type (:obj:`str`): The type of the specified resource server junction. Valid 
                                    values are ``vhj`` for a virtual junction or ``standard`` for 
                                    a standard junction. Defaults to ``standard`` if not specified.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the resources are returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = APIAC + "/resource/instance/{}/server/{}/resource?server_type={}".format(
                instance, resource_server, server_type)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response
