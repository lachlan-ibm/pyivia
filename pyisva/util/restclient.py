"""
@copyright: IBM
"""

import base64
import copy
import json
import logging
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .model import Response


logger = logging.getLogger(__name__)


class RESTClient(object):

    def __init__(self, base_url, username=None, password=None):
        super(RESTClient, self).__init__()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self._base_url = base_url
        self._username = username
        self._password = password

    def delete(self, endpoint, accept_type="*/*"):
        url = self._base_url + endpoint
        headers = self._get_headers(accept_type)

        self._log_request("DELETE", url, headers)

        r = requests.delete(url=url, headers=headers, params=None, verify=False)

        self._log_response(r.status_code, r.headers, r.content)

        response = self._build_response(r)
        r.close()

        return response

    def delete_json(self, endpoint):
        return self.delete(endpoint, accept_type="application/json")

    def get(
            self, endpoint, accept_type="*/*", content_type="application/json",
            parameters=None):
        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        self._log_request("GET", url, headers)

        r = requests.get(
            url=url, params=parameters, headers=headers, verify=False)

        self._log_response(r.status_code, r.headers, r._content)

        response = self._build_response(r)
        r.close()

        return response

    def get_json(self, endpoint, parameters=None):
        return self.get(
            endpoint, accept_type="application/json", parameters=parameters)

    def get_wait(
            self, endpoint, status_code=200, iteration_wait=3,
            max_iterations=20):
        logger.debug("Waiting for %i response from %s", status_code, endpoint)
        response = Response()
        url = self._base_url + endpoint

        iteration = 1
        while response.status_code != status_code and (
                max_iterations is None or iteration <= max_iterations):
            try:
                self._log_request("GET", url, None)

                r = requests.get(url=url, verify=False, timeout=1)

                self._log_response(r.status_code, r.headers, r.content)

                response = self._build_response(r)
                r.close()
            except: # Ignore this
                pass

            if response.status_code != status_code:
                time.sleep(iteration_wait)
                iteration += 1

        return response


    def post(
            self, endpoint, accept_type="*/*", content_type="application/json",
            parameters=None, data=""):
        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        self._log_request("POST", url, headers)

        r = requests.post(
            url=url, headers=headers, params=parameters, data=data,
            verify=False)

        self._log_response(r.status_code, r.headers, r.content)

        response = self._build_response(r)
        r.close()

        return response

    def post_file(
            self, endpoint, accept_type="application/json", data="", files={}, parameters=None):
        url = self._base_url + endpoint
        headers = self._get_headers(accept_type)

        self._log_request("POST", url, headers)

        r = requests.post(
            url=url, headers=headers, data=data, files=files, params=parameters, verify=False)

        self._log_response(r.status_code, r.headers, r.content)

        response = self._build_response(r)
        r.close()

        return response

    def post_json(self, endpoint, data=""):
        return self.post(
            endpoint, accept_type="application/json", data=json.dumps(data))

    def put(
            self, endpoint, accept_type="*/*", content_type="application/json",
            data=""):
        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        self._log_request("PUT", url, headers)

        r = requests.put(
            url=url, headers=headers, params=None, data=data, verify=False)

        self._log_response(r.status_code, r.headers, r.content)

        response = self._build_response(r)
        r.close()

        return response

    def put_json(self, endpoint, data=""):
        return self.put(
            endpoint, accept_type="application/json", data=json.dumps(data))

    def put_file(
            self, endpoint, accept_type="application/json", data="", files={}, parameters=None):
        url = self._base_url + endpoint
        headers = self._get_headers(accept_type)

        self._log_request("PUT", url, headers)

        r = requests.put(
            url=url, headers=headers, data=data, files=files, params=parameters, verify=False)

        self._log_response(r.status_code, r.headers, r.content)

        response = self._build_response(r)
        r.close()

        return response

    def _build_response(self, request_response):
        response = Response()
        try:
            response.data = request_response.content.decode()
        except (UnicodeDecodeError, AttributeError):
            response.data = request_response.content
        response.status_code = request_response.status_code
        content_type = request_response.headers.get("Content-type", "").lower()
        if "application/json" in content_type:
            response.decode_json()
        location = request_response.headers.get("Location", "").lower()
        if location:
            response.id_from_location = location.split('/')[-1]

        return response

    def _get_headers(self, accept_type=None, content_type=None):
        headers = {}

        if accept_type:
            headers["Accept"] = accept_type

        if content_type:
            headers["Content-type"] = content_type

        if self._username and self._password:
            credential = "%s:%s" % (self._username, self._password)
            credential_encode = base64.b64encode(credential.encode())
            authorization = "Basic " + str(credential_encode.decode()).rstrip()
            headers["Authorization"] = authorization

        return headers

    def _log_request(self, method, url, headers):
        safe_headers = copy.copy(headers)
        if safe_headers and safe_headers.get("Authorization", None):
            safe_headers["Authorization"] = "*******"

        logger.debug("Request: %s %s headers=%s", method, url, safe_headers)

    def _log_response(self, status_code, headers, content):
        logger.debug("Response: %i headers=%s content=%s", status_code, headers, content)
