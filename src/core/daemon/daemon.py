__author__ = 'heinrich.potgieter@gmail.com'

import logging
import sys
from http import server as http_server

from src.core.daemon import HttpRequestHandler


class Daemon():
    httpd = None

    def __init__(self):
        self.logger_daemon = logging.getLogger("Daemon")
        self.logger_daemon.debug(" === Daemon::__init__ ===")

    def ListDownloadComplete_Callback(self, data):
        self.logger_daemon.info("List download complete (Size: %s)", sys.getsizeof(data.size))

    def run(self):
        server_address = ('127.0.0.1', 8000)
        self.httpd = http_server.HTTPServer(server_address, HttpRequestHandler.HttpRequestHandler)
        self.logger_daemon.debug("Started serving")
        self.httpd.serve_forever()


if __name__ == "__main__":
    daemon = Daemon()
    daemon.run()