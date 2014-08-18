__author__="dvorak"
__date__ ="$Dec 17, 2011 10:45:35 PM$"
import logging
import urllib
from urllib import request
import threading


class NetworkHandler(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.Callback = callback
        self.logger_network = logging.getLogger("NetworkHandler")
        self.logger_network.debug(" === NetworkHandler::__init__ ===")
        # self.config = configparser.ConfigParser()
        #self.config.read_file(open('./config.conf'))

    def DoGet(self, url, user=None, password=None):
        proxy = urllib.request.ProxyHandler({'http': r''})
        auth = urllib.request.HTTPBasicAuthHandler()
        opener = urllib.request.build_opener(proxy, auth, urllib.request.HTTPHandler)
        request = opener.open(url)
        response = request.read()
        self.Callback(response)

if __name__ == "__main__":
    class ThreadManager():
        def Get(self):
            networkHandle = NetworkHandler(self.threadComplete)
            networkHandle.DoGet('http://myanimelist.net/malappinfo.php?status=all&u=DvorakUser')

        def threadComplete(self, data):
            print(data)

    manager = ThreadManager()
    manager.Get()
