"""
@copyright: IBM
"""

import logging
import uuid

from pyivia.util.model import DataObject
from pyivia.util.restclient import RESTClient

POC_PROFILES = "/iam/access/v8/poc/profiles"
POC = "/iam/access/v8/poc"

logger = logging.getLogger(__name__)

class PointOfContact(object):

    def __init__(self, base_url, username, password):
        super(PointOfContact, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def create_profile(self, name, description=None, authenticate_callbacks=[], sign_in_callbacks=[], local_id_callbacks=[],
            sign_out_callbacks=[], authn_policy_callbacks=[]):
        """
        Create a new Point of Contact profile.

        Args:
            name (:obj:`str`): A meaningful name to identify this point of contact profile.
            description (:obj:`str`, optional): A description of the point of contact profile.
            authenticate_callbacks (:obj:`list` of :obj:`dict`): An array of callbacks for authentication. The format 
                                    of the dictionary is::

                                        {
                                            "index":0,
                                            "moduleReferenceId":"websealPocAuthenticateCallback",
                                            "parameters": [
                                                            {"name":"authentication.level",
                                                             "value":"1"}
                                                        ]
                                        }

            sign_in_callbacks (:obj:`list` of :obj:`str`): An array of callbacks for sign in. The format of the 
                                    dictionary is::

                                            {
                                                "index":0,
                                                "moduleReferenceId":"websealPocSignInCallback",
                                                "parameters": [
                                                                {"name":"fim.user.response.header.name",
                                                                 "value":"am-fim-eai-user-id"}
                                                            ]
                                            }

            local_id_callbacks (:obj:`list` of :obj:`dict`): An array of callbacks for local identity. The format of 
                                    the dictionary is::

                                        {
                                            "index":0,
                                            "moduleReferenceId":"websealPocLocalIdentityCallback",
                                            "parameters":[
                                                          {"name":"fim.cred.request.header.name",
                                                           "value":"iv-creds"}
                                                        ]
                                        }

            sign_out_callbacks (:obj:`list` of :obj:`dict`): An array of callbacks for sign out. The format of the 
                                    dictionary is::

                                        {
                                            "index":0,
                                            "moduleReferenceId":"websealPocSignOutCallback",
                                            "parameters":[
                                                          {"name":"fim.user.session.id.request.header.name",
                                                           "value":"user_session_id"}
                                                        ]
                                        }


            authn_policy_callbacks (:obj:`list` of :obj:`dict`): An array of callbacks for authentication policy. The format
                                    of the dictionary is::

                                        {
                                            "index":0,
                                            "moduleReferenceId":"genericPocAuthnPolicyCallback",
                                            "parameters":[
                                                          {"name":"authentication.level",
                                                           "value":"1"}
                                                        ]
                                        }


        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created PoC profile can be acess from the 
            response.id_from_location attribute
        """
        configuration = DataObject()
        configuration.add_value_string("name", name)
        configuration.add_value_string("description", description)
        configuration.add_value_not_empty("authenticateCallbacks", authenticate_callbacks)
        configuration.add_value_not_empty("signInCallbacks", sign_in_callbacks)
        configuration.add_value_not_empty("localIdCallbacks", local_id_callbacks)
        configuration.add_value_not_empty("signOutCallbacks", sign_out_callbacks)
        configuration.add_value_not_empty("authnPolicyCallbacks", authn_policy_callbacks)
        response = self.client.post_json(POC_PROFILES, configuration.data)
        response.success = response.status_code == 201

        return response


    def update_profile(self, poc_id, name=None, description=None, authenticate_callbacks=[], sign_in_callbacks=[], 
            local_id_callbacks=[], sign_out_callbacks=[], authn_policy_callbacks=[]):
        """
        Update an existing Point of Contact profile.

        Args:
            poc_id (:obj:`str`): The unique generated identifier of the Point of Contact profile.
            name (:obj:`str`): A meaningful name to identify this point of contact profile.
            description (:obj:`str`, optional): A description of the point of contact profile.
            authenticate_callbacks (:obj:`list` of :obj:`dict`): An array of callbacks for authentication. The format 
                        of the dictionary is::

                                        {
                                            "index":0,
                                            "moduleReferenceId":"websealPocAuthenticateCallback",
                                            "parameters": [
                                                            {"name":"authentication.level",
                                                             "value":"1"}
                                                        ]
                                        }

            sign_in_callbacks (:obj:`list` of :obj:`str`): An array of callbacks for sign in. The format of the 
                        dictionary is::

                                        {
                                            "index":0,"moduleReferenceId":
                                            "websealPocSignInCallback",
                                            "parameters": [
                                                            {"name":"fim.user.response.header.name",
                                                             "value":"am-fim-eai-user-id"}
                                                        ]
                                        }

            local_id_callbacks (:obj:`list` of :obj:`dict`): An array of callbacks for local identity. The format of 
                        the dictionary is::

                                            {
                                                "index":0,
                                                "moduleReferenceId":"websealPocLocalIdentityCallback",
                                                "parameters": [
                                                                {"name":"fim.cred.request.header.name",
                                                                 "value":"iv-creds"}
                                                            ]
                                            }

            sign_out_callbacks (:obj:`list` of :obj:`dict`): An array of callbacks for sign out. The format of the 
                        dictionary is::

                                        {
                                            "index":0,
                                            "moduleReferenceId":"websealPocSignOutCallback",
                                            "parameters": [
                                                            {"name":"fim.user.session.id.request.header.name",
                                                             "value":"user_session_id"}
                                                        ]
                                        }

            authn_policy_callbacks (:obj:`list` of :obj:`dict`): An array of callbacks for authentication policy. The format
                        of the dictionary is::

                                        {
                                            "index":0,
                                            "moduleReferenceId":"genericPocAuthnPolicyCallback",
                                            "parameters": [
                                                            {"name":"authentication.level",
                                                             "value":"1"}
                                                        ]
                                        }

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

        """
        configuration = DataObject()
        configuration.add_value_string("name", name)
        configuration.add_value_string("description", description)
        configuration.add_value_not_empty("authenticateCallbacks", authenticate_callbacks)
        configuration.add_value_not_empty("signInCallbacks", sign_in_callbacks)
        configuration.add_value_not_empty("localIdCallbacks", local_id_callbacks)
        configuration.add_value_not_empty("signOutCallbacks", sign_out_callbacks)
        configuration.add_value_not_empty("authnPolicyCallbacks", authn_policy_callbacks)
        endpoint = "{}/{}".format(POC_PROFILES, poc_id)
        response = self.client.put_json(endpoint, configuration.data)
        response.success = response.status_code == 204

        return response


    def list_profiles(self):
        """
        Get the list of configured Point of Contact profiles.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the POC profiles are returned as JSON and can be accessed from
            the response.json attribute
        """

        endpoint = POC_PROFILES

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_profile(self, poc_id):
        """
        Get a configured Point of Contact profiles.

        Args:
            poc_id (:obj:`str`): The system-assigned point of contact profile identifier.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the POC profile is returned as JSON and can be accessed from
            the response.json attribute
        """

        endpoint = "{}/{}".format(POC_PROFILES, poc_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def get_current_profile(self):
        """
        Get the active Point of Contact profile.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the POC profile is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = POC

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def set_current_profile(self, profile_id):
        """
        Update the Point of Contact profile

        Args:
            profile_id (:obj:`str`): The ID of an existing point of contact profile to set as the current profile.

        Returns:
            :obj:`~requests.Response`: The response from verify identity access. 

            Success can be checked by examining the response.success boolean attribute
        """
        data = DataObject()

        data.add_value('currentProfileId',profile_id)

        endpoint = POC
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response


    def create_like_credential(self, name=None, description="", authenticate_callbacks=None, 
            local_id_callbacks=None, sign_out_callbacks=None, sign_in_callbacks=None):
        
        data = DataObject()

        initial_json = {
                "id": "",
                "name": name,
                "description": description,
                "isReadOnly": False,
                "signInCallbacks": [ {
                    "moduleReferenceId": "websealPocSignInCallback",
                    "index": 0,
                    "parameters": [
                      { "name": "fim.user.response.header.name", "value": "" },
                      { "name": "fim.user.session.id.response.header.name", "value": "" },
                      { "name": "fim.target.response.header.name", "value": "am-eai-redir-url" },
                      { "name": "fim.attributes.response.header.name", "value": "" },
                      { "name": "fim.groups.response.header.name", "value": "" },
                      { "name": "url.encoding.enabled", "value": "false" },
                      { "name": "fim.server.response.header.name", "value": "" },
                      { "name": "fim.cred.response.header.name", "value": "am-eai-pac" },
                      { "name": "fim.user.request.header.name", "value": "iv-user" }
                    ] } ],
                "signOutCallbacks": [ {
                    "moduleReferenceId": "websealPocSignOutCallback",
                    "index": 0,
                    "parameters": [
                      { "name": "fim.user.session.id.request.header.name", "value": "user_session_id" },
                      { "name": "fim.user.request.header.name", "value": "iv-user" }
                    ] } ],
                "localIdCallbacks": [ {
                    "moduleReferenceId": "websealPocLocalIdentityCallback",
                    "index": 0,
                    "parameters": [
                      { "name": "fim.attributes.request.header.name", "value": "" },
                      { "name": "fim.groups.request.header.name", "value": "iv-groups" },
                      { "name": "fim.cred.request.header.name", "value": "iv-creds" },
                      { "name": "fim.user.request.header.name", "value": "iv-user" }
                    ] } ],
                "authenticateCallbacks": [ {
                    "moduleReferenceId": "websealPocAuthenticateCallback",
                    "index": 0,
                    "parameters": [
                      { "name": "fim.user.request.header.name", "value": "iv-user" }
                    ] } ] }



        items_to_update = {'signInCallbacks':sign_in_callbacks,
                'authenticateCallbacks': authenticate_callbacks,
                'signOutCallbacks':sign_out_callbacks,
                'localIdCallbacks':local_id_callbacks}

        for work in items_to_update.items():
            if work[1] == None:
                    continue

            before = initial_json[work[0]][0]['parameters']
            during = map(lambda ent: (ent['name'], ent['value']), before)

            after = {}
            after.update(during)
            after.update(work[1])

            initial_json[work[0]][0]['parameters'] = list(map(lambda ent: {"name":ent[0], "value":ent[1]}, after.items()))

        data.from_json(initial_json)

        endpoint = POC_PROFILES 
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response



