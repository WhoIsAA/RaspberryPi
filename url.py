#!/usr/bin/env python3
# coding=utf-8

from handler.index import IndexHandler
from handler.car import ConnectTestHandler, CarControlHandler, ServoControlHandler

url = [
    (r'/', IndexHandler),
    (r'/carpi/connect_test', ConnectTestHandler),
    (r'/carpi/car_control', CarControlHandler),
    (r'/carpi/servo_control', ServoControlHandler),
]
