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
    Object manages WebSEAL API Access Control features.

    '''

    cors: CORS
    'Manage the :ref:`Cross Origin Remote Scripting<Cross Origin Remote Scripting>` configuration.'
    policies: Policies
    'Manage the API Access Control :ref:`authorization policies<Policies>`.'
    resource_server: ResourceServer
    'Manage the API Gateway Reverse Proxy :ref:`instances<Resources>`.'
    utilities: Utilities
    'Use helper :ref:`functions<Utilities>` for managing reverse proxy instances.'
    document_root: DocumentRoot
    'Manage the static :ref:`document root<Document Root>` of an API Gateway.'
    authz_server: AuthorizationServer
    'Manage the :ref:`authorization<Authorization Server>` (policy) server of an API Gateway instance.'

    def __init__(self, base_url, username, password):
        super(APIAccessControl, self).__init__()
        self.cors = CORS(base_url, username, password)
        self.policies = Policies(base_url, username, password)
        self.resource_server = ResourceServer(base_url, username, password)
        self.utilities = Utilities(base_url, username, password)
        self.document_root = DocumentRoot(base_url, username, password)
        self.authz_server = AuthorizationServer(base_url, username, password)
