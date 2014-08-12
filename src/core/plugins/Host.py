import logging
import configparser
from PyQt4.QtCore import QObject, pyqtSignal,  pyqtSlot
from core.util import XMLHandler, NetworkHandler
class Host(QObject):
    """
    Base class for all media classes. Defines interface and abstract
    functions that need to be implemented by all subclasses
    """
    media_list = None  # Needs to be overridden, dict of media from host
    xml_handle = XMLHandler.XMLHandler()
    network_handle = NetworkHandler.NetworkHandler()

    logger_host = None
    config = None

    # PyQt signal definitions follow
    refresh_started_signal = pyqtSignal(str)
    refresh_complete_signal = pyqtSignal()
    refresh_failed_signal = pyqtSignal(str)
    search_started_signal = pyqtSignal(str)
    search_complete_signal = pyqtSignal()
    search_failed_signal = pyqtSignal(str)
    send_message_signal = pyqtSignal(str)
    read_ready_signal = pyqtSignal()
  
    def __init__(self, parent=None):
        super(Host, self).__init__(parent)
        self.logger_Host = logging.getLogger("Host")
        # Read and assign config
        self.config = configparser.ConfigParser()
        try:
            self.config.readfp(open('./config.conf'))
            self.logger_Host.debug(" -- Successfully opened config file")
        except:
            self.logger_Host.error("Could not read ./config.conf")
        
        self.refresh_started_signal.connect(self.__refresh_started_slot)
        self.refresh_complete_signal.connect(self.__refresh_complete_slot)
        self.refresh_failed_signal.connect(self.__refresh_failed_slot)
        self.search_started_signal.connect(self.__search_started_slot)
        self.search_complete_signal.connect(self.__search_complete_slot)
        self.search_failed_signal.connect(self.__search_failed_slot)

    def refresh_media_list(self):
        """
        Refresh function.
        Takes no arguments, but reads path of media_list from
        config. Function needs to call network_handle.start.
        Function needs to emit refresh_started on success, or
        refresh_failed on failure.
        """
        raise NotImplementedError
    
    def refresh_search_list(self):
        """
        Refresh search function.
        Takes no arguments, but reads path of media_list from
        config. Function needs to calle network_handle.start.
        Function needs to emit search_started on success, or
        search_failed on failure.
        """
        raise NotImplementedError

    def parse_media_list(self):
        """
        Send command to parse the downloaded list.
        """
        raise NotImplementedError

    def add_media(self, media_id):
        """
        Adds media to the current media_list member
        """
        raise NotImplementedError

    def add_extra_info(self, extra_info):
        """
        Adds extra metadata after a parse of a list has been successfull
        """
        raise NotImplementedError
        
    @pyqtSlot(str,str)
    def __download_complete_slot(self, filename, class_name):
        """
        Connected to the NetworkHandler's download_complete_signal.
        """
        raise NotImplementedError
        
    @pyqtSlot(str)
    def __parse_complete_slot(self, filename):
        """
        Connected to the XMLHandler's parse_comlpete_signal.
        Emits a signal that either the media_list or the search_list_path
        is complete
        """
        raise NotImplementedError
    
    @pyqtSlot(str)
    def __refresh_started_slot(self,  filename):
        """
        Sends a signal to the calling class verifiying that the refresh
        signal has successfully started
        """
        self.send_message_signal.emit("Refresh of " + filename + " has started successfully")
        
    @pyqtSlot()
    def __refresh_complete_slot(self):
        """
        Sends a signal to the calling class verifiying that the refresh
        signal has completed successfully. This is done by the normal display
        signal as well as another signal to tell the calling class that the 
        media object is ready to be read.
        """
        self.send_message_signal.emit("Refresh has completed successfully")
        self.read_ready_signal.emit()
        
    @pyqtSlot(str)
    def __refresh_failed_slot(self,  filename):
        """
        Sends a signal to the calling class verifying that the refresh
        signal has failed to start
        """
        self.send_message_signal.emit("Refresh of " + filename + " has started unsuccessfully")
        
    @pyqtSlot(str)
    def __search_started_slot(self,  filename):
        """
        Sends a signal to the calling class verifiying that the search
        signal has successfully started
        """
        self.search_started_signal.emit(filename)
        
    @pyqtSlot()
    def __search_complete_slot(self):
        """
        Sends a signal to the calling class verifiying that the search
        signal has completed successfully
        """
        self.search_complete_signal.emit()
        
    @pyqtSlot(str)
    def __search_failed_slot(self,  filename):
        """
        Sends a signal to the calling class verifying that the search
        signal has failed to start
        """
        self.search_failed_signal.emit(filename)
