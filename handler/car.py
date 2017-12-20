#!/usr/bin/env python3
# coding=utf-8
import atexit
import json
from RPi import GPIO
from car.smartcar import SmartCar
from handler.base import BaseHandler

# 初始化GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
atexit.register(GPIO.cleanup)

with open("./static/config.json") as file:
    config = json.load(file)

car = SmartCar(config)


class ConnectTestHandler(BaseHandler):

    def _create_json(self):
        json_data = {}
        json_data['hrAngle'] = car.get_servo_angle_hr()
        json_data['vtAngle'] = car.get_servo_angle_vt()
        self.write(self.normal_json("connect successed", json_data))

    def get(self, *args, **kwargs):
        self._create_json()

    def post(self, *args, **kwargs):
        self._create_json()


class CarControlHandler(BaseHandler):

    def _create_json(self):
        action = self.get_argument('action')
        if action == 'forward':
            car.car_forward()
        elif action == 'backward':
            car.car_backward()
        elif action == 'front_turnleft':
            car.car_front_turnleft()
        elif action == 'front_turnright':
            car.car_front_turnright()
        elif action == 'back_turnleft':
            car.car_back_turnleft()
        elif action == 'back_turnright':
            car.car_back_turnright()
        elif action == 'stop':
            car.car_stop()
        else:
            return

        json_data = {}
        json_data['hrAngle'] = car.get_servo_angle_hr()
        json_data['vtAngle'] = car.get_servo_angle_vt()
        self.write(self.normal_json("car control, %s successed" % action, json_data))

    def get(self, *args, **kwargs):
        self._create_json()

    def post(self, *args, **kwargs):
        self._create_json()


class ServoControlHandler(BaseHandler):

    def _create_json(self):
        orientation = self.get_argument('orientation')
        angle = self.get_argument('angle')
        if orientation == 0:
            car.servo_hr_move_to(angle)
        elif orientation == 1:
            car.servo_vt_move_to(angle)
        else:
            return

        json_data = {}
        json_data['hrAngle'] = car.get_servo_angle_hr()
        json_data['vtAngle'] = car.get_servo_angle_vt()
        self.write(
            self.normal_json("servo control, orientation:%s, angle:%s successed" % (orientation, angle), json_data))

    def get(self, *args, **kwargs):
        self._create_json()

    def post(self, *args, **kwargs):
        self._create_json()
