#-------------------------------------------------------------------------------
# Name:        XMLHandler
# Purpose:
#
# Author:      HP
#
# Created:     31-12-2011
# Copyright:   (c) HP 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import logging
import configparser
import xml.etree.ElementTree as etree
import codecs

from PyQt5.QtCore import *


#from core import Anime

class XMLHandler(QThread):
    parse_complete_signal = pyqtSignal(str, name="parse_complete_signal")
    add_media_signal = pyqtSignal(str,  name="add_media_signal")
    parse_complete_extra_info = pyqtSignal (dict, name="parse_complete_extra_info")
    config = None
    def __init__(self, parent = None):
        super(XMLHandler, self).__init__(parent)
        self.logger_xml_handler = logging.getLogger("XMLHandler")
        self.logger_xml_handler.debug(" === XMLHandler::__init__ ===")
        # Read and assign config
        self.config = configparser.ConfigParser()
        try:
          self.config.readfp(open('./config.conf'))
          self.logger_xml_handler.debug(" -- Successfully opened config file")
        except:
          self.logger_xml_handler.error("Could not read ./config.conf")
    def run(self):
        self.logger_xml_handler.debug(" === XMLHandler::run ===")
    def parse_media_list(self, plugin_name, filename, media_list):
        """ Parses the anime_list.xml and creates the anime_list object. """
        self.logger_xml_handler.debug(" === XMLHandler::parse_anime_list ===")

        target_file = codecs.open(filename,mode='r',encoding='utf-8')
        tree = etree.parse(target_file)
        root = tree.getroot()
        self.__set_user_info(root.find('myinfo'))

        self.logger_xml_handler.info("=== Adding Anime ===")
        extra_information = {}
        for anime in root.findall(self.config[plugin_name]["xml_node_name"]):
            id = 0
            extra_information_items = {}
            for item in anime.getiterator():
                if (item.tag == self.config[plugin_name]["xml_id_text"]):
                    id = item.text
                    self.add_media_signal.emit(id)    # Create new media object
                else:
                    extra_information_items[item.tag] = item.text
            extra_information[id] = extra_information_items
        self.logger_xml_handler.debug(" -- Emitting parse_complete_signal")
        self.parse_complete_extra_info.emit(extra_information)
        self.parse_complete_signal.emit(filename)

    def parse_search_list(self, filename, anime_list):
        self.logger_xml_handler.debug(" === XMLHandler::parse_search_list ===")

        tree = etree.parse(filename)
        root = tree.getroot()

        english = ""
        synopsis = ""
        for anime in root.findall("entry"):
            for item in anime.getiterator():
                if (item.tag == "id"):
                    self.logger_xml_handler.debug(" -- Looking for: %s",
                                                 item.text)
                    if item.text in anime_list.anime_list:
                        self.logger_xml_handler.debug(
                                    " -- Found %s",
                                             anime_list.anime_list[item.text].
                                                                    get_title())
                        english = anime.find("english").text
                        synopsis = anime.find("synopsis").text
                        anime_list.anime_list[
                                        item.text].set_english_title(english)
                        anime_list.anime_list[
                                        item.text].set_synopsis(synopsis)
                        self.parse_complete_signal.emit(filename)

    def __set_user_info(self, element):
        self.logger_xml_handler.debug(" === XMLHandler::__set_user_info() ===")
        self.__user_info = {
                'id': element.find('user_id').text,
                'name': element.find('user_name').text,
                'watching': element.find('user_watching').text,
                'completed': element.find('user_completed').text,
                'onhold': element.find('user_onhold').text,
                'dropped': element.find('user_dropped').text,
                'plantowatch': element.find('user_plantowatch').text,
                'days_spent_watching':
                                element.find('user_days_spent_watching').text}
        self.logger_xml_handler.debug(" -- user_info: %s", self.get_user_info())

    def get_user_info(self):
        return self.__user_info

if __name__ == '__main__':
    print("Run pyhton_anime_tracker in root folder")
