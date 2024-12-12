#!/bin/python
"""
@copyright: IBM
"""

from .apiac.cors import CORS
from .apiac.policies import Policies
from .apiac.resource_server import ResourceServer
from .apiac.utilities import Utilities
from .apiac.document_root import DocumentRoot
from .apiac.authorization_server import AuthorizationServer

class APIAccessControl(object):
    '''
    Class is responsible for WebSEAL API Access Control endpoints.

    :var cors: Manage the :ref:`Cross Origin Remote Scripting<Cross Origin Remote Scripting>` configuration.
    :var policies: Manage the API Access Control :ref:`authorization policies<Policies>`.
    :var resource_server: Manage the API Gateway Reverse Proxy :ref:`instances<Resources>`.
    :var utilities: Use helper :ref:`functions<Utilities>` for managing reverse proxy instances.
    :var document_root: Manage the static :ref:`document root<Document Root>` of an API Gateway.
    :var authz_server: Manage the :ref:`authorization<Authorization Server>` (policy) server of an API Gateway instance.
    '''

    def __init__(self, base_url, username, password):
        super(APIAccessControl, self).__init__()
        self.cors = CORS(base_url, username, password)
        self.policies = Policies(base_url, username, password)
        self.resource_server = ResourceServer(base_url, username, password)
        self.utilities = Utilities(base_url, username, password)
        self.document_root = DocumentRoot(base_url, username, password)
        self.authz_server = AuthorizationServer(base_url, username, password)
