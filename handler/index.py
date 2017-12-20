#!/usr/bin/env python3
# coding=utf-8

from handler.base import BaseHandler

class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("index.html")

    def post(self, *args, **kwargs):
        self.write(self.error_json("To be completed"))