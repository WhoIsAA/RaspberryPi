#!/usr/bin/env python3
# coding=utf-8

from tornado import ioloop, options, httpserver
from application import application
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

def main():
    options.parse_command_line()
    http_server = httpserver.HTTPServer(application)
    http_server.listen(options.port)

    print("Development server is running at http://127.0.0.1:%s" % options.port)
    print("Quit the server with Control-C")

    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
