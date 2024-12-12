"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


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


    def create_ldap(self, name=None, description=None, locked=None,
            connection_host_name=None, connection_bind_dn=None,
            connection_bind_pwd=None, connection_ssl_truststore=None,
            connection_ssl_auth_key=None, connection_host_port=None,
            connection_ssl=None, connect_timeout=None, servers=None):
        '''
        Create a LDAP server connection.

        Args:
            name (:obj:`str`): Unique name for the server connection.
            description (:obj:`str`): Description of the server connection.
            locked (bool): Controls whether the connection is allowed to be deleted.
            connection_host_name (:obj:`str`): Host name for the LDAP server.
            connection_bind_dn (:obj:`str`): Name to bind to LDAP server for admin operations.
            connection_bind_pwd (:obj:`str`): Password associated with admin domain name.
            connection_ssl_truststore (:obj:`str`, optional): The SSL database to use. Only valid if ssl is enabled.
            connection_ssl_auth_key (:obj:`str`, optional): The certificate to use to authentication connections. Only 
                                                            valid if ssl is enabled.
            connection_host_port (:obj:`str`): The port that the LDAP server is listening on.
            connection_ssl (bool): Enable SSL encryption on connections.
            connect_timeout (int): Length of time Verify Identity Access will wait before timing out a connection.
            servers: (:obj:`list` of :obj:`dict`): Additional LDAP servers for this connection.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the uuid of the created LDAP connection can be accessed from the 
            response.id_from_location attribute.

        '''
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
        '''
        Delete an existing LDAP server connection.

        Args:
            uuid (:obj:`str`): The id of the LDAP server connection to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_LDAP, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def list_ldap(self):
        '''
        List the configured LDAP server connections.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the LDAP server connections are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = SERVER_CONNECTION_LDAP + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create_smtp(self, name=None, description=None, locked=None, connect_timeout=None, 
            connection_host_name=None, connection_host_port=None,
            connection_ssl=None, connection_user=None, connection_password=None):
        '''
        Create a SMTP server connection.

        Args:
            name (:obj:`str`): Unique name for the server connection.
            description (:obj:`str`): Description of the server connection.
            locked (bool): Controls whether the connection is allowed to be deleted.
            connect_timeout (int): Amount of time Verify Identity Access will wait before timing out a connection.
            connection_host_name (:obj:`str`, optional): The hostname of the SMTP server. Only valid if SSL is enabled.
            connection_host_port (:obj:`str`, optional): The port that the SMTP server is listening on. Only valid if
                                                        SSL is enabled.
            connection_ssl (bool): Enable SSL encryption on connections.
            connection_user (:obj:`str`, optional): User to authenticate to SMTP server.
            connection_password (:obj:`str`, optional): Password to authenticate to SMTP server.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the uuid of the created LDAP connection can be accessed from the 
            response.id_from_location attribute.

        '''
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
        data.add_value("locked", locked)
        data.add_value_string("type", "smtp")
        data.add_value_not_empty("connection", connection_data.data)
        data.add_value_not_empty("connectionManager", manager_data.data)

        endpoint = SERVER_CONNECTION_SMTP + "/v1"

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response


    def delete_smtp(self, uuid):
        '''
        Delete an existing SMTP server connection.

        Args:
            uuid (:obj:`str`) The id of the SMTP server connection to remove.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_SMTP, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def list_smtp(self):
        '''
        List the configured SMTP server connections.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the SMTP server connections are returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = SERVER_CONNECTION_SMTP + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create_ci(self, name=None, description=None, locked=None,
            connection_host_name=None, connection_client_id=None,
            connection_client_secret=None, connection_ssl_truststore=None):
        '''
        Create a Cloud Identity server connection.

        Args:
            name (:obj:`str`): Unique name for the server connection.
            description (:obj:`str`): Description of the server connection.
            locked (bool): Controls whether the connection is allowed to be deleted.
            connection_host_name (:obj:`str`): The hostname of the Cloud Identity Tenant.
            connection_client_id (:obj:`str`): The id of the OIDC client to authenticate to Cloud Identity.
            connection_client_secret (:obj:`str`): The OIDC client secret to authenticate to Cloud Identity.
            connection_ssl_truststore (:obj:`str`): The SSL database to authenticate connections.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the uuid of the created Cloud Identity connection can be accessed from the 
            response.id_from_location attribute

        '''
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
        '''
        Delete an existing Cloud Identity server connection.

        Args:
            uuid (:obj:`str`): The id of the Cloud Identity connection to remove.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_CI, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def list_ci(self):
        '''
        List the configured Cloud Identity server connections.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the Cloud Identity server connections are returned as JSON and can be accessed from
            the response.json attribute

        '''
        endpoint = SERVER_CONNECTION_CI + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def create_web_service(self, name=None, description=None, locked=None, connection_url=None,
            connection_user=None, connection_password=None, connection_ssl_truststore=None, 
            connection_ssl_auth_key=None, connection_ssl=None):
        '''
        Create a Web Service server connection.

        Args:
            name (:obj:`str`): Unique name for the server connection.
            description (:obj:`str`): Description of the server connection.
            locked (bool): Controls whether the connection is allowed to be deleted.
            connection_url (:obj:`str`): The URL to the server.
            connection_user (:obj:`str`, optional): The user to authenticate to the Web Service.
            connection_password (:obj:`str`, optional): The password to authenticate to the Web Service.
            connection_ssl_truststore (:obj:`str`, optional): The SSL database to authenticate connections. Only valid 
                                                            if SSL is enabled.
            connection_ssl_auth_key (:obj:`str`): The certificate to authenticate connections. Only valid if SSL is 
                                                enabled.
            connection_ssl (bool): Flag to enable SSL encryption for connections.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the uuid of the created Web Service connection can be accessed from the 
            response.id_from_location attribute

        '''
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
        '''
        Delete an existing Web Service server connection.

        Args:
            uuid (:obj:`str`): The id of the Web Service server connection to remove.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

        '''
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_WEB_SERVICE, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def list_web_service(self):
        '''
        List the configure Web Service server connections.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the Web Service server connections are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = SERVER_CONNECTION_WEB_SERVICE + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_jdbc(self, name=None, description=None, locked=None, database_type=None, connection_jndi=None,
            connection_host_name=None, connection_port=None, connection_ssl=None, connection_user=None,
            connection_password=None, connection_type=None, connection_service_name=None, 
            connection_database_name=None, connection_aged_timeout=None, connection_connection_timeout=None, 
            connection_per_thread=None, connection_max_idle=None, connection_max_pool_size=None, 
            connection_min_pool_size=None, connection_per_local_thread=None, connection_purge_policy=None,
            connection_reap_time=None):
        '''
        Create JDBC server connection.

        Args:
            name (:obj:`str`): Unique name for the server connection.
            description (:obj:`str`): Description of the server connection.
            locked (bool): Controls whether the connection is allowed to be deleted.
            database_type (:obj:`str`): The database type deployed on the server connection.
            connection_jndi (:obj:`str`): The internal JNDI id used to reference this connection.
            connection_host_name (:obj:`str`): The hostname for the database server.
            connection_port (int):The port that the database is listening on.
            connection_ssl (bool: Flag to enable SSL encryption on connections.
            connection_user (:obj:`str`): User to authenticate to database.
            connection_password (:obj:`str`): Password to authenticate to database.
            connection_type (:obj:`str`): The Oracle JDBC driver type. Only valid for Oracle databases.
            connection_service_name (:obj:`str`): The name of the database service to connect to.
            connection_database_name (:obj:`str`): The name of the database to connect to.
            connection_aged_timeout (int): Amount of time before a physical connection can be discarded by pool maintenance.
            connection_connection_timeout (int): Amount of time after which a connection request times out.
            connection_per_thread (int): Limits the number of open connections on each thread.
            connection_max_idle (:obj:`str`): Amount of time after which an unused or idle connection can be discarded.
            connection_max_pool_size (int): Maximum number of physical connections for a pool. A value of 0 is unlimited.
            connection_min_pool_size (int): Minimum number of physical connections to maintain in the pool.
            connection_per_local_thread (int): Caches the specified number of connections for each thread.
            connection_purge_policy (:obj:`str`): Specifies which connections to destroy when a stale connection is 
                                                detected in a pool.
            connection_reap_time (:obj:`str`): Amount of time between runs of the pool maintenance thread. A value of -1
                                                disables pool maintenance.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the uuid of the created JDBC can be accessed from the 
            response.id_from_location attribute

        '''
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
        manager.add_value_string("numConnectionsPerThreadLocal", connection_per_local_thread)
        manager.add_value_string("purgePolicy", connection_purge_policy)
        manager.add_value_string("reapTime", connection_reap_time)

        data.add_value_string("connectionManager", manager.data)

        endpoint = SERVER_CONNECTION_JDBC + "/v1"
        
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response


    def delete_jdbc(self, uuid):
        '''
        Delete an existing JDBC server connection.

        Args:
            uuid (:obj:`str`): The id of the JDBC to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_JDBC, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def list_jdbc(self):
        '''
        List the configured JDBC server connections.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the JDBC's are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = SERVER_CONNECTION_JDBC + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list_all(self):
        '''
        List all of the configured server connections.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the server connections are returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = SERVER_CONNECTION_ROOT + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


class ServerConnections9050(ServerConnections):

    def __init__(self, base_url, username, password):
        super(ServerConnections, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_isam_runtime(self, name=None, description=None, locked=None,
            connection_bind_dn=None, connection_bind_pwd=None, connection_ssl_truststore=None,
            connection_ssl_auth_key=None, connection_ssl=None, connect_timeout=None, servers=None):
        '''
        Create an Verify Identity Access Runtime server connection.

        Args:
            name (:obj:`str`): Unique name for the server connection.
            description (:obj:`str`): Description of the server connection.
            locked (bool): Controls whether the connection is allowed to be deleted.
            connection_bind_dn (:obj:str`): The domain name to bind to the runtime server.
            connection_bind_pwd (:obj:`str`): The password to bind to the runtime server.
            connection_ssl_truststore (:obj:`str`): The SSL database to authenticate connections. Only valid if SSL is
                                                enabled.
            connection_ssl_auth_key (:obj:`str`): The certificate to authenticate connections. Only valid if SSL is enabled.
            connection_ssl (bool): Flag to enable SSL encryption for connections.
            connect_timeout (int): Length of time Verify Identity Access will wait before timing out a connection.
            servers: (:obj:`list` of :obj:`dict`): Additional LDAP servers for this connection.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the uuid of the created LDAP connection can be accessed from the 
            response.id_from_location attribute

        '''
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


    def list_runtime(self):
        '''
        List the configured Verify Identity Access runtime server connections.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the Verify Identity Access runtime server connections are returned as JSON and can be 
            accessed from the response.json attribute.

        '''
        endpoint = SERVER_CONNECTION_ISAM_RUNTIME + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def delete_runtime(self, uuid):
        '''
        Delete a Verify Identity Access runtime server connection.

        Args:
            uuid (:obj:`str`): The id of the Verify Identity Access runtime connection to remove.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access.

            Success can be checked by examining the response.success boolean attribute.

        '''
        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_ISAM_RUNTIME, uuid)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204
        return response
