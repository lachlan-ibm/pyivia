"""
@copyright: IBM
"""

import logging, os

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient


TEMPLATE_FILES = "/mga/template_files"

logger = logging.getLogger(__name__)


class TemplateFiles(object):

    def __init__(self, base_url, username, password):
        super(TemplateFiles, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_directory(self, path, dir_name=None):
        '''
        Create a new directory for template files.

        Args:
            path (:obj:`str`): Path to directory where new directory will be created.
            dir_name (:obj:`str`): Name of new directory

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the directory is returned as JSON and can be accessed from
            the response.json attribute

        '''
        data = DataObject()
        data.add_value_string("dir_name", dir_name)
        data.add_value_string("type", "dir")

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def get_directory(self, path, recursive=None):
        '''
        List the contents of a directory.

        Args:
            path (:obj:`str`): Path to directory to list.
            recursive (bool): Flag to recursively list subdirectories.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the contents of the directory is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        parameters = DataObject()
        parameters.add_value("recursive", recursive)

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)

        response = self.client.get_json(endpoint, parameters.data)
        response.success = response.status_code == 200

        if response.success and isinstance(response.json, dict):
            response.json = response.json.get("contents", [])

        return response


    def create_file(self, path, file_name=None, contents=None):
        '''
        Create a new template file.

        Args:
            name (:obj:`str`): Name of new file
            file_name (:obj:`str`, optional): Absolute path to file with contents of new template file. Either file_name
                                            or contents must be specified.
            contents (:obj:`str`, optional): Contents of new template file. Either file_name or contents must be specified.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the contents of the directory is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        data = DataObject()
        data.add_value_string("file_name", file_name)

        data.add_value_string("contents", contents)
        data.add_value_string("type", "file")

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def delete_file(self, path, file_name):
        '''
        Delete a template file from Verify Identity Access.

        Args:
            path (:obj:`str`): Path to template file.
            file_name (:obj:`str`): Name of template file to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the file is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_file(self, path, file_name):
        '''
        Get the conents of a template file.

        Args:
            path (:obj:`str`): Path to template file.
            file_name (:obj:`str`): Name of the file to return.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the contents of the file is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def import_file(self, path, file_name, file_path):
        '''
        Import a template file to Verify Identity Access.

        Args:
            path (:obj:`str`): The path to the directory where the new template file will be created
            file_name (:obj:`str`): The name of the template file.
            file_path (:obj:`str`): Absolute path to local file to be imported.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the file is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        response = Response()

        try:
            with open(file_path, 'rb') as template:
                files = {os.path.basename(file_path): template}

                endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))

                response = self.client.post_file(endpoint, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response


    def import_files(self, file_path, force=True):
        '''
        Import a compressed (zip) file of template files.

        Args:
            file_path (:obj:`str`): Absolute path to compressed file to be imported.
            force (bool): Flag to overwrite any existing template files in Verify Identity Access.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the file is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        response = Response()

        try:
            with open(file_path, 'rb') as templates:
                files = {"file": templates}

                data = DataObject()
                data.add_value("force", force)

                response = self.client.post_file(
                    TEMPLATE_FILES, data=data.data, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response


    def update_file(self, path, file_name, contents=None, force=False):
        '''
        Update an existing template file.

        Args:
            path (:obj:`str`): Path to directory where template file will be updated.
            file_name (:obj:`str`): name of file to be updated.
            contents (:obj:`str`): new contents of template file.
            force (bool): Flag o overwrite an existing file with the same name.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the file is returned as JSON and can be accessed from
            the response.json attribute.

        '''
        data = DataObject()
        data.add_value_string("contents", contents)
        data.add_value_string("force", force)
        data.add_value_string("type", "file")

        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response
