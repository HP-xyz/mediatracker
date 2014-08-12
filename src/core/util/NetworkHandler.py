__author__="dvorak"
__date__ ="$Dec 17, 2011 10:45:35 PM$"
import logging
import configparser
from PyQt4.QtNetwork import *
from PyQt4.QtCore import *
class NetworkHandler(QThread):
    progress_signal = pyqtSignal(int, name='progressUpdate')
    download_complete_signal = pyqtSignal(str, str, name='downloadComplete')
    def __init__(self, parent = None):
        super(NetworkHandler, self).__init__(parent)
        self.logger_network = logging.getLogger("NetworkHandler")
        self.logger_network.debug(" === NetworkHandler::__init__ ===")

        self.config = configparser.ConfigParser()
        self.config.readfp(open('./config.conf'))

        self.filename = ''
        self.network_access_manager = QNetworkAccessManager()
        self.network_access_manager.finished.connect(
                                                self.__transaction_complete)
        self.reply = QObject()

        self.__transaction_type = 0
    def run(self):
        self.logger_network.debug(" === NetworkHandler::run ===")
        
    def set_calling_classname(self, classname):
        """ 
        The network handler needs to know what class its doing work for
        so that its name can be sent in the download_complete signal
        """
        self.class_name = classname

    def __setup_network(self, host, query):
        """ 
        Setting up the network before transactions can be done.
        MUST be called before any uploading/downloading!

        host = host (without protocol)
        query = query (part of url without host)
        """
        self.logger_network.debug("== NetworkHandler::__setup_network ==")

        #Generating the url to download
        self.s_url = host + query
        #url += "?u=" + self.config["MAL"]["username"]
        #url += "?status=all?type=anime"
        self.logger_network.debug(" -- URL Generated: %s", self.s_url)

        #Setting proxy values if need be
        if (self.config["Network"]["proxy"] == "True"):
            self.logger_network.info("-- Using proxy")
            self.logger_network.debug("-- Host = %s",
                                    self.config["Network"]["host"])
            self.logger_network.debug("-- Port = %s",
                                    self.config["Network"]["port"])
            self.logger_network.debug("-- User = %s",
                                    self.config["Network"]["username"])
            self.logger_network.debug("-- Pass = %s",
                                    self.config["Network"]["password"])

            proxy = QNetworkProxy()
            proxy.setType(QNetworkProxy.HttpProxy)
            proxy.setHostName(self.config["Network"]["host"])
            proxy.setPort(int(self.config["Network"]["port"]))
            proxy.setUser(self.config["Network"]["username"])
            proxy.setPassword(self.config["Network"]["password"])

            self.network_access_manager.setProxy(proxy)
        else:
            self.logger_network.info("-- Not using proxy")

        #Creating url into proper QUrl
        self.url = QUrl(self.s_url)

        #Extreme Logging! (FOR DEBUGGING ONLY)
        self.logger_network.debug("-- q_url.isEmpty(): %s",
                                    self.url.isEmpty())
        self.logger_network.debug("-- q_url.isValid(): %s" ,
                                    self.url.isValid())
        self.logger_network.debug("-- q_url.hasQuery(): %s",
                                    self.url.hasQuery())

        self.request = QNetworkRequest(self.url)

    def download_file(self, host, query, filename):
        """
        Downloads a file
        host = host (without protocol)
        query = query (part of url without host)
        filename = filename to save the file to

        Will return to calling thread if the initialization of the download
        was successufull. The calling thread then has to call start on the class
        object, to initiate the actual download
        """

        # We need to call __setup_network to initialize the network_access_manager
        # and request
        self.__setup_network(host, query)
        self.filename = filename

        # We must specify that be are doing a DOWNLOAD transaction
        self.__transaction_type = 2

        self.logger_network.debug("-- Going to save as: %s" ,
                                    filename)
        #Lets get a reply
        try:
            self.reply = self.network_access_manager.get(self.request)
            self.reply.downloadProgress.connect(self.__update_progress_bar_slot)
            return True
        except Exception as error:
            self.logger_network.critical("!! - Error getting reply: %s", error)
            return False

        #self.start()
        #self.eventloop.exec_() # Needed to start the actual download

    def upload_file(self, host, query, request_string):
        """
        Uploads a file, or just does a normal query
        host = host (without protocol)
        query = query (part of url without host)
        filename = filename to save the file to

        Will return to calling thread if the initialization was successfull.
        The calling thread then has to call start on the class object to init
        the actual download.
        """
        # We need to call __setup_network to initialize the network_access_manager
        # and request
        self.__setup_network(host, query)

        request_string = QUrl.toPercentEncoding(request_string)
        self.logger_network.debug ("Encoded URL: %s", request_string)
        self.request.setRawHeader ("Content-type", "application/xml");
        self.request.setRawHeader ("Content-length", bytes(request_string));
        self.request.setRawHeader ("Connection", "close");
        
        for header in self.request.rawHeaderList():
            print (header)
        
        # We must specify that be are doing a UPLODAD/PUT transaction
        self.__transaction_type = 1
        
        try:
            self.reply = self.network_access_manager.post(self.request, request_string)
            return True
        except Exception as error:
            self.logger_network.critical("!! - Error getting reply: %s", error)
            return False

    def __transaction_complete(self, reply):
        """ Slot gets called on completion of network transaction """
        #Extreme logging again
        self.logger_network.debug(" == NetworkHandler::transaction_complete ==")
        self.logger_network.debug("  -- Status Code: %s",
                    reply.attribute(QNetworkRequest.HttpStatusCodeAttribute))
        self.logger_network.debug("  -- Status Phrase: %s",
                    reply.attribute(QNetworkRequest.HttpReasonPhraseAttribute))
        self.logger_network.debug("  -- ContentType: %s",
                    reply.header(QNetworkRequest.ContentTypeHeader))
        self.logger_network.debug("  -- ContentLength: %s",
                    reply.header(QNetworkRequest.ContentLengthHeader))
        self.logger_network.debug("  -- LocationHeader: %s",
                    reply.header(QNetworkRequest.LocationHeader))
        self.logger_network.debug("  -- Transaction Type: %s",
                    self.__transaction_type)

        if (reply.error() == QNetworkReply.NoError
                and self.__transaction_type == 1):
            #THIS IS FOR UPLOADS, OR TRANSACTIONS THAT WILL NOT DOWNLOAD
            bytes_ = reply.readAll()
            data = str(bytes_)
            self.logger_network.debug("  -- Content: %s",data)
        elif (reply.error() == QNetworkReply.NoError
                and self.__transaction_type == 2):
            #THIS IS FOR DOWNLOADS
            with open(self.filename, 'wb+') as file:
                file.write(reply.readAll())
            self.logger_network.debug("  -- Sending download complete signal")
            self.download_complete_signal.emit(self.filename, self.class_name)
        elif (reply.error() == QNetworkReply.NoError
                and self.__transaction_type == 0):
            #I HOPE THIS NEVER HAPPENS
            self.logger_network.critical("  -- No download error",
                                    "but application does not know what to do")
        else:
            self.logger_network.critical("  -- Reply error: %s",
                                        reply.errorString())

    def __update_progress_bar_slot(self, bytes_recieved, bytes_total):
        self.logger_network.debug(" -- Network Progress %s / %s",
                                    bytes_recieved, bytes_total)
        if (bytes_total != 0):
            double_progress = bytes_recieved * 100 / bytes_total
            int_progress = int(double_progress)
            self.progress_signal.emit(int_progress)


if __name__ == "__main__":
    print("Please run python_anime_tracker.py")
