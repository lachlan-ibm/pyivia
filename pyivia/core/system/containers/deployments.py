#!/bin/python
"""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient


DEPLOYMENT = "/isam/container_ext/container"

logger = logging.getLogger(__name__)

'''
Class is responsible for managing authorization configuration to 
external container image registries.
'''
class Deployments(object):


    def __init__(self, base_url, username, password):
        super(Deployments, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create(self, name=None, image=None, type=None, ports=None, volumes=None,
               env=None, logging=None, command=None, args=None):
        '''
        Create a new managed container deployment. 

        Args:
            name (:obj:`str`): Name of the container deployment.
            image (:obj:`str`): Container image to use.
            type (:obj:`str`): Container deployment metadata type.
            ports (:obj:`list` of :obj:`dict`): Mapping between container ports and host ports.
            volumes (:obj:`list` of :obj:`dict`): Container volume mount properties.
            env (:obj:`list` of :obj:`dict`): Container environment variable properties.
            logging (:obj:`list` of :obj:`dict`): Container logfile rollover properties.
            command (:obj:`str`, optional): An optional command from the metadata document to 
                                            run instead of the container entrypoint.
            args (:obj:`list` of :obj:`str`): An optional list of arguments to pass to 
                                            the specified command. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the created deployment is returned as JSON and can be accessed from
            the response.json attribute
        '''
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("image", image)
        data.add_value_string("type", type)
        data.add_value_not_empty("ports", ports)
        data.add_value_not_empty("volumes", volumes)
        data.add_value_not_empty("env", env)
        data.add_value_not_empty("logging", logging)
        data.add_value_string("command", command)
        data.add_value_not_empty("args", args)

        response = self.client.post_json(DEPLOYMENT, data.data)
        response.success = response.status_code == 201

        return response


    def update(self, deployment_id, operation=None, command=None, args=None):
        '''
        Update the pod state of a managed container deployment. 

        Args:
            deployment_id (:obj:`str`): The id of the container deployment.
            operation (:obj:`str`): Should the container be stopped ("stop") or 
                                    started ("start") or restarted ("restart"). 
                                    Either "command" or "operation" property must be provided.
            command (:obj:`str`): The name of the command from the metadata document to run. 
                                  Either "command" or "operation" property must be provided.
            type (:obj:`str`): Container deployment metadata type.
            args (:obj:`list` of :obj:`str`): An optional list of arguments to pass to 
                                            the specified command. 

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the output from the command is returned as JSON and can be accessed from
            the response.json attribute. Operations do not return JSON.
        '''
        data = DataObject()
        data.add_value_string("operation", operation)
        data.add_value_string("command", command)
        data.add_value_not_empty("args", args)

        endpoint = "{}/{}".format(DEPLOYMENT, deployment_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200 or response.status_code == 204

        return response


    def delete(self, deployment_id=None):
        '''
        Delete a credential for a user and container registry. 

        Args:
            deployment_id (:obj:`str`): The id of the container deployment to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        endpoint = "{}/{}".format(DEPLOYMENT, deployment_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get(self, deployment_id=None):
        '''
        Get the deployment properties for a managed container. 

        Args:
            deployment_id (:obj:`str`): Unique id of the managed container.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the deployment properties are returned as JSON and can be accessed from
            the response.json attribute
        '''
        endpoint = "{}/{}".format(DEPLOYMENT, deployment_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def list(self):
        '''
        Get all known deployment properties for all managed containers.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the deployment properties are returned as JSON and can be accessed from
            the response.json attribute
        '''
        response = self.client.get_json(DEPLOYMENT)
        response.success = response.status_code == 200

        return response