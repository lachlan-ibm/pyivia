"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


SERVER_CONNECTION_ROOT = "/mga/server_connections"
SERVER_CONNECTION_LDAP = "/mga/server_connections/ldap"
SERVER_CONNECTION_ISAM_RUNTIME = "/mga/server_connections/isamruntime"
SERVER_CONNECTION_WEB_SERVICE = "/mga/server_connections/ws"
SERVER_CONNECTION_SMTP = "/mga/server_connections/smtp"
SERVER_CONNECTION_CI = "/mga/server_connections/ci"
SERVER_CONNECTION_JDBC = "/mga/server_connections/jdbc"


logger = logging.getLogger(__name__)


class ServerConnections(object):

    def __init__(self, base_url, username, password):
        super(ServerConnections, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_ldap(
            self, name=None, description=None, locked=None,
            connection_host_name=None, connection_bind_dn=None,
            connection_bind_pwd=None, connection_ssl_truststore=None,
            connection_ssl_auth_key=None, connection_host_port=None,
            connection_ssl=None, connect_timeout=None, servers=None):
        connection_data = DataObject()
        connection_data.add_value_string("hostName", connection_host_name)
        connection_data.add_value_string("bindDN", connection_bind_dn)
        connection_data.add_value_string("bindPwd", connection_bind_pwd)
        connection_data.add_value_string(
            "sslTruststore", connection_ssl_truststore)
        connection_data.add_value_string("sslAuthKey", connection_ssl_auth_key)
        connection_data.add_value("hostPort", connection_host_port)
        connection_data.add_value("ssl", connection_ssl)

        manager_data = DataObject()
        manager_data.add_value("connectTimeout", connect_timeout)

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("type", "ldap")
        data.add_value("locked", locked)
        data.add_value("servers", servers)
        data.add_value_not_empty("connection", connection_data.data)
        data.add_value_not_empty("connectionManager", manager_data.data)

        endpoint = SERVER_CONNECTION_LDAP + "/v1"

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response

    def delete_ldap(self, uuid):
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_LDAP, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def list_ldap(self):
        endpoint = SERVER_CONNECTION_LDAP + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_smtp(
            self, name=None, description=None,connect_timeout=None, 
            connection_host_name=None, connection_host_port=None,
            connection_ssl=None, connection_user=None, connection_password=None):
        connection_data = DataObject()
        connection_data.add_value_string("hostName", connection_host_name)
        connection_data.add_value("hostPort", connection_host_port)
        connection_data.add_value("ssl", connection_ssl)
        connection_data.add_value("user", connection_user)
        connection_data.add_value("password", connection_password)

        manager_data = DataObject()
        manager_data.add_value("connectTimeout", connect_timeout)

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("type", "smtp")
        data.add_value_not_empty("connection", connection_data.data)
        data.add_value_not_empty("connectionManager", manager_data.data)

        endpoint = SERVER_CONNECTION_SMTP + "/v1"

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response

    def delete_smtp(self, uuid):
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_SMTP, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def list_smtp(self):
        endpoint = SERVER_CONNECTION_SMTP + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_ci(
            self, name=None, description=None, locked=None,
            connection_host_name=None, connection_client_id=None,
            connection_client_secret=None, connection_ssl_truststore=None):
        connection_data = DataObject()
        connection_data.add_value_string("adminHost", connection_host_name)
        connection_data.add_value("clientId", connection_client_id)
        connection_data.add_value("clientSecret", connection_client_secret)
        connection_data.add_value("ssl", True)
        connection_data.add_value("sslTruststore", connection_ssl_truststore)
        connection_data.add_value("usersEndpoint", "/v2.0/Users")
        # yes, I know this is a token endpoint. The parameter name was poorly selected
        connection_data.add_value("authorizeEndpoint", "/v1.0/endpoint/default/token")
        connection_data.add_value("authenticatorsEndpoint", "/v1.0/authenticators")
        connection_data.add_value("authnmethodsEndpoint", "/v1.0/authnmethods")

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("type", "ci")
        data.add_value_string("locked", locked)
        data.add_value_not_empty("connection", connection_data.data)

        endpoint = SERVER_CONNECTION_CI + "/v1"

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response

    def delete_ci(self, uuid):
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_CI, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def list_ci(self):
        endpoint = SERVER_CONNECTION_CI + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_web_service(
            self, name=None, description=None, locked=None, connection_url=None,
            connection_user=None, connection_password=None,
            connection_ssl_truststore=None, connection_ssl_auth_key=None,
            connection_ssl=None):
        connection_data = DataObject()
        connection_data.add_value_string("url", connection_url)
        connection_data.add_value_string("user", connection_user)
        connection_data.add_value_string("password", connection_password)
        connection_data.add_value_string(
            "sslTruststore", connection_ssl_truststore)
        connection_data.add_value_string("sslAuthKey", connection_ssl_auth_key)
        connection_data.add_value("ssl", connection_ssl)

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("type", "ws")
        data.add_value("locked", locked)
        data.add_value_not_empty("connection", connection_data.data)

        endpoint = SERVER_CONNECTION_WEB_SERVICE + "/v1"

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response

    def delete_web_service(self, uuid):
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_WEB_SERVICE, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def list_web_service(self):
        endpoint = SERVER_CONNECTION_WEB_SERVICE + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_jdbc(self, name=None, description=None, locked=None, database_type=None, connection_jndi=None,
            connection_host_name=None, connection_port=None, connection_ssl=None, connection_user=None,
            connection_password=None, connection_type=None, connection_service_name=None, 
            connection_dataabse_name=None, connection_aged_timeout=None, connection_connection_timeout=None, 
            connection_per_thread=None, connection_max_idle=None, connection_max_pool_size=None, 
            connection_min_pool_size=None, connection_per_local_thread=None, connection_purge_policy=None,
            connection_reap_time=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("locked", locked)
        data.add_value_string("type", database_type)
        data.add_value_string("jndiId", connection_jndi)

        connection_data = DataObject()
        connection_data.add_value_string("serverName", connection_host_name)
        connection_data.add_value_string("portNumber", connection_port)
        connection_data.add_value_string("ssl", connection_ssl)
        connection_data.add_value_string("user", connection_user)
        connection_data.add_value_string("password", connection_password)
        connection_data.add_value_string("type", connection_type)
        connection_data.add_value_string("serviceName", connection_service_name)
        connection_data.add_value_string("databaseName", connection_database_name)

        data.add_value_string("connection", connection_data.data)

        manager = DataObject()
        manager.add_value_string("agedTimeout", connection_aged_timeout)
        manager.add_value_string("connectionTimeout", connection_connection_timeout)
        manager.add_value_string("maxConnectionsPerThread", connection_per_thread)
        manager.add_value_string("maxIdleTime", connection_max_idle)
        manager.add_value_string("maxPoolSize", connection_max_pool_size)
        manager.add_value_string("minPoolSize", connection_min_pool_size)
        manager.add_value_string("numConnectionsPerThreadLocal", connection_per_thread_local)
        manager.add_value_string("purgePolicy", connection_purge_policy)
        manager.add_value_string("reapTime", connection_reap_time)

        data.add_value_string("connectionManager", manager.data)

        endpoint = SERVER_CONNECTION_JDBC + "/v1"
        
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response


    def delete_jdbc(self, uuid):
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_JDBC, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def list_jdbc(self):
        endpoint = SERVER_CONNECTION_JDBC + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_all(self):
        endpoint = SERVER_CONNECTION_ROOT + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response
        
class ServerConnections9050(ServerConnections):

    def __init__(self, base_url, username, password):
        super(ServerConnections, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_isam_runtime(
            self, name=None, description=None, locked=None,
            connection_bind_dn=None,
            connection_bind_pwd=None, connection_ssl_truststore=None,
            connection_ssl_auth_key=None,
            connection_ssl=None, connect_timeout=None, servers=None):
        connection_data = DataObject()        
        connection_data.add_value_string("bindDN", connection_bind_dn)
        connection_data.add_value_string("bindPwd", connection_bind_pwd)
        connection_data.add_value_string(
            "sslTruststore", connection_ssl_truststore)
        connection_data.add_value_string("sslAuthKey", connection_ssl_auth_key)        
        connection_data.add_value("ssl", connection_ssl)

        manager_data = DataObject()
        manager_data.add_value("connectTimeout", connect_timeout)

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("type", "isamruntime")
        data.add_value("locked", locked)
        data.add_value("servers", servers)
        data.add_value_not_empty("connection", connection_data.data)
        data.add_value_not_empty("connectionManager", manager_data.data)

        endpoint = SERVER_CONNECTION_ISAM_RUNTIME + "/v1"        
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response

    def get_runtime(self):
        endpoint = SERVER_CONNECTION_ISAM_RUNTIME + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response
        
    def delete_runtime(self, uuid):
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_ISAM_RUNTIME, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204
        return response
