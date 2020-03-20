""""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


ADMIN_CONFIG = "/core/admin_cfg"

logger = logging.getLogger(__name__)


class AdminSettings(object):

    def __init__(self, base_url, username, password):
        super(AdminSettings, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get(self):
        response = self.client.get_json(ADMIN_CONFIG)
        response.success = response.status_code == 200

        return response

    def update(
            self, old_password=None, new_password=None, confirm_password=None,
            min_heap_size=None, max_heap_size=None, session_timeout=None,
            http_port=None, https_port=None, min_threads=None, max_threads=None,
            max_pool_size=None, lmi_debugging_enabled=None,
            console_log_level=None, accept_client_certs=None,
            validate_client_cert_identity=None, exclude_csrf_checking=None,
            enable_ssl_v3=None):
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
        data.add_value_bool("lmiDebuggingEnabled", lmi_debugging_enabled)
        data.add_value_bool("acceptClientCerts", accept_client_certs)
        data.add_value_bool(
            "validateClientCertIdentity", validate_client_cert_identity)
        data.add_value_bool("enableSSLv3", enable_ssl_v3)
        
        response = self.client.put_json(ADMIN_CONFIG, data.data)
        response.success = response.status_code == 200

        return response

class AdminSetting10000(AdminSettings):

    def update(
            self, old_password=None, new_password=None, confirm_password=None,
            min_heap_size=None, max_heap_size=None, session_timeout=None,
            http_port=None, https_port=None, min_threads=None, max_threads=None,
            max_pool_size=None, lmi_debugging_enabled=None,
            console_log_level=None, accept_client_certs=None,
            validate_client_cert_identity=None, exclude_csrf_checking=None,
            enable_ssl_v3=None, sshd_port=None, session_inactivity_timeout=None,
            max_files=None, max_file_size=None, http_proxy=None, https_proxy=None,
            login_header=None, login_message=None, sshd_client_alive_interval=None,
            enabled_server_protocols=None, enabled_tls=None, session_cache_purge=None):
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
        data.add_value_bool("lmiDebuggingEnabled", lmi_debugging_enabled)
        data.add_value_bool("acceptClientCerts", accept_client_certs)
        data.add_value_bool(
            "validateClientCertIdentity", validate_client_cert_identity)
        data.add_value_bool("enableSSLv3", enable_ssl_v3)
        data.add_value("sshdPort", sshd_port)
        data.add_value("sessionInactivityTimeout", session_inactivity_timeout)
        data.add_value("sessionCachePurge", session_cache_purge)
        data.add_value("maxFiles", max_files)
        data.add_value("maxFileSize", max_file_size)
        data.add_value_string("httpProxy", http_proxy)
        data.add_value_string("httpsProxy", https_proxy)
        data.add_value_string("loginHeader", login_header)
        data.add_value_string("loginMessage", login_message)
        data.add_value("sshdClientAliveInterval", sshd_client_alive_interval)
        data.add_value_string("enabledServerProtocols", enabled_server_protocols)
        data.add_value_not_empty("enabledTLS", enabled_tls)
        
        response = self.client.put_json(ADMIN_CONFIG, data.data)
        response.success = response.status_code == 200

        return response
