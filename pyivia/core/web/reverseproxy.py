"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient
import urllib.parse


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
        '''
        Create a new WebSEAL Reverse Proxy instance.

        Args:
            inst_name (:obj:`str`): Name of the WebSEAL instance.
            host (:obj:`str`): The host name that is used by the Verify Identity Access policy server to contact the appliance.
            admin_id (:obj:`str`): The Verify Identity Access policy server's administrator name.
            admin_pwd (:obj:`str`): The Verify Identity Access policy server's administrator password.
            ssl_yn (:obj:`str`): Specifies whether to enable SSL communication between the instance and the LDAP server. "yes" || "no".
            key_file (:obj:`str`, optional): The file that contains the LDAP SSL certificate.
            cert_label (:obj:`str`, optional): The LDAP client certificate label.
            ssl_port (:obj:`str`, optional): The port number through which to communicate with the LDAP server.
            http_yn (:obj:`str`): Specifies whether to accept user requests across the HTTP protocol.
            http_port (:obj:`str`, optional): The port to listen for HTTP requests.
            https_yn (:obj:`str`): Specifies whether to accept user requests across the HTTPS protocol
            https_port (:obj:`str`, optional): The port to listen for HTTPS requests.
            nw_interface_yn (:obj:`str`): Specifies whether to use a logical network interface for the instance.
            ip_address (:obj:`str`, optional): The IP address for the logical interface.
            listening_port (:obj:`str`): This is the listening port through which the instance communicates with the 
                                Verify Identity Access policy server.
            domain (:obj:`str`): The Verify Identity Access policy server's domain.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the reverse proxy instance id is returned as JSON and can be accessed from
            the response.json attribute

        '''
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


    def delete_instance(self, webseal_id, admin_id, admin_pwd):
        '''
        Delete the specified WebSEAL Reverse Proxy if it exists.

        Args:
            webseal_id (:obj:`str`): The id of the WebSEAL instance to be removed.
            admin_id (:obj:`str`): The Verify Identity Access policy server's administrator name.
            admin_pwd (:obj:`str`): The Verify Identity Access policy server's administrator password.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        '''
        data = DataObject()
        data.add_value_string("admin_id", admin_id)
        data.add_value_string("admin_pwd", admin_pwd)
        data.add_value_string("operation", "unconfigure")

        endpoint = "%s/%s" % (REVERSEPROXY, webseal_id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def list_instances(self):
        """
        List the state of all configured WebSEAL Reverse Proxy instances.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the state of all instances is returned as JSON and can be accessed from
            the response.json attribute

        """
        response = self.client.get_json(REVERSEPROXY)
        response.success = response.status_code == 200

        return response


    def get_wga_defaults(self):
        '''
        Return the list of valid default WebSEAL instance configuration values.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the state of all instances is returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = self.client.get_json(WGA_DEFAULTS)
        response.success = response.status_code == 200

        return response


    def restart_instance(self, webseal_id):
        """
        Restart a WebSEAL Reverse Proxy. This will cause a brief service outage.

        Args:
            webseal_id (:obj:`str`): The WebSEAL instance which will be restarted.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        data = DataObject()
        data.add_value_string("operation", "restart")

        endpoint = "%s/%s" % (REVERSEPROXY, webseal_id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def configure_mmfa(
            self, webseal_id, lmi_hostname=None, lmi_port=None,
            lmi_username=None, lmi_password=None, runtime_hostname=None,
            runtime_port=None, runtime_username=None, runtime_password=None,
            reuse_certs=None,reuse_acls=None, reuse_pops=None):
        """
        Configure a WebSEAL instance to use the Federated runtime server for Mobile Multi-Factor Authentication.

        Args:
            webseal_id (:obj:`str`): The name of the WebSEAL instance to act on.
            lmi_hostname (:obj:`str`): The hostname of the LMI service.
            lmi_port (:obj:`str`): The port of the LMI service.
            lmi_username (:obj:`str`): The username used to authenticate with the LMI service.
            lmi_password (:obj:`str`): The password used to authenticate with the LMI service.
            runtime_hostname (:obj:`str`): The hostname of the runtime service.
            runtime_port (:obj:`str`): The port of the runtime service.
            runtime_username (:obj:`str`): The username used to authenticate with the runtime service.
            runtime_password (:obj:`str`): The password used to authenticate with the runtime service.
            reuse_certs (`bool`, optional): Should WebSEAL try to import the SSL certificate of the runtime service.
            reuse_acls (`bool`, optional): Should WebSEAL reuse ACLS with the same name.
            reuse_pops (`bool`, optional): Should WebSEAL reuse POPs with the same name.
            channel (:obj:`str`): Supports multi channel configuration, absence configures single channel. Valid channel values: browser, mobile.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
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
        runtime_hostname=None,runtime_port=None,runtime_username=None,runtime_password=None,
        runtime_type=None,runtime_load_cert=None,runtime_enable_mtls=None):
        '''
        Configure a WebSEAL instance to use the Federated runtime server to perform STS functions for federated identity
        partners.

        Args:
            webseal_id (:obj:`str`): Name of the WebSEAL instance to act on, which is a unique name that identifies the instance
            federation_id (:obj:`str`): The UUID which identifies the federation.
            reuse_certs (`bool`, optional): If the SSL certificate has already been saved, this flag indicates that the 
                                certificate should be reused instead of overwritten. Default is false.
            reuse_acls (`bool`, optional): A flag to indicate that any existing ACLs with the same name should be reused. 
                                If they are not reused, they will be replaced. Default is false .
            runtime_hostname (:obj:`str`): The hostname of the runtime server.
            runtime_port (:obj:`str`): The port of the runtime server. Must be the SSL port.
            runtime_username (:obj:`str`): The username used to authenticate with the runtime server.
            runtime_password (:obj:`str`): The password used to authenticate with the runtime server.
            runtime_type (:obj:`str`, optional): The type of runtime server, "local" or "remote". Default is "local".
            runtime_load_cert (:obj:`str`, optional): Control if th X.509 certificate should be read from the runtime 
                                                    server's https endpoint. Default is "on".
            runtime_enable_mtls (`bool`, optional): Control if the runtime server should use mutual TLS authentication.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
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
        '''
        Configure a WebSEAL instance to use the Federated runtime server for Advanced Access Control and Context Based
        Authorization decisions.

        Args:
            webseal_id (:obj:`str`): Name of the WebSEAL instance to act on, which is a unique name that identifies the instance
            junction (:obj:`str`): Junction point to create.
            reuse_certs (`bool`, optional): If the SSL certificate has already been saved, this flag indicates that the 
                                certificate should be reused instead of overwritten. Default is false.
            reuse_acls(:obj:`str`): A flag to indicate that any existing ACLs with the same name should be reused. If 
                                they are not reused, they will be replaced. Default is false .
            runtime_hostname (:obj:`str`): The hostname of the runtime server.
            runtime_port (:obj:`str`): The port of the runtime server. Must be the SSL port.
            runtime_username (:obj:`str`): The username used to authenticate with the runtime server.
            runtime_password (:obj:`str`): The password used to authenticate with the runtime server.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
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
        '''
        Add a configuration stanza with the RESTful web service

        Args:
            webseal_id (:obj:`str`): Name of the WebSEAL instance to act on, which is a unique name that identifies the instance.
            stanza_id (:obj:`str`): The name of the resource stanza entry.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created stanza is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = ("%s/%s/configuration/stanza/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id))
        response = self.client.post_json(endpoint)
        response.success = response.status_code == 200

        return response


    def delete_configuration_stanza(self, webseal_id, stanza_id):
        '''
        Remove a configuration stanza if it exists.

        Args:
            webseal_id (:obj:`str`): Name of the WebSEAL instance to act on, which is a unique name that identifies the instance
            stanza_id (:obj:`str`): The name of the resource stanza entry.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = ("%s/%s/configuration/stanza/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id))

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def add_configuration_stanza_entry(self, webseal_id, stanza_id, entry_name, value):
        '''
        Add a configuration entry to a stanza.

        Args:
            webseal_id (:obj:`str`): Name of the WebSEAL instance to act on, which is a unique name that identifies the instance
            stanza_id (:obj:`str`): The name of the resource stanza entry.
            entry_name (:obj:`str`): Name of the configuration entry to add.
            value (:obj:`str`): Value of the configuration entry to add.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the configuration entry id is returned as JSON and can be accessed from
            the response.json attribute

        '''
        data = DataObject()
        data.add_value("entries", [[str(entry_name), str(value)]])
        endpoint = ("%s/%s/configuration/stanza/%s/entry_name"
                    % (REVERSEPROXY, webseal_id, stanza_id))
        response = self.client.post_json(endpoint, data=data.data)
        response.success = response.status_code == 200

        return response


    def delete_configuration_stanza_entry(self, webseal_id, stanza_id, entry_name, value=None):
        '''
        Remove a configuration entry from a stanza. If a value is specified only an entry which matches the value will
        be removed.

        Args:
            webseal_id (:obj:`str`): Name of the WebSEAL instance to act on, which is a unique name that identifies the instance
            stanza_id (:obj:`str`): The name of the resource stanza entry.
            entry_name (:obj:`str`): Name of the configuration entry to add.
            value (:obj:`str`): Value of the configuration entry to add.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = ("%s/%s/configuration/stanza/%s/entry_name/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id, entry_name))
        if value:
            endpoint = "%s/value/%s" % (endpoint, value)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_configuration_stanza_entry(self, webseal_id, stanza_id, entry_name):
        '''
        Return the value of a configuration entry as JSON.

        Args:
            webseal_id (:obj:`str`): Name of the WebSEAL instance to act on, which is a unique name that identifies the instance
            stanza_id (:obj:`str`): The name of the resource stanza entry.
            entry_name (:obj:`str`): Name of the configuration entry to fetch 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the configuration entry value is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = ("%s/%s/configuration/stanza/%s/entry_name/%s"
                    % (REVERSEPROXY, webseal_id, stanza_id, entry_name))

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def update_configuration_stanza_entry(self, webseal_id, stanza_id, entry_name, value):
        '''
        Update a configuration stanza entry value. If it does not exist it will be created.

        Args:
            webseal_id (:obj:`str`): Name of the WebSEAL instance to act on, which is a unique name that identifies the instance
            stanza_id (:obj:`str`): The name of the resource stanza entry.
            entry_name (:obj:`str`): Name of the configuration entry to add.
            value (:obj:`str`): Value of the configuration entry to add.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
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
            server_uuid=None, virtual_hostname=None, server_dn=None, server_cn=None,
            local_ip=None, query_contents=None, case_sensitive_url=None,
            windows_style_url=None, ltpa_keyfile_password=None,
            proxy_hostname=None, sms_environment=None, vhost_label=None,
            force=None, delegation_support=None, scripting_support=None,
            junction_hard_limit=None, junction_soft_limit=None,
            server_port=None, https_port=None, http_port=None, proxy_port=None,
            remote_http_header=None):
        '''
        Create a standard or virtual WebSEAL junction.

        Args:
            webseal_id (:obj:`str`): The Reverse Proxy instance name.
            server_hostname (:obj:`str`): The DNS host name or IP address of the target back-end server.
            junction_point (:obj:`str`): Name of the location in the Reverse Proxy namespace where the root of the 
                                        back-end application server namespace is mounted.
            junction_type (:obj:`str`): Type of junction. The value is one of: tcp, ssl, tcpproxy, sslproxy, mutual.
            description (:obj:`str`, optional): An optional description for this junction.
            basic_auth_mode (:obj:`str`): Defines how the Reverse Proxy server passes client identity information in 
                                        HTTP basic authentication (BA) headers to the back-end server.
            tfim_sso (:obj:`str`): Enables IBM Security Federated Identity Manager single sign-on (SSO) for the junction. 
                                    Valid value is "yes" or "no".
            stateful_junction (:obj:`str`, optional): Specifies whether the junction supports stateful applications.
            preserve_cookie (:obj:`str`): Specifies whether modifications of the names of non-domain cookies are to be made.
            cookie_include_path (:obj:`str`, optional): Specifies whether script generated server-relative URLs are 
                                                        included in cookies for junction identification.
            transparent_path_junction (:obj:`str`, optional): Specifies whether a transparent path junction is created. 
                                                            Valid value is "yes" or "no".
            mutual_auth(:obj:`str`, optional): Specifies whether to enforce mutual authentication between a front-end 
                                               Reverse Proxy server and a back-end Reverse Proxy server over SSL.
            insert_ltpa_cookies (:obj:`str`, optional): Controls whether LTPA cookies are passed to the junctioned Web 
                                                        server. Valid value is "yes" or "no".
            insert_session_cookies (:obj:`str`): Controls whether to send the session cookie to the junctioned Web server.
            request_encoding (:obj:`str`, optional): Specifies the encoding to use when the system generates HTTP 
                                    headers for junctions.
            enable_basic_auth (:obj:`str`, optional): Specifies whether to use BA header information to authenticate 
                                                    to back-end server.
            key_label (:obj:`str`, optional): The key label for the client-side certificate that is used when the system 
                                            authenticates to the junctioned Web server.
            gso_resource_group (:obj:`str`, optional): The name of the GSO resource or resource group.
            junction_cookie_javascript_block (:obj:`str`, optional): Controls the junction cookie JavaScript block.
            client_ip_http (:obj:`str`, optional): Specifies whether to insert the IP address of the incoming request 
                                                into an HTTP header for transmission to the junctioned Web server.
            version_two_cookies (:obj:`str`, optional): Specifies whether LTPA version 2 cookies (LtpaToken2) are used.
            ltpa_keyfile (:obj:`str`, optional): Location of the key file that is used to encrypt the LTPA cookie data.
            authz_rules (:obj:`str`, optional): Specifies whether to allow denied requests and failure reason information 
                                            from authorization rules to be sent in the Boolean Rule header 
                                            (AM_AZN_FAILURE) across the junction.
            fsso_config_file (:obj:`str`, optional): The name of the configuration file that is used for forms based 
                                                    single sign-on.
            username (:obj:`str`, optional): The Reverse Proxy user name to send BA header information to the back-end server.
            password (:obj:`str`, optional): The Reverse Proxy password to send BA header information to the back-end server.
            server_uuid (:obj:`str`, optional): Specifies the UUID that will be used to identify the junctioned Web server.
            virtual_hostname (:obj:`str`, optional): Virtual host name that is used for the junctioned Web server.
            server_dn (:obj:`str`, optional): Specifies the distinguished name of the junctioned Web server.
            server_cn (:obj:`str`, optional): Specifies the common name, or subject alternative name, of the junctioned Web server. 
            local_ip (:obj:`str`, optional): Specifies the local IP address that the Reverse Proxy uses when the system 
                                    communicates with the target back-end server.
            query_contents (:obj:`str`, optional): Provides the Reverse Proxy with the correct name of the query_contents 
                                                    program file and where to find the file.
            case_sensitive_url (:obj:`str`, optional): Specifies whether the Reverse Proxy server treats URLs as case sensitive.
            windows_style_url (:obj:`str`, optional): Specifies whether Windows style URLs are supported.
            ltpa_keyfile_password (:obj:`str`, optional): Password for the key file that is used to encrypt LTPA cookie data.
            proxy_hostname (:obj:`str`, optional): The DNS host name or IP address of the proxy server.
            sms_environment (:obj:`str`, optional): Only applicable for virtual junctions. Specifies the replica set 
                                                    that sessions on the virtual junction are managed under.
            vhost_label (:obj:`str`): Only applicable for virtual junctions. Causes a second virtual junction to share 
                                    the protected object space with the initial virtual junction.
            force (:obj:`str`): Specifies whether to overwrite an existing junction of the same name.
            delegation_support (:obj:`str`): This option is valid only with junctions that were created with the type 
                                    of ssl or sslproxy.
            scripting_support (:obj:`str`): Supplies junction identification in a cookie to handle script-generated 
                                            server-relative URLs.
            junction_hard_limit (:obj:`str`): Defines the hard limit percentage for consumption of worker threads.
            junction_soft_limit (:obj:`str`): Defines the soft limit percentage for consumption of worker threads.
            server_port (:obj:`str`, optional): TCP port of the back-end third-party server.
            https_port (:obj:`str`): HTTPS port of the back-end third-party server.
            http_port (:obj:`str`): HTTP port of the back-end third-party server.
            proxy_port (:obj:`str`): The TCP port of the proxy server.
            remote_http_header (:obj:`str`): Controls the insertion of Verify Identity Access specific client identity 
                                            information in HTTP headers across the junction.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created instance is returned as JSON and can be accessed from
            the response.json attribute

        '''
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
        data.add_value_string("server_cn", server_cn)
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
        logger.debug("Junction config: {}".format(data.data))
        endpoint = "%s/%s/junctions" % (REVERSEPROXY, str(webseal_id))

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_junction(self, webseal_id, junction_point):
        '''
        Remove a junction from a WebSEAL Reverse Proxy instance.

        Args:
            webseal_id (:obj:`str`): The Reverse Proxy instance name.
            junction_point (:obj:`str`): Name of the location in the Reverse Proxy namespace where the root of the 
                                    back-end application server namespace is mounted.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        '''
        query = urllib.parse.urlencode({ JUNCTIONS_QUERY : junction_point})
        endpoint = "%s/%s/junctions?%s" % (REVERSEPROXY, webseal_id, query)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_junctions(self, webseal_id, detailed='false'):
        '''
        List the configured Standard and Virtual junctions. if the `detailed=true` query parameter is set on Verify 
        Access 10.0.4.0 and newer, detailed junction configuration in addition to the id and type attributes are returned.

        Args:
            webseal_id (:obj:`str`): The Reverse Proxy instance name.
            detailed (:obj:`str`, optional): Return detailed junction configuration.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful a list id and type of configured junctions is returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = "%s/%s/junctions?detailed=%s" % (REVERSEPROXY, webseal_id, detailed)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def import_management_root_files(self, webseal_id, file_path):
        '''
        Import a zip file into the management root of a WebSEAL reverse proxy instance. File path should be an absolute URL

        Args:
            webseal_id (:obj:`str`): The Reverse Proxy instance name.
            file_path (:obj:`str`): Zip file to be imported to the management root.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created file is returned as JSON and can be accessed from
            the response.json attribute

        '''
        response = Response()

        endpoint = ("%s/%s/management_root/" % (REVERSEPROXY, webseal_id))
        try:
            with open(file_path, 'rb') as f:
                #This should allow requests to detect application/zip content-type
                fd = {'file': f}
                response = self.client.post_file(endpoint, files=fd, data=None)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response


    def update_management_root_file(self, webseal_id, page_id, contents):
        '''
        Update the contents of a management root file of a WebSEAL instance.

        Args:
            webseal_id (:obj:`str`): The Reverse Proxy instance name.
            page_id (:obj:`str`): Path to the file to be updated in the management root file system.
            contents (:obj:`str`): Serialized contents of the updated management root file.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the updated file is returned as JSON and can be accessed from
            the response.json attribute

        '''
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
        '''
        Import a singe file into a WebSEAL management root file system.

        Args:
            webseal_id (:obj:`str`): The Reverse Proxy instance name.
            page_id (:obj:`str`): Path to the file to be updated in the management root file system.
            file_path (:obj:`str`): File to be uploaded to the management root file system.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the uploaded file is returned as JSON and can be accessed from
            the response.json attribute

        '''
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

    def configure_verify_gateway(self, webseal_id, mmfa=None, junction=None) -> Response:
        """
        Configure a WebSEAL instance to act as a gateway to an IBM Verify Identity tenant.

        Args:
            webseal_id (:obj:`str`): The name of the WebSEAL instance to act on.
            mmfa (`bool`): A flag indicating whether the MMFA endpoints should also be mapped.
            junction (:obj:`str`): AAC junction point to include in the HTTP Transformation rules.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        raise Exception("Not Yet Implemented")

class ReverseProxy9040(ReverseProxy):

    def __init__(self, base_url, username, password):
        super(ReverseProxy, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def configure_api_protection(
            self, webseal_id, hostname=None, port=None,
            username=None, password=None, reuse_certs=None,reuse_acls=None, api=None,
            browser=None, junction=None, auth_register=None, fapi_compliant=None):
        """
        Configure a WebSEAL instance to use the Federated runtime server to support OAuth and OIDC API Protection.

        Args:
            webseal_id (:obj:`str`): The name of the WebSEAL instance to act on.
            hostname (:obj:`str`): The hostname of the runtime service.
            port (:obj:`str`): The port of the runtime service.
            username (:obj:`str`): The username used to authenticate with the runtime service.
            password (:obj:`str`): The password used to authenticate with the runtime service.
            reuse_certs (`bool`, optional): Should WebSEAL try to import the SSL certificate of the runtime service.
            reuse_acls (`bool`, optional): Should WebSEAL reuse ACLS with the same name.
            api (`bool`, optional): Should this reverse proxy be configured for API protection. Default is false.
            browser (`bool`, optional): Should this reverse proxy be configured for Browser interaction. Default is false.
            junction (:obj:`str`): Junction point to create.
            auth_register (`bool`, optional): Will the client registration endpoint require authentication. Default is false.
            fapi_compliant (`bool`, optional): Configures reverse proxy instance to be FAPI Compliant. Default is false.
        """
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
        data.add_value_boolean("auth_register", auth_register)
        data.add_value_boolean("fapi_compliant", fapi_compliant)

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


    def configure_verify_gateway(self, webseal_id, mmfa=None, junction=None) -> Response:
        data = DataObject()
        data.add_value_boolean("mmfa", mmfa)
        data.add_value_string("junction", junction);

        endpoint = "{}/{}/verify_gateway_config".format(REVERSEPROXY, webseal_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response

    def configure_fed(self,webseal_id,federation_id=None,reuse_certs=False,reuse_acls=False,
        runtime_hostname=None,runtime_port=None,runtime_username=None,runtime_password=None,
        runtime_type=None,runtime_load_cert=None,runtime_enable_mtls=None):
        data = DataObject()
        data.add_value_string("federation_id", federation_id)
        data.add_value("reuse_certs", reuse_certs)
        data.add_value("reuse_acls", reuse_acls)

        runtime_data = DataObject()
        runtime_data.add_value_string("runtime_type", runtime_type)
        runtime_data.add_value_string("hostname", runtime_hostname)
        runtime_data.add_value_string("port", runtime_port)
        runtime_data.add_value_string("username", runtime_username)
        runtime_data.add_value_string("password", runtime_password)
        runtime_data.add_value_string("load_certificate", runtime_load_cert)
        runtime_data.add_value_boolean("enable_mtls", runtime_enable_mtls)

        data.add_value_not_empty("runtime", runtime_data.data)

        endpoint = "%s/%s/fed_config" % (REVERSEPROXY, webseal_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response