"""
@copyright: IBM
"""

import importlib
import re

from pyivia.util.restclient import RESTClient


DEVELOPMENT_VERSION = "IBM Verify Identity Access Development"
VERSIONS = {
    DEVELOPMENT_VERSION: "11020",
    "IBM Verify Identity Access 11.0.2.0": "11020",
    "IBM Verify Identity Access 11.0.1.0": "11010",
    "IBM Verify Identity Access 11.0.0.0": "11000",
    "IBM Security Verify Access 11.0.0.0": "11000",
    "IBM Security Verify Access 10.0.9.0": "11000",
    "IBM Security Verify Access 10.0.8.0": "10080",
    "IBM Security Verify Access 10.0.7.0": "10070",
    "IBM Security Verify Access 10.0.6.0_b1": "10060",
    "IBM Security Verify Access 10.0.6.0": "10060",
    "IBM Security Verify Access 10.0.5.0": "10050",
    "IBM Security Verify Access 10.0.4.0": "10040",
    "IBM Security Verify Access 10.0.3.1": "10031",
    "IBM Security Verify Access 10.0.3.0": "10030",
    "IBM Security Verify Access 10.0.2.0": "10020",
    "IBM Security Verify Access 10.0.1.0": "10010",
    "IBM Security Verify Access 10.0.1.0_b1": "10010",
    "IBM Security Verify Access 10.0.0.0": "10000",
    "IBM Security Access Manager 10.0.0.0_b1": "10000",
    "IBM Security Access Manager 10.0.0.0": "10000",
    "IBM Security Access Manager 9.0.8.0": "9080",
    "IBM Security Access Manager 9.0.7.3": "9073",
    "IBM Security Access Manager 9.0.7.2": "9072",
    "IBM Security Access Manager 9.0.7.1": "9071",
    "IBM Security Access Manager 9.0.7.0": "9070",
    "IBM Security Access Manager 9.0.6.0_b2": "9060",
    "IBM Security Access Manager 9.0.6.0_b1": "9060",
    "IBM Security Access Manager 9.0.6.0": "9060",
    "IBM Security Access Manager 9.0.5.0": "9050",
    "IBM Security Access Manager 9.0.4.0": "9040",
    "IBM Security Access Manager 9.0.3.0": "9030",
    "IBM Security Access Manager 9.0.2.1": "9021",
    "IBM Security Access Manager 9.0.2.0": "9020"
}


class AuthenticationError(Exception):
    pass


class Factory(object):
    """
    The Factory class is used to initialise a singleton "appliance" object which can be use for all subsequent API 
    requests.

    The factory has getter methods for the three modules: WebSEAL, Advanced Access Control; and Federation. It also 
    getter methods for the system and diagnostics API.

    Finally this class has helper methods to determine if the IBM Verify Identity Access deployment is an appliance
    or container deployment model.

    This project supports both basic and API token authorization. 
    If both username and password are provided, the rest client will use Basic
    authorization, if just a password is supplied, then Bearer authorization
    is supplied.
    """

    def __init__(self, base_url, username, password):
        super(Factory, self).__init__()
        self._base_url = base_url
        self._username = username
        self._password = password
        self._version = None
        self._deployment_model = "Appliance"

        self._discover_version_and_deployment()
        self._get_version()

    def get_federation(self):
        '''
        Return manager of Federation endpoint

        Returns:
            versioned :ref:`federation` object.
        '''
        class_name = "Federation" + self._get_version()
        module_name = "pyivia.core.federationsettings"
        return self._class_loader(module_name, class_name)

    def get_access_control(self):
        '''
        Return manager of AAC endpoint

        Returns:
            versioned :ref:`access_control` object.
        '''
        class_name = "AccessControl" + self._get_version()
        module_name = "pyivia.core.accesscontrol"
        return self._class_loader(module_name, class_name)

    def get_analysis_diagnostics(self):
        '''
        Return manager of diagnostic endpoint
        
        Returns:
            versioned :ref:`analysis_diagnostics` object.
        '''
        class_name = "AnalysisDiagnostics" + self._get_version()
        module_name = "pyivia.core.analysisdiagnostics"
        return self._class_loader(module_name, class_name)

    def get_system_settings(self):
        '''
        Return manager of system settings endpoint

        Returns:
            versioned :ref:`system_settings` object.
        '''
        class_name = "SystemSettings" + self._get_version()
        module_name = "pyivia.core.systemsettings"
        return self._class_loader(module_name, class_name)

    def get_version(self):
        '''
        Return the Verify Identity Access version
        '''
        return self._version

    def get_web_settings(self):
        '''
        Return manager of Web Reverse Proxy endpoints

        Returns:
        versioned :ref:`web_settings` object.
        '''
        class_name = "WebSettings" + self._get_version()
        module_name = "pyivia.core.websettings"
        return self._class_loader(module_name, class_name)

    def get_deployment_utility(self):
        '''
        Return manager of Web Reverse Proxy endpoints
        '''
        class_name = "WebSettings" + self._get_version()
        module_name = "pyivia.core.websettings"
        return self._class_loader(module_name, class_name)

    def set_password(self, password):
        '''
        Update the password used to authenticate to Verify Identity Access administrator endpoints
        '''
        self._password = password

    def _class_loader(self, module_name, class_name):
        Klass = getattr(importlib.import_module(module_name), class_name)
        return Klass(self._base_url, self._username, self._password)

    def is_docker(self):
        '''
        Return true if detected deployment is running in a container
        '''
        return self._deployment_model == "Docker"

    def get_deployment_model(self):
        '''
        Get the deployment model detected by Verify Identity Access.
        Appliance or Docker
        '''
        return self._deployment_model

    def _discover_version_and_deployment(self):
        client = RESTClient(self._base_url, self._username, self._password)

        response = client.get_json("/core/sys/versions")
        if response.status_code == 200 and isinstance(response.json, dict):
            self._version          = "{0} {1}".format(response.json.get("product_description"), response.json.get("firmware_version"))
            self._deployment_model = response.json.get("deployment_model")
        elif response.status_code == 403:
            raise AuthenticationError("Authentication failed.")
        else:
            response = client.get_json("/firmware_settings")
            if response.status_code == 200 and isinstance(response.json, dict):
                for entry in response.json:
                    if entry.get("active", False):
                        if entry.get("name", "").endswith("_nonproduction_dev"):
                            self._version = DEVELOPMENT_VERSION
                        else:
                            self._version = entry.get("firmware_version")
            elif response.status_code == 403:
                raise AuthenticationError("Authentication failed.")

        if not self._version:
            raise Exception("Failed to retrieve the ISAM firmware version.")

    def __fuzzy_match_minor_version(self):
        # If no exact match, try matching first three version digits
        # Extract version number from the full version string
        # Format: "Product Name X.Y.Z.W" -> extract "X.Y.Z"
        if not self._version:
            return None

        version_match = re.search(r'(\d+\.\d+\.\d+)\.\d+', self._version)
        if version_match:
            # Get the first three digits (e.g., "11.0.1" from "11.0.1.1")
            base_version = version_match.group(1)
            
            # Search for a matching version in VERSIONS that starts with base_version
            for version_key in VERSIONS:
                # Extract version number from the key
                key_version_match = re.search(r'(\d+\.\d+\.\d+)', version_key)
                if key_version_match:
                    key_base_version = key_version_match.group(1)
                    # Check if the base versions match and the product name matches
                    if key_base_version == base_version:
                        # Extract product name from both versions
                        version_product = self._version.rsplit(' ', 1)[0] if ' ' in self._version else ''
                        key_product = version_key.rsplit(' ', 1)[0] if ' ' in version_key else ''
                        
                        if version_product == key_product:
                            return version_key
        return None

    def _get_version(self):
        # First try exact match
        if self._version in VERSIONS:
            return str(VERSIONS.get(self._version))
        
        # Try fuzzy match on first three version digits
        matched_version = self.__fuzzy_match_minor_version()
        if matched_version:
            return str(VERSIONS.get(matched_version))
        
        raise Exception(str(self._version) + " is not supported.")
