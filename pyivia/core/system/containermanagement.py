"""
@copyright: IBM
"""

import logging

from .containers.volumes import Volumes
from .containers.images import Images
from .containers.registry import Registry
from .containers.deployments import Deployments
from .containers.metadata import Metadata
from .containers.healthcheck import HealthCheck


logger = logging.getLogger(__name__)


class ContainerManagement(object):
    '''
    Object used to manage containers, images and volumes hosted on a Verify Identity Access appliance. 

    '''

    volumes: Volumes
    'Create and manage :ref:`Volumes`.'
    images: Images
    'Create and manage :ref:`Images`.'
    registry: Registry
    'Create and manage :ref:`Registry` authentication configuration.'
    deployments: Deployments
    'Create and manage :ref:`Deployments`.'
    metadata: Metadata
    'Create and manage deployment :ref:`Metadata`.'
    healthcheck: HealthCheck
    'Check the :ref:`health<Health Check>` of deployed pods (containers).'

    def __init__(self, base_url, username, password):
        super(ContainerManagement, self).__init__()
        self.volumes = Volumes(base_url, username, password)
        self.images = Images(base_url, username, password)
        self.registry = Registry(base_url, username, password)
        self.deployments = Deployments(base_url, username, password)
        self.metadata = Metadata(base_url, username, password)
        self.healthcheck = HealthCheck(base_url, username, password)
