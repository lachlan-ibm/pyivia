"""
@copyright: IBM
"""

from .web.dscadmin import DSCAdmin
from .web.policyadmin import PolicyAdmin
from .web.reverseproxy import ReverseProxy, ReverseProxy9040, ReverseProxy10020
from .web.runtimecomponent import RuntimeComponent, RuntimeComponent10000
from .web.httptransform import HTTP_Transform
from .web.fsso import FSSO
from .web.clientcertmapping import ClientCertMapping
from .web.junctionmapping import JunctionMapping
from .web.urlmapping import URLMapping
from .web.usermapping import UserMapping
from .web.kerberos import Kerberos
from .web.passwordstrength import PasswordStrength
from .web.rsa import RSA
from .web.api_access_control import APIAccessControl

class WebSettings9020(object):
    '''
    Object used to manage WebSEAL configuration endpoints

    :var dsc_admin: Manage the Distributed Session Cache
    :var policy_administration: Manage the policy server
    :var reverse_proxy: Create and manage WebSEAL instances
    :var runtime_component: Create and manage the user registry and policy server configuration files
    '''

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


class WebSettings9072(WebSettings9071):

    def __init__(self, base_url, username, password):
            super(WebSettings9072, self).__init__(base_url, username, password)


class WebSettings9073(WebSettings9072):

    def __init__(self, base_url, username, password):
            super(WebSettings9073, self).__init__(base_url, username, password)


class WebSettings9080(WebSettings9073):

    def __init__(self, base_url, username, password):
            super(WebSettings9080, self).__init__(base_url, username, password)


class WebSettings10000(WebSettings9080):

    def __init__(self, base_url, username, password):
            super(WebSettings10000, self).__init__(base_url, username, password)
            self.runtime_component = RuntimeComponent10000(base_url, username, password)
            self.http_transform = HTTP_Transform(base_url, username, password)
            self.fsso = FSSO(base_url, username, password)
            self.client_cert_mapping = ClientCertMapping(base_url, username, password)
            self.jct_mapping = JunctionMapping (base_url, username, password)
            self.url_mapping = URLMapping(base_url, username, password)
            self.user_mapping = UserMapping(base_url, username, password)
            self.kerberos = Kerberos(base_url, username, password)
            self.password_strength = PasswordStrength(base_url, username, password)
            self.rsa = RSA(base_url, username, password)
            self.api_access_control = APIAccessControl(base_url, username, password)


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
