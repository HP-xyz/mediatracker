'''
Created on 17 Jan 2012

@author: HP
'''
import logging
import configparser

from PyQt5.QtCore import *

from core.plugins import Host
from core.media import MAL_Anime


class MAL(Host.Host):
    '''
    Handles all MAL methods.
    '''
    logger_MAL = None
    
    def __init__(self, parent=None):
        '''
        Constructs the MAL class. Sets up logging and config, and creates some
        empty variables for later use
        '''
        super(MAL, self).__init__(parent)
        self.__setup_logging()
        
        self.config = configparser.ConfigParser()
        self.config.readfp(open('./config.conf'))

        # Overrides the super's host list, and defines it as a dict
        self.media_list = {}
        self.network_handle.set_calling_classname("MAL")
        
        self.xml_handle.add_media_signal.connect(self.add_media)
        self.xml_handle.parse_complete_extra_info.connect(self.add_extra_info)
        self.network_handle.download_complete_signal.connect(
                self.__download_complete_slot)
        self.xml_handle.parse_complete_signal.connect(
                self.__parse_complete_slot)
            
    def __setup_logging(self):
        self.logger_MAL = logging.getLogger("MAL")

    @pyqtSlot(str)
    def add_media(self, mal_id):
        """
        Adds an empty dict item to the host_list member if the mal_id is
        not already in that list. Information about the item should then be
        added in by direct access.
        Connects to signal in XMLHandler
        """
        if id not in self.media_list:
            anime_obj = MAL_Anime.MAL_Anime()
            self.logger_MAL.info("++ %s", mal_id)
            self.media_list[mal_id] = anime_obj
        else:
            self.logger_MAL.info("** %s already in list", mal_id)
        
    def refresh_media_list(self):
        """
        Fuction will refresh the anime list by downloading
        the anime_list.xml file from MAL. The download is
        threaded and NEEDS to call the network_handle.start()
        fuction.
        """
        if (self.network_handle.download_file("http://myanimelist.net",
                        "/malappinfo.php?u=" + self.config["MAL"]["username"] +"&status=all&type=anime",
                        self.config["MAL"]["media_list_path"])):
            self.logger_MAL.info(" ++ Download ('%s') init successfull",
                                self.config["MAL"]["media_list_path"])
            self.network_handle.start() # This starts the actual download

            #EMIT STARTING SIGNAL
            self.refresh_started_signal.emit(self.config["MAL"]["media_list_path"])
        else:
            self.logger_MAL.critical(" ++ Download ('%s') init unsuccessfull",
                                self.config["MAL"]["media_list_path"])

            #EMIT FAILED SIGNAL HERE
            self.refresh_failed_signal(self.config["MAL"]["media_list_path"]).emit()
			    
    def refresh_search_list(self, title):
      """
      Function will download the search list by downloading
      the search.xml file from MAL. The download is threaded and
      NEEDS to call the network_handle.start() fuction
      """
      host = "http://myanimelist.net"
      query_string = "/api/anime/search.xml?q=" + title
      if (self.network_handle.download_file(host, query_string,
                        self.config["MAL"]["search_list_path"])):
            self.logger_MAL.info("++ Download ('%s') init successfull",
                                self.config["MAL"]["search_list_path"])
            self.network_handle.start() # This starts the actual download
            
            #EMIT STARTING SIGNAL
            self.search_started_signal(
                    self.config["General"]["search_list_path"]).emit()
      else:
            self.logger_MAL.critical("!! Download ('%s') init unsuccessfull",
                                self.config["MAL"]["search_list_path"])
            #EMIT FAILED SIGNAL
            self.search_failed_signal.emit(
                    self.config["MAL"]["search_list_path"])

    def __parse_media_list(self, filename):
        """
        Send command to parse the downloaded list.
        """
        self.xml_handle.parse_media_list("MAL", filename, self.media_list)

    @pyqtSlot(dict)
    def add_extra_info(self, extra_info):
        """
        Function to add other info to the media_list object.
        Connects to signal from XMLHandler
        """
        #TODO
        #Add config options for what data should be added and displayed.
        #For now just add all the metadata that is read from file
        for key in extra_info.keys():
            try:
                self.media_list[key].set_title(extra_info[key]['series_title'])
                self.media_list[key].set_synonyms((extra_info[key]['series_synonyms']).split(';'))
                self.media_list[key].set_episodes(extra_info[key]['series_episodes'])
                self.media_list[key].set_watched_episodes(extra_info[key]['my_watched_episodes'])
                self.media_list[key].set_score(extra_info[key]['my_score'])
                self.media_list[key].set_type(extra_info[key]['series_type'])
                self.media_list[key].set_status(extra_info[key]['series_status'])
                self.media_list[key].set_watched_status(extra_info[key]['my_status'])
                self.media_list[key].set_start_date(extra_info[key]['series_start'])
                self.media_list[key].set_end_date(extra_info[key]['series_end'])
                self.logger_MAL.info("Added extended information for ID = %s", key)
                
                #THIS IS SOLELY FOR DEBUGGING PURPOSES
                self.logger_MAL.debug("DUMPING ALL AVAILIBLE DATA")
                self.logger_MAL.debug("MAL_ID: %s",  key)
                self.logger_MAL.debug(" -- MAL_TITLE: %s",  extra_info[key]['series_title'])
                self.logger_MAL.debug(" -- MAL_SYNONYMS: %s",  extra_info[key]['series_synonyms'])
                self.logger_MAL.debug(" -- MAL_TYPE: %s",  extra_info[key]['series_type'])
                self.logger_MAL.debug(" -- MAL_EPISODES: %s",  extra_info[key]['series_episodes'])
                self.logger_MAL.debug(" -- MAL_STATUS: %s",  extra_info[key]['series_status'])
                self.logger_MAL.debug(" -- MAL_START: %s",  extra_info[key]['series_start'])
                self.logger_MAL.debug(" -- MAL_END: %s",  extra_info[key]['series_end'])
                self.logger_MAL.debug(" -- MAL_IMAGE: %s",  extra_info[key]['series_image'])
                self.logger_MAL.debug(" -- USER_ID: %s",  extra_info[key]['my_id'])
                self.logger_MAL.debug(" -- USER_WATCHED_EPISODES: %s",  extra_info[key]['my_watched_episodes'])
                self.logger_MAL.debug(" -- USER_START_DATE: %s",  extra_info[key]['my_start_date'])
                self.logger_MAL.debug(" -- USER_FINISHED_DATE: %s",  extra_info[key]['my_finish_date'])
                self.logger_MAL.debug(" -- USER_SCORE: %s",  extra_info[key]['my_score'])
                self.logger_MAL.debug(" -- USER_STATUS: %s",  extra_info[key]['my_status'])
                self.logger_MAL.debug(" -- USER_REWATCHING: %s",  extra_info[key]['my_rewatching'])
                self.logger_MAL.debug(" -- USER_REWATCHING_EP: %s",  extra_info[key]['my_rewatching_ep'])
                self.logger_MAL.debug(" -- USER_LAST_UPDATED: %s",  extra_info[key]['my_last_updated'])
                self.logger_MAL.debug(" -- USER_TAGS: %s",  extra_info[key]['my_tags'])
            except Exception as e:
                self.logger_MAL.warn("Unable to add ID = %s",  key)
                self.logger_MAL.warn("Error Message: %s",  e)
        
    @pyqtSlot(str,str)
    def __download_complete_slot(self, filename, class_name):
        """
        Connected to the NetworkHandler's download_complete_signal.
        """
        self.logger_MAL.info("== Download of %s complete", filename)
        if (filename == self.config["MAL"]["media_list_path"]):
            self.logger_MAL.debug(" -- Sending to parse %s",
                                self.config["MAL"]["media_list_path"])
            self.__parse_media_list(filename)
        elif (filename == self.config["MAL"]["search_list_path"]):
            self.logger_MAL.debug(" -- Sending to parse %s",
                                self.config["MAL"]["search_list_path"])
            self.__parse_search_list(filename)
        elif (filename ==  self.config["MAL"]["image_path"]
                + self.editing_item_id + ".jpeg"):
            self.display_image_signal.emit()
        else:
            self.logger_MAL.warning(
                    " -- Program does not know what to do with %s", filename)
                    
    @pyqtSlot(str)
    def __parse_complete_slot(self, filename):
        """
        Connected to the XMLHandler's parse_comlpete_signal.
        Emits a signal that either the media_list or the search_list_path
        is complete
        """
        self.logger_Host.info("== Parse (%s) complete", filename)
        #self.display_label_signal.emit(
         #                       "--> Parsing complete (" + filename + " )<--")
        if (filename == self.config["MAL"]["media_list_path"]):
            self.refresh_complete_signal.emit()
        elif (filename == self.config["MAL"]["search_list_path"]):
            self.seach_complete_signal.emit()
