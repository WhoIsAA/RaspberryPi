#!/usr/bin/env python3
# coding=utf-8
import json
import threading
from time import sleep
from handler.base import BaseHandler
from car.smartcar import SmartCar


class CarHandler(BaseHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.cur_value = 0;
        with open("config.json") as file:
            self.config = json.load(file)

    def get(self, *args, **kwargs):
        # self.write(self.error_json(desc="To be completed"))
        t = threading.Thread(target=self.test)
        t.setDaemon(True)
        t.start()
        for i in range(1000):
            print("post = " + str(self.cur_value))
            self.write(self.normal_json(str(self.cur_value)))
            sleep(1)
        print("****** over")

    def post(self, *args, **kwargs):
        # self.write(self.normal_json(""))
        t = threading.Thread(target=self.test)
        t.setDaemon(True)
        t.start()
        for i in range(10):
            print("post = " + self.cur_value)
            self.write(self.normal_json(self.cur_value))
            sleep(1)
        print("****** over")

    def test(self):
        while True:
            self.cur_value = self.cur_value + 1
            sleep(0.5)