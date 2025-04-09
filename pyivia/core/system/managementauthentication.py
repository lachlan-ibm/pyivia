""""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


MANAGEMENT_AUTHENTICATION = "/isam/management_authentication"

logger = logging.getLogger(__name__)


class ManagementAuthentication(object):

    def __init__(self, base_url, username, password):
        super(ManagementAuthentication, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def test(self, username=None, password=None):
        """
        Test authenticate a username/password combination using the configured identity
        provider. THis is only valid for local or LDAP based authentication.

        Args:
            username (:obj:`str`): The username to authenticate with.
            password (:obj:`str`): The password to authenticate with.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()
        data.add_value_string("user", username)
        data.add_value_string("password", password)
        response = self.client.post_json(MANAGEMENT_AUTHENTICATION, data.data)
        response.success = True if response.status_code == 200 else False

        return response


    def update(self, auth_type, ldap_host=None, ldap_port=None, enable_ssl=None, key_database=None, cert_label=None,
               user_attribute=None, group_member_attribute=None, base_dn=None, admin_group_dn=None, anon_bind=None,
               bind_dn=None, bind_password=None, ldap_debug=None, enable_usermapping=None, usermapping_script=None,
               enable_ssh_pubkey_auth=None, ssh_pubkey_auth_attribute=None, oidc_client_id=None, oidc_client_secret=None,
               oidc_discovery_endpoint=None, oidc_enable_pkce=None, oidc_enable_admin_group=None, oidc_group_claim=None,
               oidc_admin_group=None, oidc_user_claim=None, oidc_keystore=None, enable_tokenmapping=None, 
               tokenmapping_script=None):
        """
        Update the management authorization roles configuration

        Args:
            auth_type (:obj:`str`): The type of management authorization to use. valid values are "local", "remote" or "federation".
            ldap_host (:obj:`str`, optional): Specifies the name of the LDAP server. This parameter is required if auth_type is remote.
            ldap_port (`int`, optional): Specifies the port over which to communicate with the LDAP server. This parameter is 
                                        required if auth_type is remote.
            enable_ssl (`bool`, optional): Specifies whether SSL is used when the system communicates with the LDAP server. 
            key_database  (:obj:`str`, optional): Specifies the name of the key database file. This parameter is required if 
                                                "enable_ssl" is set to true and auth_type is remote.
            cert_label (:obj:`str`, optional): Specifies the name of the certificate within the Key database that is used if 
                                                client authentication is requested by the LDAP server.
            user_attribute (:obj:`str`, optional): Specifies the name of the LDAP attribute which holds the supplied authentication 
                                                user name of the user. This parameter is required if auth_type is remote.
            group_member_attribute (:obj:`str`, optional): Specifies the name of the LDAP attribute which is used to hold the members 
                                                of a group. This parameter is required if auth_type is remote.
            base_dn (:obj:`str`, optional): Specifies the base DN which is used to house all administrative users.
            admin_group_dn (:obj:`str`, optional): Specifies the DN of the group to which all administrative users must belong.
            anon_bind (`bool``, optional): Specifies whether the LDAP user registry supports anonymous bind. If set to false, "bind_dn" 
                                            and "bind_password" are required.
            bind_dn (:obj:`str`, optional): Specifies the DN of the user which will be used to bind to the registry. This user must 
                                            have read access to the directory. This parameter is required if anon_bind is false and 
                                            auth_type is remote.
            bind_password (:obj:`str`, optional): Specifies the password which is associated with the bind_dn. This parameter is 
                                            required if anon_bind is false and auth_type is remote.
            ldap_debug (`bool`, optional): Specifies whether the capturing of LDAP debugging information is enabled or not.
            enable_usermapping (`bool`, optional): Specifies whether mapping of the incoming client certificate DN is enabled.
            usermapping_script (:obj:`str`, optional): Specifies the javascript script that will map the incoming client certificate 
                                                        DN. The script will be passed a Map containing the certificate dn, rdns, 
                                                        principal, cert, san and the user_attribute, group_member_attribute and base_dn 
                                                        from this configuration. If not specified a default script is used. Only valid 
                                                        if auth_type is set to remote and enable_usermapping is true.
            enable_ssh_pubkey_auth (`bool`, optional): Specifies whether or not users in the LDAP server can log in via SSH using SSH 
                                                        public key authentication. If this value is not provided, it will default to false.
            ssh_pubkey_auth_attribute (:obj:`str`, optional): Specifies the name of the LDAP attribute which contains a user's public key 
                                                              data. This field is required if SSH public key authentication is enabled.
            oidc_client_id (:obj:`str`, optional): The OIDC Client Identifier. This field is required if auth_type is federation.
            oidc_client_secret (:obj:`str`, optional): The OIDC Client Secret. This field is required if auth_type is federation.
            oidc_discovery_endpoint (:obj:`str`, optional): The OIDC Discovery (well-known) endpoint. This field is required if auth_type 
                                                            is federation.
            oidc_enable_pkce (`bool`, optional): Specifies whether the Public key Code Exchange extension is enforced. This field is required 
                                                if auth_type is federation.
            oidc_enable_admin_group (`bool`, optional): Specifies whether a user must be a member of a particular group to be considered an 
                                                        administrator user. This field is required if auth_type is federation.
            oidc_group_claim (:obj:`str`, optional): The OIDC token claim to use as group membership. This claim can either be a String, or a 
                                                    list of Strings. The default value is "groups".
            oidc_admin_group (:obj:`str`, optional): The name of the group which a user must be a member of to be considered an administrator 
                                                    user. The default value is "adminGroup".
            oidc_user_claim: (:obj:`str`, optional): Specifies the OIDC token claim to use as the username. The default value is "sub".
            oidc_keystore (:obj:`str`, optional): The SSL Truststore to verify connections the the OIDC OP. The default value if "lmi_trust_store".
            enable_tokenmapping (`bool`, optional): Specifies whether custom claim to identity mapping is performed using a JavaScript code fragment.
            tokenmapping_script (:obj:`str`, optional): The custom JavaScript code fragment to map an identity token to a username/group membership. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the management authorization configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        data = DataObject()
        data.add_value_string("type", auth_type)
        data.add_value_string("ldap_host", ldap_host)
        data.add_value_string("ldap_port", ldap_port)
        data.add_value_boolean("ldap_ssl", enable_ssl)
        data.add_value_string("key_database", key_database)
        data.add_value_string("cert_label", cert_label)
        data.add_value_string("user_attribute", user_attribute)
        data.add_value_string("group_member_attribute", group_member_attribute)
        data.add_value_string("base_dn", base_dn)
        data.add_value_string("admin_group_dn", admin_group_dn)
        data.add_value_boolean("anon_bind", anon_bind)
        data.add_value_string("bind_dn", bind_dn)
        data.add_value_string("bind_password", bind_password)
        data.add_value_boolean("ldap_debug", ldap_debug)
        data.add_value_boolean("enable_usermapping", enable_usermapping)
        data.add_value_string("usermapping_script", usermapping_script)
        data.add_value_boolean("enable_ssh_pubkey_auth", enable_ssh_pubkey_auth)
        data.add_value_string("ssh_pubkey_auth_attribute", ssh_pubkey_auth_attribute)
        data.add_value_string("oidc_client_id", oidc_client_id)
        data.add_value_string("oidc_client_secret", oidc_client_secret)
        data.add_value_string("oidc_discovery_endpoint", oidc_discovery_endpoint)
        data.add_value_boolean("oidc_enable_pkce", oidc_enable_pkce)
        data.add_value_boolean("oidc_enable_admin_group", oidc_enable_admin_group)
        data.add_value_string("oidc_group_claim", oidc_group_claim)
        data.add_value_string("oidc_admin_group", oidc_admin_group)
        data.add_value_string("oidc_user_claim", oidc_user_claim)
        data.add_value_string("oidc_keystore", oidc_keystore)
        data.add_value_boolean("enable_tokenmapping", enable_tokenmapping)
        data.add_value_string("tokenmapping_script", tokenmapping_script)
        response = self.client.put_json(MANAGEMENT_AUTHENTICATION, data.data)
        response.success = response.status_code == 200

        return response

    def get(self):
        """
        Get the management authentication configuration

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the management authorization configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(MANAGEMENT_AUTHENTICATION)
        response.success = response.status_code == 200

        return response