"""
@copyright: IBM
"""


from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


EMBEDDED_LDAP_PASSWORD = "/isam/embedded_ldap/change_pwd/v1"
RUNTIME_COMPONENT = "/isam/runtime_components"
UNCONFIGURE_RUNTIME_COMPONENT = RUNTIME_COMPONENT + "/RTE"
FEDERATED_DIRECTORIES = RUNTIME_COMPONENT + "/federated_directories"
RUNTIME_STANZA_FILE_BASE = "/isam/runtime"


class RuntimeComponent(object):

    def __init__(self, base_url, username, password):
        super(RuntimeComponent, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def configure(
            self, ps_mode=None, user_registry=None, admin_password=None,
            ldap_password=None, admin_cert_lifetime=None, ssl_compliance=None,
            ldap_host=None, ldap_port=None, isam_domain=None, ldap_dn=None,
            ldap_suffix=None, ldap_ssl_db=None, ldap_ssl_label=None,
            isam_host=None, isam_port=None):
        """
        Configure the reverse proxy runtime component, including the policy server and user registry.

        Args:
            ps_mode (:obj:`str`): The mode for the policy server. Valid values are local and remote.
            user_registry (:obj:`str`): The type of user registry to be configured against. Valid values are local, ldap
            admin_password (:obj:`str`): The security administrator's password (also known as sec_master).
            ldap_password (:obj:`str`, optional): The password for the DN. If the ps_mode is local and the user registry is remote, this field is required.
            admin_cert_lifetime (:obj:`str`, optional): The lifetime in days for the SSL server certificate. If ps_mode is local, this field is required.
            ssl_compliance (:obj:`str`): Specifies whether SSL is compliant with any additional computer security standard.
            ldap_host (:obj:`str`): The name of the LDAP server.
            ldap_port (:obj:`str`): The port to be used when the system communicates with the LDAP server.
            isam_domain (:obj:`str`): The Security Verify Identity Access domain name. This field is required unless ps_mode is local and user_registry is local.
            ldap_dn (:obj:`str`): The DN that is used when the system contacts the user registry.
            ldap_suffix (:obj:`str`): The LDAP suffix that is used to hold the Security Verify Identity Access secAuthority data.
            ldap_ssl_db (:obj:`str`): The key file (no path information is required) that contains the certificate that 
                                is used to communicate with the user registry. If no keyfile is provided, the SSL is 
                                not used when the system communicates with the user registry.
            ldap_ssl_label (:obj:`str`, optional): The label of the SSL certificate that is used when the system 
                                communicates with the user registry. This option is only valid if the ldap_ssl_db option 
                                is provided.
            isam_host (:obj:`str`): The name of the host that hosts the Security Verify Identity Access policy server.
            isam_port (:obj:`str`, optional): The port over which communication with the Security Verify Identity Access policy 
                                server takes place. If ps_mode is remote, this field is required.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
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
        Get the status of the runtime server.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the rate limiting policy is returned as JSON and can be accessed from
            the response.json attribute

        """
        response = self.client.get_json(RUNTIME_COMPONENT)
        response.success = response.status_code == 200
        return response


    def update_embedded_ldap_password(self, password):
        """
        Change the admin password on the embedded LDAP server.

        Args:
            password (:obj:`str`): The new administrator password.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        data = DataObject()
        data.add_value_string("password", password)

        response = self.client.post_json(EMBEDDED_LDAP_PASSWORD, data.data)
        response.success = response.status_code == 200
        return response


    def create_federated_user_registry(self, _id, hostname=None, port=None, bind_dn=None, bind_pwd=None, 
            ignore_if_down=None, use_ssl=None, client_cert_label=None, suffix=[]):
        """
        Add a federated LDAP server to the user registry for use as basic or full Verify Identity Access users.

        Args:
            _id (:obj:`str`): The identifier of the federated LDAP server.
            hostname (:obj:`str`): The hostname or address of the LDAP server.
            port (:obj:`str`): The port that the LDAP server is listening on.
            bind_dn (:obj:`str`): The Distinguished Name to bind to the LDAP server as to perform admin operations.
            bind_pwd (:obj:`str`): The secret to authenticate as the ``bind_dn`` user.
            ignore_if_down (`bool`, optional): Whether the server will continue to operate using the other configured 
                                               federated registries if this user registry is unavailable.
            use_ssl (`bool`): Whether or not SSL is used to communicate with the directory.
            client_cert_label (:obj:`str`, optional): The client certificate to use when communicating with the 
                                                      directory using SSL. Only valid if ``use_ssl`` is true.
            suffix (:obj:`list` of :obj:`dict`): List of suffixes to use, eg::

                                                                                [
                                                                                 {"id": "dc=ibm,dc=com"},
                                                                                 {"id": "o=ibm"}
                                                                                ]

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        data = DataObject()
        data.add_value_string("id", _id)
        data.add_value_string("hostname", hostname)
        data.add_value("port", port)
        data.add_value_string("bind_dn", bind_dn)
        data.add_value_string("bind_pwd", bind_pwd)
        data.add_value_boolean("ignore_if_down", ignore_if_down)
        data.add_value_boolean("use_ssl", use_ssl)
        data.add_value_string("client_cert_label", client_cert_label)
        data.add_value("suffix", suffix)

        response = self.client.post_json(FEDERATED_DIRECTORIES + "/v1", data.data)
        response.success = response.status_code == 200

        return response


    def delete_federated_user_registry(self, _id):
        """
        Remove a configured federated user registry

        Args:
            _id (:obj:`str`): The identifier of the federated user registry to remove.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        url = FEDERATED_DIRECTORIES + "/{}/v1".format(_id)
        response = self.client.delete_json(url)
        response.success = response.status_code == 204

        return response


    def create_configuration_file_entry(self, resource=None, stanza=None, entries=None):
        """
        Create a new stanza or entry in a runtime component configuration file.

        Args:
            resource (:obj:`str`): The configuration file to modify. For example: ldap.conf, pd.conf, instance.conf
            stanza (:obj:`str`): The name of the resource stanza entry.
            entries (:obj:`list` of :obj:`list`, optional): Entry name and value in the format of key value pairs. If 
                                                            this property is not supplied then the stanza is created
                                                            instead. Format of list is::

                                                                                        [
                                                                                          ["entryName", "entryValue"],
                                                                                          ["anotherName", "theValue"]
                                                                                        ]

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        url = RUNTIME_STANZA_FILE_BASE + "/{}/configuration/stanza/{}".format(resource, stanza)
        data = DataObject()
        if entries:
            data.add_value_not_empty("entries", entries)
            url += "/entry_name"

        response = self.client.post_json(url, data.data)
        response.success = response.status_code == 200

        return response


    def update_configuration_file_entry(self, resource=None, stanza=None, entries=None):
        """
        Update a stanza entry in a runtime component configuration file.

        Args:
            resource (:obj:`str`): The configuration file to modify. For example: ldap.conf, pd.conf, instance.conf
            stanza (:obj:`str`): The name of the resource stanza entry.
            entries (:obj:`list` of :obj:`list`): Entry name and value in the format of key value pairs. If 
                                                            this property is not supplied then the stanza is created
                                                            instead. Format of list is::

                                                                                        [
                                                                                          ["entryName", "entryValue"],
                                                                                          ["anotherName", "theValue"]
                                                                                        ]

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        url = RUNTIME_STANZA_FILE_BASE + "/{}/configuration/stanza/{}/entry_name".format(resource, stanza)
        data = DataObject()
        data.add_value_not_empty("entries", entries)
        response = self.client.put_json(url, data.data)
        response.success = response.status_code == 200

        return response


    def delete_configuration_file_entry(self, resource=None, stanza=None, entry=None, value=None):
        """
        Delete a stanza or entry in a runtime component configuration file.

        Args:
            resource (:obj:`str`): The configuration file to modify. For example: ldap.conf, pd.conf, instance.conf
            stanza (:obj:`str`): The name of the resource stanza entry.
            entry (:obj:`str`, optional): The entry name to be removed. If not supplied then the entire stanza is removed.
            value (:obj:`str`, optional): The entry value to be removed. This must be set if the ``entry`` property is
                                          supplied.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        response = None
        url = RUNTIME_STANZA_FILE_BASE + "/{}/configuration/stanza/{}".format(resource, stanza)
        if entry:
            url += "/entry_name/{}/value/{}".format(entry, value)

        response = self.client.delete_json(url)
        response.success = response.status_code == 200

        return response


class RuntimeComponent10000(RuntimeComponent):
    
    def configure(
            self, ps_mode=None, user_registry=None, admin_password=None,
            ldap_password=None, admin_cert_lifetime=None, ssl_compliance=None,
            ldap_host=None, ldap_port=None, isam_domain=None, ldap_dn=None,
            ldap_suffix=None, ldap_ssl_db=None, ldap_ssl_label=None,
            isam_host=None, isam_port=None, clean_ldap=None):
        """
        Configure the reverse proxy runtime component, including the policy server and user registry.

        Args:
            ps_mode (:obj:`str`): The mode for the policy server. Valid values are local and remote.
            user_registry (:obj:`str`): The type of user registry to be configured against. Valid values are local, ldap
            admin_password (:obj:`str`): The security administrator's password (also known as sec_master).
            ldap_password (:obj:`str`, optional): The password for the DN. If the ps_mode is local and the user registry is remote, this field is required.
            admin_cert_lifetime (:obj:`str`, optional): The lifetime in days for the SSL server certificate. If ps_mode is local, this field is required.
            ssl_compliance (:obj:`str`): Specifies whether SSL is compliant with any additional computer security standard.
            ldap_host (:obj:`str`): The name of the LDAP server.
            ldap_port (:obj:`str`): The port to be used when the system communicates with the LDAP server.
            isam_domain (:obj:`str`): The Security Verify Identity Access domain name. This field is required unless ps_mode is local and user_registry is local.
            ldap_dn (:obj:`str`): The DN that is used when the system contacts the user registry.
            ldap_suffix (:obj:`str`): The LDAP suffix that is used to hold the Security Verify Identity Access secAuthority data.
            ldap_ssl_db (:obj:`str`): The key file (no path information is required) that contains the certificate that 
                                is used to communicate with the user registry. If no keyfile is provided, the SSL is 
                                not used when the system communicates with the user registry.
            ldap_ssl_label (:obj:`str`, optional): The label of the SSL certificate that is used when the system 
                                communicates with the user registry. This option is only valid if the ldap_ssl_db option 
                                is provided.
            isam_host (:obj:`str`): The name of the host that hosts the Verify Identity Access policy server.
            isam_port (:obj:`str`, optional): The port over which communication with the Verify Identity Access policy 
                                server takes place. If ps_mode is remote, this field is required.
            clean_ldap (`bool`, optional): Whether any existing data within the LDAP server should be cleaned prior 
                                to the configuration. Required if the user registry is local.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
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


    def unconfigure(self, operation="unconfigure", ldap_dn=None, ldap_pwd=None, clean=False, force=False):
        """
        Unconfigure the runtime component. This is only possible if there are no WebSEAL reverse proxy instances configured.

        Args:
            ldap_dn (:obj:`str`): The DN that is used when the system contacts the user registry.
            ldap_password (:obj:`str`, optional): The password for the DN.
            clean (`bool`, optional): Whether the unconfigure operation removes all Verify Identity Access domain, user, and 
                            group information.
            force (`bool`, optional): This option is used to force the unconfiguration if it is failing.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        data = DataObject()
        data.add_value_string("operation", operation)
        data.add_value_string("ldap_dn", ldap_dn)
        data.add_value_string("ldap_pwd", ldap_pwd)
        data.add_value_string("clean", clean)
        data.add_value_string("force", force)

        response = self.client.post_json(UNCONFIGURE_RUNTIME_COMPONENT, data.data)

        response.success = response.status_code == 200

        return response
