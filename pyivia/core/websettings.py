"""
@copyright: IBM
"""

from .web.dscadmin import DSCAdmin
from .web.policyadmin import PolicyAdmin
from .web.reverseproxy import ReverseProxy, ReverseProxy9040, ReverseProxy10020
from .web.runtimecomponent import RuntimeComponent, RuntimeComponent10000
from .web.httptransform import HTTPTransform
from .web.fsso import FSSO
from .web.clientcertmapping import ClientCertMapping
from .web.junctionmapping import JunctionMapping
from .web.urlmapping import URLMapping
from .web.usermapping import UserMapping
from .web.kerberos import Kerberos
from .web.passwordstrength import PasswordStrength
from .web.rsa import RSA
from .web.api_access_control import APIAccessControl
from .web.runtimecomponent import RuntimeComponent
from .web.ratelimit import RateLimit

class WebSettings(object):
    '''
    Object used to manage WebSEAL configuration endpoints

    :var dsc_admin: Manage the :ref:`Distributed Session Cache`.
    :var policy_administration: Manage the :ref:`policy server<Policy Administration>`.
    :var reverse_proxy: Create and manage :ref:`WebSEAL<Reverse Proxy>` instances.
    :var runtime_component: Create and manage the :ref:`user registry and policy server<Runtime Component>` configuration files.
    :var http_transform: Create and manage XSLT and LUA HTTP :ref:`transformation rules<HTTP Transformations>`.
    :var fsso: Create and manage :ref:`Form Single Sign-On` rules.
    :var client_cert_mapping: Create :ref:`Client X509 Certificate<Client Certificate Mapping>` authentication mapping rules.
    :var jct_mapping: Create :ref:`Junction Mapping` rules.
    :var url_mapping: Create :ref:`URL Mapping` rules.
    :var user_mapping: Create :ref:`User Mapping` rules.
    :var kerberos: Create and manage :ref:`KERBEROS<Kerberos>` federated user registries.
    :var password_strength: Create :ref:`Password Strength Rules`.
    :var rsa: Configure :ref:`RSA OTP<RSA Security Token>` integration
    :var api_access_control: Create and manage :ref:`API Gateway<API Access Control>` integrations.
    :var ratelimit: Create :ref:`Rate Limiting` rules.
    '''

class WebSettings9020(object):

    def __init__(self, base_url, username, password):
        super(WebSettings9020, self).__init__()
        self.dsc_admin = DSCAdmin(base_url, username, password)
        self.policy_administration = PolicyAdmin(base_url, username, password)
        self.reverse_proxy = ReverseProxy(base_url, username, password)
        self.runtime_component = RuntimeComponent(base_url, username, password)


class WebSettings9021(WebSettings9020):

    def __init__(self, base_url, username, password):
        super(WebSettings9021, self).__init__(base_url, username, password)


class WebSettings9030(WebSettings9021):

    def __init__(self, base_url, username, password):
        super(WebSettings9030, self).__init__(base_url, username, password)


class WebSettings9040(WebSettings9030):

    def __init__(self, base_url, username, password):
        super(WebSettings9040, self).__init__(base_url, username, password)
        self.reverse_proxy = ReverseProxy9040(base_url, username, password)


class WebSettings9050(WebSettings9040):

    def __init__(self, base_url, username, password):
        super(WebSettings9050, self).__init__(base_url, username, password)


class WebSettings9060(WebSettings9050):

    def __init__(self, base_url, username, password):
        super(WebSettings9060, self).__init__(base_url, username, password)


class WebSettings9070(WebSettings9060):

    def __init__(self, base_url, username, password):
        super(WebSettings9070, self).__init__(base_url, username, password)


class WebSettings9071(WebSettings9070):

    def __init__(self, base_url, username, password):
        super(WebSettings9071, self).__init__(base_url, username, password)


class WebSettings9080(WebSettings9071):

    def __init__(self, base_url, username, password):
        super(WebSettings9080, self).__init__(base_url, username, password)


class WebSettings10000(WebSettings9080):

    def __init__(self, base_url, username, password):
        super(WebSettings10000, self).__init__(base_url, username, password)
        self.runtime_component = RuntimeComponent10000(base_url, username, password)
        self.http_transform = HTTPTransform(base_url, username, password)
        self.fsso = FSSO(base_url, username, password)
        self.client_cert_mapping = ClientCertMapping(base_url, username, password)
        self.jct_mapping = JunctionMapping (base_url, username, password)
        self.url_mapping = URLMapping(base_url, username, password)
        self.user_mapping = UserMapping(base_url, username, password)
        self.kerberos = Kerberos(base_url, username, password)
        self.password_strength = PasswordStrength(base_url, username, password)
        self.rsa = RSA(base_url, username, password)
        self.api_access_control = APIAccessControl(base_url, username, password)
        self.ratelimit = RateLimit(base_url, username, password)


class WebSettings10010(WebSettings10000):

    def __init__(self, base_url, username, password):
        super(WebSettings10010, self).__init__(base_url, username, password)


class WebSettings10020(WebSettings10010):

    def __init__(self, base_url, username, password):
        super(WebSettings10020, self).__init__(base_url, username, password)
        self.reverse_proxy = ReverseProxy10020(base_url, username, password)


class WebSettings10030(WebSettings10020):

    def __init__(self, base_url, username, password):
        super(WebSettings10030, self).__init__(base_url, username, password)


class WebSettings10031(WebSettings10030):

    def __init__(self, base_url, username, password):
        super(WebSettings10031, self).__init__(base_url, username, password)


class WebSettings10040(WebSettings10031):

    def __init__(self, base_url, username, password):
        super(WebSettings10040, self).__init__(base_url, username, password)


class WebSettings10050(WebSettings10040):

    def __init__(self, base_url, username, password):
        super(WebSettings10050, self).__init__(base_url, username, password)

class WebSettings10060(WebSettings10050):

    def __init__(self, base_url, username, password):
        super(WebSettings10060, self).__init__(base_url, username, password)

class WebSettings10070(WebSettings10060):

    def __init__(self, base_url, username, password):
        super(WebSettings10070, self).__init__(base_url, username, password)

class WebSettings10080(WebSettings10070):

    def __init__(self, base_url, username, password):
        super(WebSettings10080, self).__init__(base_url, username, password)

class WebSettings11000(WebSettings10080):

    def __init__(self, base_url, username, password):
        super(WebSettings11000, self).__init__(base_url, username, password)

class WebSettings11010(WebSettings11000):

    def __init__(self, base_url, username, password):
        super(WebSettings11010, self).__init__(base_url, username, password)

class WebSettings11020(WebSettings11010):

    def __init__(self, base_url, username, password):
        super(WebSettings11020, self).__init__(base_url, username, password)
