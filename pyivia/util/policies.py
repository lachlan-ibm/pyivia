"""
@copyright: IBM
"""

import time


ACCESS_POLICY = [
    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
    "<!-- PolicyTag=urn:ibm:security:isam:8.0:xacml:2.0:config-policy -->",
    "<!-- PolicyName='%(policy_name)s' -->",
    "<PolicySet xmlns=\"urn:oasis:names:tc:xacml:2.0:policy:schema:os\" xmlns:xacml-context=\"urn:oasis:names:tc:xacml:2.0:context:schema:os\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"urn:oasis:names:tc:xacml:2.0:policy:schema:os http://docs.oasis-open.org/xacml/access_control-xacml-2.0-policy-schema-os.xsd\" PolicySetId=\"urn:ibm:security:config-policy\" PolicyCombiningAlgId=\"%(precedence_uri)s\">",
    "<Description>%(policy_description)s</Description>",
    "<Target/>",
    "%(rules)s"
    "</PolicySet>"
]
ATTRIBUTE = [
    "<AttributeAssignment AttributeId=\"%(attribute_id)s\">",
    "<AttributeDesignator AttributeId=\"%(designator_id)s\" Namespace=\"%(namespace)s\" Source=\"%(source)s\" DataType=\"%(data_type)s\"/>",
    "</AttributeAssignment>"
]
ATTRIBUTE_VALUE = [
    "<AttributeAssignment AttributeId=\"%(attribute_id)s\">",
    "<AttributeValue DataType=\"%(data_type)s\">%(attribute_value)s</AttributeValue>",
    "</AttributeAssignment>"
]
AUTHENTICATION_MECHANISM_AUTHENTICATOR_BASIC = [
    "<Step id=\"id%(id_a)s\" type=\"Authenticator\">",
    "<Authenticator id=\"id%(id_b)s\" AuthenticatorId=\"%(mechanism_uri)s\">",
    "</Authenticator>",
    "</Step>"
]
AUTHENTICATION_MECHANISM_AUTHENTICATOR_FINGERPRINT = [
    "<Step id=\"id%(id_a)s\" type=\"Authenticator\">",
    "<Authenticator id=\"id%(id_b)s\" AuthenticatorId=\"urn:ibm:security:authentication:asf:mechanism:mobile_user_approval:fingerprint\">",
    "<Parameters>",
    "%(username)s",
    "</Parameters>",
    "</Authenticator>",
    "</Step>"
]
AUTHENTICATION_MECHANISM_AUTHENTICATOR_MMFA = [
    "<Step id=\"id%(id_a)s\" type=\"Authenticator\">",
    "<Authenticator id=\"id%(id_b)s\" AuthenticatorId=\"urn:ibm:security:authentication:asf:mechanism:mmfa\">",
    "<Parameters>",
    "%(context_message)s",
    "%(mode)s",
    "%(policy_uri)s",
    "%(reauthenticate)s",
    "%(username)s",
    "</Parameters>",
    "</Authenticator>",
    "</Step>"
]
AUTHENTICATION_MECHANISM_AUTHENTICATOR_USER_PRESENCE = [
    "<Step id=\"id%(id_a)s\" type=\"Authenticator\">",
    "<Authenticator id=\"id%(id_b)s\" AuthenticatorId=\"urn:ibm:security:authentication:asf:mechanism:mobile_user_approval:user_presence\">",
    "<Parameters>",
    "%(username)s",
    "</Parameters>",
    "</Authenticator>",
    "</Step>"
]
AUTHENTICATION_MECHANISM_URI_RECAPTCHA_VERIFICATION = "urn:ibm:security:authentication:asf:mechanism:recaptcha"
AUTHENTICATION_MECHANISM_URI_SCIM_ENDPOINT_CONFIGURATION = "urn:ibm:security:authentication:asf:mechanism:scimConfig"
AUTHENTICATION_POLICY = [
    "<Policy xmlns=\"urn:ibm:security:authentication:policy:1.0:schema\" PolicyId=\"%(policy_id)s\">",
    "<Description>%(policy_description)s</Description>",
    "%(workflow)s",
    "</Policy>"
]
SOURCE_URI_SCOPE_REQUEST = "urn:ibm:security:asf:scope:request"
SOURCE_URI_SCOPE_SESSION = "urn:ibm:security:asf:scope:session"


class AccessPolicies(object):

    def policy(self, policy_name, policy_description, precedence_uri, rules):
        return ''.join(ACCESS_POLICY) % locals()

    def precedence_deny(self):
        return "urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:deny-overrides"

    def precedence_first(self):
        return "urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:first-applicable"

    def precedence_permit(self):
        return "urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:permit-overrides"


class AuthenticationPolicies(object):

    def basic_authenticator(self, mechanism_uri):
        millis = int(time.time() * 1000)
        id_a = millis
        id_b = millis + 1
        return ''.join(AUTHENTICATION_MECHANISM_AUTHENTICATOR_BASIC) % locals()

    def fingerprint_authenticator(self, username=""):
        millis = int(time.time() * 1000)
        id_a = millis
        id_b = millis + 1
        return ''.join(
            AUTHENTICATION_MECHANISM_AUTHENTICATOR_FINGERPRINT) % locals()

    def mmfa_authenticator(
            self, context_message="", mode="", policy_uri="", reauthenticate="",
            username=""):
        millis = int(time.time() * 1000)
        id_a = millis
        id_b = millis + 1
        return ''.join(AUTHENTICATION_MECHANISM_AUTHENTICATOR_MMFA) % locals()

    def policy(self, policy_id, policy_description, workflow):
        return ''.join(AUTHENTICATION_POLICY) % locals()

    def recaptcha_verification_authenticator(self):
        return self.basic_authenticator(
            AUTHENTICATION_MECHANISM_URI_RECAPTCHA_VERIFICATION)

    def request_parameter(
            self, attribute_id, designator_id, namespace, data_type="String"):
        source = SOURCE_URI_SCOPE_REQUEST
        return ''.join(ATTRIBUTE) % locals()

    def scim_endpoint_configuration_authenticator(self):
        return self.basic_authenticator(
            AUTHENTICATION_MECHANISM_URI_SCIM_ENDPOINT_CONFIGURATION)

    def session_parameter(
            self, attribute_id, designator_id, namespace, data_type="String"):
        source = SOURCE_URI_SCOPE_SESSION
        return ''.join(ATTRIBUTE) % locals()

    def user_presence_authenticator(self, username=""):
        millis = int(time.time() * 1000)
        id_a = millis
        id_b = millis + 1
        return ''.join(
            AUTHENTICATION_MECHANISM_AUTHENTICATOR_USER_PRESENCE) % locals()

    def value_parameter(
            self, attribute_id, attribute_value, data_type="String"):
        return ''.join(ATTRIBUTE_VALUE) % locals()
