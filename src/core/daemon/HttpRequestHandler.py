__author__ = 'heinrich.potgieter@gmail.com'

import logging
from http.server import BaseHTTPRequestHandler


class HttpRequestHandler(BaseHTTPRequestHandler):
    logger_http_request_handler = logging.getLogger('HttpRequestHandler')
    logger_http_request_handler.debug(' === HttpRequestHandler::__init__ ===')

    def do_GET(self):
        self.logger_http_request_handler.info('do_GET')
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        self.logger_http_request_handler.info('do_POST')