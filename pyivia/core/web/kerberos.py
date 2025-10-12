""""
@copyright: IBM
"""

import logging

from pyivia.util.model import DataObject, Response
from pyivia.util.restclient import RESTClient

logger = logging.getLogger(__name__)

KERBEROS_CONFIG = "/wga/kerberos/config"
KERBEROS_KEYTAB = "/wga/kerberos/keytab"

class Kerberos(object):

    def __init__(self, base_url, username, password):
        super(Kerberos, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create(self, section_id=None, subsection=None, name=None, value=None):
        '''
        Create a kerberos configuration property or subsection

        Args:
            section_id (:obj:`str`): The name of the section/subsection where the new subsection/property will be created
            subsection (:obj:`str`, optional): Name of new subsection to create. Required if creating a new subsection
            name (:obj:`str`, optional): Name of new property to add to section/subsection. Required if creating a new property
            value (:obj:`str`, optional): Value of new property to add to section/subsection. Required if creating a new property

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the kerberos subsection/property is returned as JSON and can be accessed from
            the response.json attribute
        '''
        data = DataObject()
        data.add_value_not_empty("name", name)
        data.add_value_not_empty("subsection", subsection)
        data.add_value_string("value", value)

        endpoint = KERBEROS_CONFIG + "/{}".format(section_id)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def update(self, section_id=None, value=None):
        '''
        Update a kerberos configuration property

        Args:
            section_id (:obj:`str`): The name of the section/subsection where the property will be updated
            value (:obj:`str`): Value of new property to add to section/subsection. Required if creating a new property

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        data = DataObject()
        data.add_value_string("value", value)

        endpoint = KERBEROS_CONFIG + "/{}".format(section_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def get(self, section_id=None):
        '''
        Get a kerberos configuration property

        Args:
            section_id (:obj:`str`): The name of the section/subsection where the new subsection/property will be created.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the kerberos property is returned as JSON and can be accessed from
            the response.json attribute.
        '''
        endpoint = KERBEROS_CONFIG + "/{}".format(section_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def delete(self, section_id=None):
        '''
        Delete a kerberos configuration property or section

        Args:
            section_id (:obj:`str`): The name of the section/property to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute.
        '''
        endpoint = KERBEROS_CONFIG = "/{}".format(section_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def test(self, username=None, password=None):
        '''
        Test the Kerberos authentication of a web service principal using rest API.

        Args:
            username (:obj:`str`): The user to test authentication with
            password (:obj:`str`): The password to test authentication with

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        data = DataObject()
        data.add_value_string("username", username)
        data.add_value_string("password", password)

        endpoint = "/wga/kerberos/test"
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def import_keytab(self, keytab_file=None):
        '''
        Import a Kerberos keyfile.

        Args:
            keytab_file (:obj:`str`): Fully qualified path to the Kerberos keyfile.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the mapping keytab file id is returned as JSON and can be accessed from
            the response.json attribute
        '''
        response = Response()
        if keytab_file is None:
            response.success = False
            return response
        
        try:
            with open(keytab_file, 'rb') as contents:
                files = {"keytab_file": contents}

                response = self.client.post_file(KERBEROS_KEYTAB, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response


    def delete_keytab(self, keytab_id=None):
        '''
        Delete a Kerberos keyfile.

        Args:
            keytab_id (:obj:`str`): The ID of the keytab to be removed.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        '''
        endpoint = KERBEROS_KEYTAB + "/{}".format(keytab_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response


    def combine_keytab(self, new_name=None, keytab_files=[]):
        '''
        Combine a list of keytab files into a single keytab

        Args:
            new_name (:obj:`str`): The new name of the combined keytab file.
            keytab_files (:obj:`list` of :obj:`str`): List of existing keytab files to combine.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the new keytab file id returned as JSON and can be accessed from
            the response.json attribute
        '''
        data = DataObject()
        data.add_value_string("new_name", new_name)
        data.add_value_not_empty("keytab_files", keytab_files)

        response = self.client.put_json(KERBEROS_KEYTAB, data.data)
        response.success = response.status_code == 200

        return response


    def list_keytab(self):
        '''
        List all of the configured keytab files.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the keytab files are returned as JSON and can be accessed from
            the response.json attribute
        '''
        response = self.client.get_json(KERBEROS_KEYTAB)
        response.success = response.status_code == 200

        return response


    def verify_keytab(self, keytab_id=None, name=None):
        data = DataObject()
        data.add_value_string("name", name)

        endpoint = KERBEROS_KEYTAB + "/{}".format(keytab_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response
