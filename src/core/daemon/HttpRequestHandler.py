__author__ = 'heinrich.potgieter@gmail.com'

import logging
from http.server import BaseHTTPRequestHandler

from src.core.util.NetworkHandler import NetworkHandler


class HttpRequestHandler(BaseHTTPRequestHandler):
    logger_http_request_handler = logging.getLogger('HttpRequestHandler')
    logger_http_request_handler.debug(' === HttpRequestHandler::__init__ ===')

    def do_GET(self):
        self.logger_http_request_handler.info('do_GET')
        networkHandle = NetworkHandler(HttpRequestHandler.list_download_complete_callback)
        networkHandle.DoGet('http://myanimelist.net/malappinfo.php?status=all&u=DvorakUser')

    def list_download_complete_callback(self):
        self.logger_http_request_handler.info('list_download_complete_callback')
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        self.logger_http_request_handler.info('do_POST')