"""
@copyright: IBM
"""

from .access.accesscontrol import AccessControl
from .access.accesscontrol import AccessControl9030
from .access.accesscontrol import AccessControl10000
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

class AdvancedAccessControl(object):
    '''
    Object used to managed Advanced Access Control endpoints.

    '''

    access_control: AccessControl
    'Create and manage :ref:`Access Control` policies.'
    advanced_config: AdvancedConfig
    'Manage :ref:`Advanced Configuration` parameters.'
    api_protection: APIProtection
    'Create and manage OIDC :ref:`API Protection` definitions and clients.'
    attributes: Attributes
    'Create and manage Risk Based Access :ref:`Attribute <Attributes>` mappings.'
    authentication: Authentication
    'Create and manage :ref:`Authentication` policies and mechanisms.'
    fido2_config: FIDO2Config
    'Create and manage :ref:`FIDO2 Configuration` including metadata and mediators.'
    fido2_registrations: FIDO2Registrations
    'Manage :ref:`FIDO2 Registrations` for runtime users.'
    mapping_rules: MappingRules
    'Create and manage JavaScript :ref:`Mapping Rules` used for customized authentication.'
    mmfa_config: MMFAConfig
    'Configure :ref:`Mobile Multi-Factor Authentication` for Verify Access.'
    push_notifications: PushNotification
    'Configure and manage :ref:`Push Notification Providers`.'
    risk_profiles: RiskProfiles
    'Create and manage Risk Based Access :ref:`Risk Profiles`.'
    runtime_parameters: RuntimeParameters
    'Manage :ref:`Runtime Parameters` of the Liberty runtime server.'
    scim_config: SCIMConfig
    'Create and manage :ref:`SCIM<System for Cross-Domain Identity Management (SCIM) Configuration>` attribute mapping.'
    server_connections: ServerConnections
    'Create :ref:`Server Connections` to external service providers.'
    template_files: TemplateFiles
    'Create and manage HTML and JSON :ref:`Template Files`.'
    user_registry: UserRegistry
    'Manage :ref:`user authentication<User Registry>` to the Liberty runtime server.'
    pip: PIP
    'Manage :ref:`policy information points<Policy Information Points>`.'

class AdvancedAccessControl9020(object):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl9020, self).__init__()
        self.access_control = AccessControl(base_url, username, password)
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


class AdvancedAccessControl9021(AdvancedAccessControl9020):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl9021, self).__init__(base_url, username, password)
        self.mmfa_config = MMFAConfig9021(base_url, username, password)
        self.push_notification = PushNotification9021(base_url, username, password)
        self.authentication = Authentication9021(base_url, username, password)


class AdvancedAccessControl9030(AdvancedAccessControl9021):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl9030, self).__init__(base_url, username, password)
        self.access_control = AccessControl9030(base_url, username, password)


class AdvancedAccessControl9040(AdvancedAccessControl9030):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl9040, self).__init__(base_url, username, password)
        self.api_protection = APIProtection9040(base_url, username, password)

class AdvancedAccessControl9050(AdvancedAccessControl9040):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl9050, self).__init__(base_url, username, password)
        self.server_connections = ServerConnections9050(base_url, username, password)
        self.scim_config = SCIMConfig9050(base_url, username, password)

class AdvancedAccessControl9060(AdvancedAccessControl9050):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl9060, self).__init__(base_url, username, password)


class AdvancedAccessControl9070(AdvancedAccessControl9060):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl9070, self).__init__(base_url, username, password)
        self.fido2_config = FIDO2Config(base_url, username, password)
        self.fido2_registrations = FIDO2Registrations(base_url, username, password)


class AdvancedAccessControl9071(AdvancedAccessControl9070):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl9071, self).__init__(base_url, username, password)


class AdvancedAccessControl9072(AdvancedAccessControl9071):

    def __init__(self, base_url, username, password):
              super(AdvancedAccessControl9072, self).__init__(base_url, username, password)
              self.fido2_config = FIDO2Config(base_url, username, password)


class AdvancedAccessControl9073(AdvancedAccessControl9072):

    def __init__(self, base_url, username, password):
              super(AdvancedAccessControl9073, self).__init__(base_url, username, password)
              self.fido2_config = FIDO2Config(base_url, username, password)


class AdvancedAccessControl9080(AdvancedAccessControl9073):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl9080, self).__init__(base_url, username, password)


class AdvancedAccessControl10000(AdvancedAccessControl9080):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl10000, self).__init__(base_url, username, password)


class AdvancedAccessControl10010(AdvancedAccessControl10000):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl10010, self).__init__(base_url, username, password)
        self.access_control = AccessControl10000(base_url, username, password)


class AdvancedAccessControl10020(AdvancedAccessControl10010):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl10020, self).__init__(base_url, username, password)
        self.user_registry = UserRegistry10020(base_url, username, password)


class AdvancedAccessControl10030(AdvancedAccessControl10020):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl10030, self).__init__(base_url, username, password)
        self.api_protection = APIProtection10030(base_url, username, password)


class AdvancedAccessControl10031(AdvancedAccessControl10030):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl10031, self).__init__(base_url, username, password)

class AdvancedAccessControl10040(AdvancedAccessControl10031):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl10040, self).__init__(base_url, username, password)

class AdvancedAccessControl10050(AdvancedAccessControl10040):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl10050, self).__init__(base_url, username, password)
        self.fido2_config = FIDO2Config10050(base_url, username, password)


class AdvancedAccessControl10060(AdvancedAccessControl10050):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl10060, self).__init__(base_url, username, password)

class AdvancedAccessControl10070(AdvancedAccessControl10060):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl10070, self).__init__(base_url, username, password)

class AdvancedAccessControl10080(AdvancedAccessControl10070):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl10080, self).__init__(base_url, username, password)

class AdvancedAccessControl11000(AdvancedAccessControl10080):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl11000, self).__init__(base_url, username, password)

class AdvancedAccessControl11010(AdvancedAccessControl11000):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl11010, self).__init__(base_url, username, password)

class AdvancedAccessControl11020(AdvancedAccessControl11010):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl11020, self).__init__(base_url, username, password)

class AdvancedAccessControl11030(AdvancedAccessControl11020):

    def __init__(self, base_url, username, password):
        super(AdvancedAccessControl11030, self).__init__(base_url, username, password)
