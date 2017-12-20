#!/usr/bin/env python3
# coding=utf-8

import json
from tornado.web import RequestHandler

class BaseHandler(RequestHandler):

    def write_error(self, status_code, **kwargs):
        #重写此方法，发送错误
        self.write(self.error_json(status_code, str(kwargs['exc_info'][1])))

    def get_response(self, code=200, desc='', data=''):
        json_data = {}
        json_data['code'] = code
        json_data['desc'] = desc
        json_data['data'] = data
        return json.dumps(json_data)

    def error_json(self, code, desc='error'):
        return self.get_response(code, desc)

    def normal_json(self, desc, data):
        if data:
            return self.get_response(desc=desc, data=data)
        else:
            return self.error_json()

class ErrorHandler(BaseHandler):

    def write_error(self, status_code, **kwargs):
        #重写此方法，发送错误
        self.write(self.error_json(status_code, str(kwargs['exc_info'][1])))

