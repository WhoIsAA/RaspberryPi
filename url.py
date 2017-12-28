#!/usr/bin/env python3
# coding=utf-8

from handler.index import IndexHandler
from handler.car import ConnectTestHandler, CarControlHandler, ServoControlHandler, CameraControlHandler

url = [
    (r'/', IndexHandler),
    (r'/carpi/connect_test', ConnectTestHandler),
    (r'/carpi/car', CarControlHandler),
    (r'/carpi/servo', ServoControlHandler),
    (r'/carpi/camera', CameraControlHandler),
]
