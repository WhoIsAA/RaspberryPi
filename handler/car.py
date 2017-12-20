#!/usr/bin/env python3
# coding=utf-8

from handler.base import BaseHandler


class ConnectTestHandler(BaseHandler):

    def _create_json(self):
        json_data = {}
        json_data['hrAngle'] = 90
        json_data['vtAngle'] = 90
        self.write(self.normal_json("connect successed", json_data))

    def get(self, *args, **kwargs):
        self._create_json()

    def post(self, *args, **kwargs):
        self._create_json()


class CarControlHandler(BaseHandler):

    def _create_json(self):
        action = self.get_argument('action')
        json_data = {}
        json_data['hrAngle'] = 90
        json_data['vtAngle'] = 90
        self.write(self.normal_json("car control, %s successed" % action, json_data))

    def get(self, *args, **kwargs):
        self._create_json()

    def post(self, *args, **kwargs):
        self._create_json()


class ServoControlHandler(BaseHandler):

    def _create_json(self):
        orientation = self.get_argument('orientation')
        angle = self.get_argument('angle')
        json_data = {}
        json_data['hrAngle'] = 90
        json_data['vtAngle'] = 90
        self.write(self.normal_json("servo control, orientation:%s, angle:%s successed" % (orientation, angle), json_data))

    def get(self, *args, **kwargs):
        self._create_json()

    def post(self, *args, **kwargs):
        self._create_json()
