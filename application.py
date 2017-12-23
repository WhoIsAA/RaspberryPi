#!/usr/bin/env python3
# coding=utf-8

from url import url
from tornado.web import Application
from handler.base import ErrorHandler
import os

settings = dict(
    debug = True,
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    default_handler_class = ErrorHandler,
    #base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    # cookie_secret = "H+4fGguTT0W55iDItghVYx9As3f09EnhnlzOJoJ9RsI=",
    # #开启XFRF保护
    # xsrf_cookies = True,
    #如果self.current_user为false，会自动跳转到该目录
    login_url = "/",
)

application = Application(
    handlers=url,
    **settings,
)