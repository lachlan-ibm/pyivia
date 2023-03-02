#!/bin/python
"""
@copyright: IBM
"""

from .apiac.cors import CORS
from .apiac.policies import Policies
from .apiac.resources import Resources
from .apiac.utilities import Utilities
from .apiac.document_root import DocumentRoot
from .apiac.authorization_server import AuthorizationServer

class APIAccessControl(object):
    '''
    Class is resposible for WebSEAL API Access Control endpoints
    '''

    def __init__(self, base_url, username, password):
        super(APIAccessControl, self).__init__()
        self.cors = CORS(base_url, username, password)
        self.policies = Policies(base_url, username, password)
        self.resoures = Resources(base_url, username, password)
        self.utilities = Utilities(base_url, username, password)
        self.document_root = DocumentRoot(base_url, username, password)
        self.authz_server = AuthoriztaionServer(base_url, username, password)
