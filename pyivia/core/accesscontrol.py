"""
@copyright: IBM
"""

from .access.accesscontrol import AccessControl as AC9000
from .access.accesscontrol import AccessControl9030 as AC9030
from .access.accesscontrol import AccessControl10000 as AC10000
from .access.advancedconfig import AdvancedConfig
from .access.apiprotection import APIProtection, APIProtection9040, APIProtection10030
from .access.attributes import Attributes
from .access.authentication import Authentication, Authentication9021
from .access.mmfaconfig import MMFAConfig, MMFAConfig9021
from .access.pushnotification import PushNotification, PushNotification9021
from .access.riskprofiles import RiskProfiles
from .access.runtimeparameters import RuntimeParameters
from .access.scimconfig import SCIMConfig, SCIMConfig9050
from .access.serverconnections import ServerConnections, ServerConnections9050
from .access.templatefiles import TemplateFiles
from .access.userregistry import UserRegistry, UserRegistry10020
from .access.mappingrules import MappingRules
from .access.fido2config import FIDO2Config, FIDO2Config10050
from .access.fido2registrations import FIDO2Registrations
from .access.pip import PIP

class AccessControl(object):
    '''
    Object used to managed Advanced Access Control endpoints. Available modules are:

    :var access_control: Create and manage :ref:`Access Control` policies.
    :var advanced_config: Manage :ref:`Advanced Configuration` parameters.
    :var api_protection: Create and manage OIDC :ref:`API Protection` definitions and clients.
    :var attributes: Create and manage Risk Based Access :ref:`Attribute <Attributes>` mappings.
    :var authentication: Create and manage :ref:`Authentication` policies and mechanisms.
    :var fido2_config: Create and manage :ref:`FIDO2 Configuration` including metadata and mediators.
    :var fido2_registrations: Manage :ref:`FIDO2 Registrations` for runtime users.
    :var mapping_rules: Create and manage JavaScript :ref:`Mapping Rules` used for customized authentication.
    :var mmfa_config: Configure :ref:`Mobile Multi-Factor Authentication` for Verify Access.
    :var push_notifications: Configure and manage :ref:`Push Notification Providers`.
    :var risk_profiles: Create and manage Risk Based Access :ref:`Risk Profiles`.
    :var runtime_parameters: Manage :ref:`Runtime Parameters` of the Liberty runtime server.
    :var scim_config: Create and manage :ref:`SCIM<System for Cross-Domain Identity Management (SCIM) Configuration>` attribute mapping.
    :var server_connections: Create :ref:`Server Connections` to external service providers.
    :var template_files: Create and manage HTML and JSON :ref:`Template Files`.
    :var user_registry: Manage :ref:`user authentication<User Registry>` to the Liberty runtime server.
    :var pip: Manage :ref:`policy information points<Policy Information Points>`.
    '''

class AccessControl9020(object):

    def __init__(self, base_url, username, password):
        super(AccessControl9020, self).__init__()
        self.access_control = AC9000(base_url, username, password)
        self.advanced_config = AdvancedConfig(base_url, username, password)
        self.api_protection = APIProtection(base_url, username, password)
        self.attributes = Attributes(base_url, username, password)
        self.authentication = Authentication(base_url, username, password)
        self.mmfa_config = MMFAConfig(base_url, username, password)
        self.push_notification = PushNotification(base_url, username, password)
        self.risk_profiles = RiskProfiles(base_url, username, password)
        self.runtime_parameters = RuntimeParameters(
            base_url, username, password)
        self.scim_config = SCIMConfig(base_url, username, password)
        self.server_connections = ServerConnections(
            base_url, username, password)
        self.template_files = TemplateFiles(base_url, username, password)
        self.user_registry = UserRegistry(base_url, username, password)
        self.mapping_rules = MappingRules(base_url, username, password)
        self.pip = PIP(base_url, username, password)


class AccessControl9021(AccessControl9020):

    def __init__(self, base_url, username, password):
        super(AccessControl9021, self).__init__(base_url, username, password)
        self.mmfa_config = MMFAConfig9021(base_url, username, password)
        self.push_notification = PushNotification9021(base_url, username, password)
        self.authentication = Authentication9021(base_url, username, password)


class AccessControl9030(AccessControl9021):

    def __init__(self, base_url, username, password):
        super(AccessControl9030, self).__init__(base_url, username, password)
        self.access_control = AC9030(base_url, username, password)


class AccessControl9040(AccessControl9030):

    def __init__(self, base_url, username, password):
        super(AccessControl9040, self).__init__(base_url, username, password)
        self.api_protection = APIProtection9040(base_url, username, password)

class AccessControl9050(AccessControl9040):

    def __init__(self, base_url, username, password):
        super(AccessControl9050, self).__init__(base_url, username, password)
        self.server_connections = ServerConnections9050(base_url, username, password)
        self.scim_config = SCIMConfig9050(base_url, username, password)

class AccessControl9060(AccessControl9050):

    def __init__(self, base_url, username, password):
        super(AccessControl9060, self).__init__(base_url, username, password)


class AccessControl9070(AccessControl9060):

    def __init__(self, base_url, username, password):
        super(AccessControl9070, self).__init__(base_url, username, password)
        self.fido2_config = FIDO2Config(base_url, username, password)
        self.fido2_registrations = FIDO2Registrations(base_url, username, password)


class AccessControl9071(AccessControl9070):

    def __init__(self, base_url, username, password):
        super(AccessControl9071, self).__init__(base_url, username, password)


class AccessControl9072(AccessControl9071):

    def __init__(self, base_url, username, password):
              super(AccessControl9072, self).__init__(base_url, username, password)
              self.fido2_config = FIDO2Config(base_url, username, password)


class AccessControl9073(AccessControl9072):

    def __init__(self, base_url, username, password):
              super(AccessControl9073, self).__init__(base_url, username, password)
              self.fido2_config = FIDO2Config(base_url, username, password)


class AccessControl9080(AccessControl9073):

    def __init__(self, base_url, username, password):
        super(AccessControl9080, self).__init__(base_url, username, password)


class AccessControl10000(AccessControl9080):

    def __init__(self, base_url, username, password):
        super(AccessControl10000, self).__init__(base_url, username, password)


class AccessControl10010(AccessControl10000):

    def __init__(self, base_url, username, password):
        super(AccessControl10010, self).__init__(base_url, username, password)
        self.access_control = AC10000(base_url, username, password)


class AccessControl10020(AccessControl10010):

    def __init__(self, base_url, username, password):
        super(AccessControl10020, self).__init__(base_url, username, password)
        self.user_registry = UserRegistry10020(base_url, username, password)


class AccessControl10030(AccessControl10020):

    def __init__(self, base_url, username, password):
        super(AccessControl10030, self).__init__(base_url, username, password)
        self.api_protection = APIProtection10030(base_url, username, password)


class AccessControl10031(AccessControl10030):

    def __init__(self, base_url, username, password):
        super(AccessControl10031, self).__init__(base_url, username, password)

class AccessControl10040(AccessControl10031):

    def __init__(self, base_url, username, password):
        super(AccessControl10040, self).__init__(base_url, username, password)

class AccessControl10050(AccessControl10040):

    def __init__(self, base_url, username, password):
        super(AccessControl10050, self).__init__(base_url, username, password)
        self.fido2_config = FIDO2Config10050(base_url, username, password)


class AccessControl10060(AccessControl10050):

    def __init__(self, base_url, username, password):
        super(AccessControl10060, self).__init__(base_url, username, password)

class AccessControl10070(AccessControl10060):

    def __init__(self, base_url, username, password):
        super(AccessControl10070, self).__init__(base_url, username, password)

class AccessControl10080(AccessControl10070):

    def __init__(self, base_url, username, password):
        super(AccessControl10080, self).__init__(base_url, username, password)

class AccessControl11000(AccessControl10080):

    def __init__(self, base_url, username, password):
        super(AccessControl11000, self).__init__(base_url, username, password)

class AccessControl11010(AccessControl11000):

    def __init__(self, base_url, username, password):
        super(AccessControl11010, self).__init__(base_url, username, password)

class AccessControl11020(AccessControl11010):

    def __init__(self, base_url, username, password):
        super(AccessControl11020, self).__init__(base_url, username, password)
