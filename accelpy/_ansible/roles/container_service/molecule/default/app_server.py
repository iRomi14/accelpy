#! /usr/bin/env python3
# coding=utf-8
"""Fake application web server"""
from os import getuid, getgid, environ
from json import dumps
from http.server import HTTPServer, BaseHTTPRequestHandler
from accelize_drm.fpga_drivers import get_driver
from traceback import format_exc


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Server that return FPGA response"""

    def do_GET(self):
        """GET"""
        try:
            driver = get_driver(name='aws_f1')(
                fpga_slot_id=int(environ['FPGA_SLOTS'].split(',', 1)[0]))
            code = 200
            msg = dumps(dict(
                response=driver.read_register(0),
                uid=getuid(), gid=getgid(),
            ))
        except Exception:
            code = 500
            msg = format_exc()
        self.send_response(code)
        self.end_headers()
        self.wfile.write(msg.encode() + b'\n')


HTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler).serve_forever()
