"""
@copyright: IBM
"""

import json


class DataObject(object):

    def __init__(self):
        super(DataObject, self).__init__()
        self.data = {}

    def __str__(self):
        return str(self.data)

    def add_value(self, key, value):
        if value is not None:
            self.data[key] = value

    def add_value_boolean(self, key, value):
        if value == None:
            return
        if value is True:
            self.data[key] = True
        else:
            self.data[key] = False

    def add_value_not_empty(self, key, value):
        if value:
            self.data[key] = value

    def add_value_string(self, key, value):
        if value is not None:
            self.data[key] = str(value)

    def from_json(self, initial_data):
        self.data = initial_data

class Response(object):

    def __init__(self):
        super(Response, self).__init__()
        self.data = None
        self.json = None
        self.status_code = None
        self.success = None

    def __str__(self):
        return "<Response [%s, %s]>" % (self.success, self.status_code)

    def decode_json(self):
        try:
            self.json = json.loads(self.data)
        except Exception as e:
            self.json = None
