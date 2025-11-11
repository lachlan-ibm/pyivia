""""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


ADMIN_CONFIG = "/core/admin_cfg"

logger = logging.getLogger(__name__)


class AdminSettings(object):

    def __init__(self, base_url, username, password):
        super(AdminSettings, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get(self):
        """
        Get the current administrator configuration.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the obligations are returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(ADMIN_CONFIG)
        response.success = response.status_code == 200

        return response

    def update(self, old_password=None, new_password=None, confirm_password=None, min_heap_size=None, max_heap_size=None, 
            session_timeout=None, session_inactive_timeout=None, session_cache_purge=None, ba_session_timeout=None, 
            http_port=None, https_port=None, sshd_port=None, sshd_client_alive=None, swap_size=None, min_threads=None, max_threads=None, max_pool_size=None, 
            lmi_debugging_enabled=None, console_log_level=None, accept_client_certs=None, validate_client_cert_identity=None, 
            exclude_csrf_checking=None, enabled_server_protocols=None, enabled_tls=[], log_max_files=None, log_max_size=None,
            http_proxy=None, https_proxy=None, login_header=None, login_msg=None, access_log_fmt=None, lmi_msg_timeout=None,
            valid_verify_domains=None, audit_enabled=None, audit_json=None, audit_verbose=None) -> Response:
        """
        Update the administrator settings.

        Args:
            old_password (:obj:`str`, optional): The old administrator password. Required if changing the password.
            new_password (:obj:`str`, optional): The new administrator password. Required if changing the password.
            confirm_password (:obj:`str`), optional: Confirmation of the new administrator password. Required if 
                            changing the password.
            min_heap_size (`int`): The minimum heap size, in megabytes, for the JVM.
            max_heap_size (`int`): The minimum heap size, in megabytes, for the JVM.
            session_timeout (`int`): The length of time, in minutes, that a session can remain idle before it is 
                            deleted (valid values: 0 - 720).
            session_inactive_timeout (`int`): The length of time, in minutes, that a session can remain idle before it 
                            is deleted (valid values: -1 to 720).
            http_port (`int`): The TCP port on which the LMI will listen.
            https_port (`int`): The SSL port on which the LMI will listen. A default value of 443 is used.
            sshd_port (`int`, optional): The port on which the SSH daemon will listen. A default value of 22 is used.
            sshd_client_alive (`int`): The number of seconds that the server will wait before sending a null packet to 
                            the client.
            swap_size (`int`): The amount of allocated swap space, in Megabytes.
            min_threads (`int`): The minimum number of threads which will handle LMI requests. A default value of 6 is 
                            used.
            max_threads (`int`): The maximum number of threads which will handle LMI requests. A default value of 6 is used.
            max_pool_size (`int`): The maximum number of connections for the connection pool. The default value is 100.
            lmi_debugging_enabled (`bool`): A boolean value which is used to control whether LMI debugging is enabled 
                            or not. By default debugging is disabled.
            console_log_level (`bool`): The console messaging level of the LMI (valid values: INFO, AUDIT, WARNING, 
                            ERROR and OFF). A default value of OFF is used.
            accept_client_certs (`bool`): A boolean value which is used to control whether SSL client certificates are 
                            accepted by the local management interface.
            validate_client_cert_identity (`bool`): A boolean value which is used to control whether the subject DN 
                            contained within an SSL client certificate is validated against the user registry. By 
                            default validation is disabled.
            exclude_csrf_checking (:obj:`str`, optional): A comma-separated string which lists the users for which CSRF checking 
                            should be disabled.
            enabled_server_protocols (:obj:`str`): Specifies which secure protocols will be accepted when connecting to 
                            the LMI.
            enabled_tls (:obj:`str`): List of Enabled TLS protocols for the local management interface in the format 
                            enabledTLS:["TLSv1", "TLSv1.1", TLSv1.2"].
            log_max_files (`int`): The maximum number of log files that are retained. The default value is 2.
            log_max_size (`int`): The maximum size (in MB) that a log file can grow to before it is rolled over. The 
                            default value is 20.
            http_proxy (`int`): The proxy (<host>:<port>) to be used for HTTP communication from the LMI.
            https_proxy (`int`): The proxy (<host>:<port>) to be used for HTTPS communication from the LMI.
            login_header (:obj:`str`): This is a customizable header that is displayed when accessing the login page 
                            in a web browser and after logging in via SSH.
            login_msg (:obj:`str`): This is a customizable message that is displayed when accessing the login page in 
                            a web browser and after logging in via SSH.
            access_log_fmt (:obj:`str`): The template string to use for the LMI access.log file.
            lmi_msg_timeout (`int`): This is a timeout (in seconds) for notification messages that appear in the LMI.
            valid_verify_domains (:obj:`str`): This is a space separated list of valid domains for IBM Security Verify.
            audit_enabled (`bool`, optional): Enable audit event logging for the Local Management Interface. only valid
                                              for v11.0.1.0 and newer.
            audit_json (`bool`, optional): Emit JSON formatted audit events for the Local Management Interface. only valid
                                           for v11.0.1.0 and newer.
            audit_verbose(`bool`, optional): Include request properties when auditing requests to the Local Management
                                             Interface. Only valid for v11.0.1.0 and newer.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        data.add_value_string("oldPassword", old_password)
        data.add_value_string("newPassword", new_password)
        data.add_value_string("confirmPassword", confirm_password)
        data.add_value_string("consoleLogLevel", console_log_level)
        data.add_value_string("excludeCsrfChecking", exclude_csrf_checking)
        data.add_value("minHeapSize", min_heap_size)
        data.add_value("maxHeapSize", max_heap_size)
        data.add_value("sessionTimeout", session_timeout)
        data.add_value("httpPort", http_port)
        data.add_value("httpsPort", https_port)
        data.add_value("minThreads", min_threads)
        data.add_value("maxThreads", max_threads)
        data.add_value("maxPoolSize", max_pool_size)
        data.add_value_boolean("lmiDebuggingEnabled", lmi_debugging_enabled)
        data.add_value_boolean("acceptClientCerts", accept_client_certs)
        data.add_value_boolean(
            "validateClientCertIdentity", validate_client_cert_identity)
        
        response = self.client.put_json(ADMIN_CONFIG, data.data)
        response.success = response.status_code == 200

        return response

class AdminSetting10000(AdminSettings):

    def update(self, old_password=None, new_password=None, confirm_password=None, min_heap_size=None, max_heap_size=None, 
            session_timeout=None, session_inactive_timeout=None, session_cache_purge=None, ba_session_timeout=None, 
            http_port=None, https_port=None, sshd_port=None, sshd_client_alive=None, swap_size=None, min_threads=None, max_threads=None, max_pool_size=None, 
            lmi_debugging_enabled=None, console_log_level=None, accept_client_certs=None, validate_client_cert_identity=None, 
            exclude_csrf_checking=None, enabled_server_protocols=None, enabled_tls=[], log_max_files=None, log_max_size=None,
            http_proxy=None, https_proxy=None, login_header=None, login_msg=None, access_log_fmt=None, lmi_msg_timeout=None,
            valid_verify_domains=None, audit_enabled=None, audit_json=None, audit_verbose=None):
        data = DataObject()
        data.add_value_string("oldPassword", old_password)
        data.add_value_string("newPassword", new_password)
        data.add_value_string("confirmPassword", confirm_password)
        data.add_value_string("consoleLogLevel", console_log_level)
        data.add_value_string("excludeCsrfChecking", exclude_csrf_checking)
        data.add_value("minHeapSize", min_heap_size)
        data.add_value("maxHeapSize", max_heap_size)
        data.add_value("sessionTimeout", session_timeout)
        data.add_value("httpPort", http_port)
        data.add_value("httpsPort", https_port)
        data.add_value("minThreads", min_threads)
        data.add_value("maxThreads", max_threads)
        data.add_value("maxPoolSize", max_pool_size)
        data.add_value_boolean("lmiDebuggingEnabled", lmi_debugging_enabled)
        data.add_value_boolean("acceptClientCerts", accept_client_certs)
        data.add_value_boolean(
            "validateClientCertIdentity", validate_client_cert_identity)
        data.add_value("sshdPort", sshd_port)
        data.add_value("sessionInactivityTimeout", session_inactive_timeout)
        data.add_value_string("swapFileSize", swap_size)
        data.add_value("sessionCachePurge", session_cache_purge)
        data.add_value("maxFiles", log_max_files)
        data.add_value("maxFileSize", log_max_size)
        data.add_value_string("httpProxy", http_proxy)
        data.add_value_string("httpsProxy", https_proxy)
        data.add_value_string("loginHeader", login_header)
        data.add_value_string("loginMessage", login_msg)
        data.add_value("sshdClientAliveInterval", sshd_client_alive)
        data.add_value_string("enabledServerProtocols", enabled_server_protocols)
        data.add_value_not_empty("enabledTLS", enabled_tls)
        data.add_value("baSessionTimeout", ba_session_timeout)
        data.add_value_string("accessLogFormat", access_log_fmt)
        data.add_value_string("lmiMessageTimeout", lmi_msg_timeout)
        data.add_value_string("validVerifyDomains", valid_verify_domains)
        
        response = self.client.put_json(ADMIN_CONFIG, data.data)
        response.success = response.status_code == 200

        return response

class AdminSetting11010(AdminSettings):

    def update(self, old_password=None, new_password=None, confirm_password=None, min_heap_size=None, max_heap_size=None, 
            session_timeout=None, session_inactive_timeout=None, session_cache_purge=None, ba_session_timeout=None, 
            http_port=None, https_port=None, sshd_port=None, sshd_client_alive=None, swap_size=None, min_threads=None, max_threads=None, max_pool_size=None, 
            lmi_debugging_enabled=None, console_log_level=None, accept_client_certs=None, validate_client_cert_identity=None, 
            exclude_csrf_checking=None, enabled_server_protocols=None, enabled_tls=[], log_max_files=None, log_max_size=None,
            http_proxy=None, https_proxy=None, login_header=None, login_msg=None, access_log_fmt=None, lmi_msg_timeout=None,
            valid_verify_domains=None, audit_enabled=None, audit_json=None, audit_verbose=None) -> Response:
        data = DataObject()
        data.add_value_string("oldPassword", old_password)
        data.add_value_string("newPassword", new_password)
        data.add_value_string("confirmPassword", confirm_password)
        data.add_value_string("consoleLogLevel", console_log_level)
        data.add_value_string("excludeCsrfChecking", exclude_csrf_checking)
        data.add_value("minHeapSize", min_heap_size)
        data.add_value("maxHeapSize", max_heap_size)
        data.add_value("sessionTimeout", session_timeout)
        data.add_value("httpPort", http_port)
        data.add_value("httpsPort", https_port)
        data.add_value("minThreads", min_threads)
        data.add_value("maxThreads", max_threads)
        data.add_value("maxPoolSize", max_pool_size)
        data.add_value_boolean("lmiDebuggingEnabled", lmi_debugging_enabled)
        data.add_value_boolean("acceptClientCerts", accept_client_certs)
        data.add_value_boolean(
            "validateClientCertIdentity", validate_client_cert_identity)
        data.add_value("sshdPort", sshd_port)
        data.add_value("sessionInactivityTimeout", session_inactive_timeout)
        data.add_value_string("swapFileSize", swap_size)
        data.add_value("sessionCachePurge", session_cache_purge)
        data.add_value("maxFiles", log_max_files)
        data.add_value("maxFileSize", log_max_size)
        data.add_value_string("httpProxy", http_proxy)
        data.add_value_string("httpsProxy", https_proxy)
        data.add_value_string("loginHeader", login_header)
        data.add_value_string("loginMessage", login_msg)
        data.add_value("sshdClientAliveInterval", sshd_client_alive)
        data.add_value_string("enabledServerProtocols", enabled_server_protocols)
        data.add_value_not_empty("enabledTLS", enabled_tls)
        data.add_value("baSessionTimeout", ba_session_timeout)
        data.add_value_string("accessLogFormat", access_log_fmt)
        data.add_value_string("lmiMessageTimeout", lmi_msg_timeout)
        data.add_value_string("validVerifyDomains", valid_verify_domains)
        data.add_value_string("auditEnabled", audit_enabled)
        data.add_value_string("auditJsonFormat", audit_json)
        data.add_value_string("auditVerbose", audit_verbose)

        response = self.client.put_json(ADMIN_CONFIG, data.data)
        response.success = response.status_code == 200

        return response