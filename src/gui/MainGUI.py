__author__="dvorak"
__date__ ="$Dec 18, 2011 12:27:15 PM$"
import sys
import logging
import configparser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class MainGUI(QObject):
    display_label_signal = pyqtSignal(str, name="display_label")
    display_anime_signal = pyqtSignal()
    display_search_signal = pyqtSignal()
    display_image_signal = pyqtSignal()
    
    config = None
    anime_list_obj = None
    host_list = []
    
    # Editing item, just a temporary storage variable
    editing_item = None
    editing_item_id = ""
        
    def __init__(self, parent=None):
        super(MainGUI, self).__init__(parent)
        self.app = QApplication(sys.argv)
        self.__setup_logging()
        self.logger_gui.debug("== pyAniTrackGui::__init__ ==")

        # Read and assign config
        self.config = configparser.ConfigParser()
        try:
            self.config.read_file(open('./config.conf'))
            self.logger_gui.debug(" -- Successfully opened config file")
        except:
            self.logger_gui.error("Could not read ./config.conf")

        for plugin in self.config["General"]["plugins"].split(','):
            # Wow this is dirty
            # But at least it seems to work
            import_str = "from core.plugins import %s" % plugin
            exec(import_str)
            class_object = eval(plugin + "." + plugin + "()")
            self.host_list.append(class_object)
            self.logger_gui.info("++ Using %s", plugin)

        #Load the UI
        self.window = loadUi("ui/AnimeTracker_MainWindow.ui")

        # Setting up progressbar
        self.window.progressBar.setMaximum(100)
        self.window.progressBar.setMinimum(0)

        # Setting up tree widgets
        tree_header_labels = ["ID", "Name", "Score", "Status"]
        #/* watching_tree_widget*/
        self.window.watching_tree_widget.setColumnCount(4)
        self.window.watching_tree_widget.setHeaderLabels(tree_header_labels)
        self.window.watching_tree_widget.resizeColumnToContents(0)
        self.window.watching_tree_widget.resizeColumnToContents(1)
        self.window.watching_tree_widget.resizeColumnToContents(2)
        self.window.watching_tree_widget.resizeColumnToContents(3)
        self.window.watching_tree_widget.setSortingEnabled(True)

        #/* completed_tree_widget*/
        self.window.completed_tree_widget.setColumnCount(4)
        self.window.completed_tree_widget.setHeaderLabels(tree_header_labels)
        self.window.completed_tree_widget.resizeColumnToContents(0)
        self.window.completed_tree_widget.resizeColumnToContents(1)
        self.window.completed_tree_widget.resizeColumnToContents(2)
        self.window.completed_tree_widget.resizeColumnToContents(3)
        self.window.completed_tree_widget.setSortingEnabled(True)

        #/* plan_to_watch_tree_widget*/
        self.window.plan_to_watch_tree_widget.setColumnCount(4)
        self.window.plan_to_watch_tree_widget.setHeaderLabels(tree_header_labels)
        self.window.plan_to_watch_tree_widget.resizeColumnToContents(0)
        self.window.plan_to_watch_tree_widget.resizeColumnToContents(1)
        self.window.plan_to_watch_tree_widget.resizeColumnToContents(2)
        self.window.plan_to_watch_tree_widget.resizeColumnToContents(3)
        self.window.plan_to_watch_tree_widget.setSortingEnabled(True)

        #/* dropped_tree_widget*/
        self.window.dropped_tree_widget.setColumnCount(4)
        self.window.dropped_tree_widget.setHeaderLabels(tree_header_labels)
        self.window.dropped_tree_widget.resizeColumnToContents(0)
        self.window.dropped_tree_widget.resizeColumnToContents(1)
        self.window.dropped_tree_widget.resizeColumnToContents(2)
        self.window.dropped_tree_widget.resizeColumnToContents(3)
        self.window.dropped_tree_widget.setSortingEnabled(True)

        #/* on_hold_tree_widget*/
        self.window.on_hold_tree_widget.setColumnCount(4)
        self.window.on_hold_tree_widget.setHeaderLabels(tree_header_labels)
        self.window.on_hold_tree_widget.resizeColumnToContents(0)
        self.window.on_hold_tree_widget.resizeColumnToContents(1)
        self.window.on_hold_tree_widget.resizeColumnToContents(2)
        self.window.on_hold_tree_widget.resizeColumnToContents(3)
        self.window.on_hold_tree_widget.setSortingEnabled(True)

        # Editing tree widget
        self.window.editing_tree_widget.setColumnCount(2)
        editing_headers = ["Description", "Value"]
        self.window.editing_tree_widget.setHeaderLabels(editing_headers)

        self.__make_connections()

        self.window.show()
        sys.exit(self.app.exec_())

    def __setup_logging(self):
        self.logger_gui = logging.getLogger("MainGUI")

    def __make_connections(self):
        self.logger_gui.debug("== MainGUI::__make_connections ==")

        print (self.host_list)
        # MAL signals, made if MAL enabled in config
        for class_object in self.host_list:
            class_object.refresh_started_signal.connect(
                self.__refresh_started)
            class_object.refresh_failed_signal.connect(
                self.__refresh_failed)
            class_object.search_started_signal.connect(
                self.__search_started)
            class_object.search_failed_signal.connect(
                self.__search_failed)
            class_object.refresh_complete_signal.connect(
                self.__display_media_list_slot)
            # Signals for network_handle
            #class_object.network_handle.progress_signal.connect(
             #     self.__update_progress_bar_slot)
            #class_object.network_handle.download_complete_signal.connect(
             #     self.__download_complete_slot)
        
        # Gui signals
        self.window.connect(self.window.actionRefresh_List,
                            SIGNAL("triggered()"),
                            self.__refresh_media_list)
        self.window.connect(self.window.actionUpdate_MAL,
                            SIGNAL("triggered()"),
                            self.__update_mal)
        #self.display_label_signal.connect(self.__display_label_slot)
        #self.display_anime_signal.connect(self.__display_media_list_slot)
        self.display_search_signal.connect(self.__display_search_list_slot)
        self.display_image_signal.connect(self.__display_image_slot)
        self.window.watching_tree_widget.itemDoubleClicked.connect(
                                                self.__search_anime_on_click)
        self.window.completed_tree_widget.itemDoubleClicked.connect(
                                                self.__search_anime_on_click)
        self.window.plan_to_watch_tree_widget.itemDoubleClicked.connect(
                                                self.__search_anime_on_click)
        self.window.on_hold_tree_widget.itemDoubleClicked.connect(
                                                self.__search_anime_on_click)
        self.window.dropped_tree_widget.itemDoubleClicked.connect(
                                                self.__search_anime_on_click)
        self.window.editing_tree_widget.itemChanged.connect(
                                                    self.__edit_anime_on_change)

        # Signals for network_handle
        #self.network_handle.progress_signal.connect(
        #                                    self.__update_progress_bar_slot)
        #self.network_handle.download_complete_signal.connect(
        #                                        self.__download_complete_slot)

        # Signals for xml_handle
        #self.xml_handle.parse_complete_signal.connect(
        #                                        self.__parse_complete_slot)
        self.logger_gui.info("Major connections(Qt) made successfully")


    def __refresh_media_list(self):
        """ 
        Starts the refresh list using the object of the website
        that is selected on the GUI.
        """
        self.logger_gui.debug("== MainGUI::__refresh_media_list ==")

        # TODO
        # ONLY FOR ACTIVE PLUGIN
        self.host_list[0].refresh_media_list()
        
        # Clearing the widgets before filling them again
        self.window.watching_tree_widget.clear()
        self.window.completed_tree_widget.clear()
        self.window.plan_to_watch_tree_widget.clear()
        self.window.on_hold_tree_widget.clear()
        self.window.plan_to_watch_tree_widget.clear()
        self.window.editing_tree_widget.clear()
        self.window.synopsis_text_browser.clear()

    @pyqtSlot(str)
    def __refresh_started(self, filename):
        """ Slot that will display that the refresh has successfully started """
        self.__display_label_slot("Downloading"
                                + " " + filename + " init successfull")
                 
    @pyqtSlot(str)
    def __refresh_failed(self, filename):
        """ Slot that wil display that the refresh has failed """
        self.__display_label_slot("Downloading"
                                + " " + filename + " init unsuccessfull")

    def __refresh_search_list(self, title):
        """ 
        Starts the search subroutine list using the object of the website
        that is selected on the GUI.
        """
        self.logger_gui.debug("== pyAniTrackGui::refresh_search_list ==")

        # TODO
        # ONLY FOR ACTIVE PLUGIN
        self.host_list[0].refresh_search_list(title)
        
        self.window.editing_tree_widget.clear()
        self.window.synopsis_text_browser.clear()
                                
    @pyqtSlot(str)
    def __search_started(self, filename):
        """ Slot that will display that the refresh has successfully started """
        self.__display_label_slot("Downloading"
                                + " " + filename + " init successfull")
                 
    @pyqtSlot(str)
    def __search_failed(self, filename):
        """ Slot that wil display that the refresh has failed """
        self.__display_label_slot("Downloading"
                                + " " + filename + " init unsuccessfull")

    def __download_image(self):
        """
        Starts downloading the image of the editing anime. Gets called by
        __get_image if image does not already exist
        """
        self.logger_gui.debug("== pyAniTrackGui::__download_image ==")
        self.__display_label_slot("Downloading "
                                + self.config["General"]["image_path"]
                                + self.editing_item_id + ".jpeg")

        if (self.network_handle.download_file(
                        self.anime_list_obj.anime_list[
                                        self.editing_item_id].get_image_url(),
                        "",
                        self.config["General"]["image_path"]
                                 + self.editing_item_id + ".jpeg")):
            self.logger_gui.info("++ Download ('%s') init successfull",
                                self.config["General"]["image_path"]
                                + self.editing_item_id + ".jpeg")
            self.network_handle.start()
        else:
            self.logger_gui.critical("!! Download ('%s') init unsuccessfull",
                                self.config["General"]["image_path"]
                                      + self.editing_item_id + ".jpeg")

    def __parse_search_list(self, filename):
        """
        Starts parsing the downloaded search.xml. Automatically gets called
        after the search.xml has been successfully downloaded.
        * Called by __download_complete_slot
        """
        self.logger_gui.debug(" == MainGUI::__parse_search_list ==")
        self.logger_gui.info("++ Parse (%s) init successfull", filename)
        self.xml_handle.parse_search_list(filename, self.anime_list_obj)

    @pyqtSlot()
    def __display_media_list_slot(self):
        """
        Displays anime data on the GUI.
        """
        self.logger_gui.debug("== MainGUI::__display_media_list_slot ==")
        for key in self.host_list[0].media_list.keys():
            item = QTreeWidgetItem()
            item = QTreeWidgetItem(
                    self.window.watching_tree_widget.invisibleRootItem())
            """
            if (anime.get_watched_status() == "Watching"):
                item = QTreeWidgetItem(
                    self.window.watching_tree_widget.invisibleRootItem())
            elif (anime.get_watched_status() == "Completed"):
                item = QTreeWidgetItem(
                    self.window.completed_tree_widget.invisibleRootItem())
            elif (anime.get_watched_status() == "Dropped"):
                item = QTreeWidgetItem(
                    self.window.dropped_tree_widget.invisibleRootItem())
            elif (anime.get_watched_status() == "On Hold"):
                item = QTreeWidgetItem(
                    self.window.on_hold_tree_widget.invisibleRootItem())
            elif (anime.get_watched_status() == "Plan-to-watch"):
                item = QTreeWidgetItem(
                    self.window.plan_to_watch_tree_widget.invisibleRootItem())
            """
            print(self.host_list[0].media_list[key].get_title())
            title = self.host_list[0].media_list[key].get_title()
            score = self.host_list[0].media_list[key].get_score()
            status = self.host_list[0].media_list[key].get_status()
            item.setText(0, str(key))
            item.setText(1, title)
            item.setText(2, str(score))
            item.setText(3, status)

            # Just resizing the tree widgets
            self.window.watching_tree_widget.resizeColumnToContents(0)
            self.window.watching_tree_widget.resizeColumnToContents(1)
            self.window.watching_tree_widget.resizeColumnToContents(2)
            self.window.watching_tree_widget.resizeColumnToContents(3)

            self.window.completed_tree_widget.resizeColumnToContents(0)
            self.window.completed_tree_widget.resizeColumnToContents(1)
            self.window.completed_tree_widget.resizeColumnToContents(2)
            self.window.completed_tree_widget.resizeColumnToContents(3)

            self.window.plan_to_watch_tree_widget.resizeColumnToContents(0)
            self.window.plan_to_watch_tree_widget.resizeColumnToContents(1)
            self.window.plan_to_watch_tree_widget.resizeColumnToContents(2)
            self.window.plan_to_watch_tree_widget.resizeColumnToContents(3)

            self.window.on_hold_tree_widget.resizeColumnToContents(0)
            self.window.on_hold_tree_widget.resizeColumnToContents(1)
            self.window.on_hold_tree_widget.resizeColumnToContents(2)
            self.window.on_hold_tree_widget.resizeColumnToContents(3)

            self.window.plan_to_watch_tree_widget.resizeColumnToContents(0)
            self.window.plan_to_watch_tree_widget.resizeColumnToContents(1)
            self.window.plan_to_watch_tree_widget.resizeColumnToContents(2)
            self.window.plan_to_watch_tree_widget.resizeColumnToContents(3)

            self.window.dropped_tree_widget.resizeColumnToContents(0)
            self.window.dropped_tree_widget.resizeColumnToContents(1)
            self.window.dropped_tree_widget.resizeColumnToContents(2)
            self.window.dropped_tree_widget.resizeColumnToContents(3)

    @pyqtSlot()
    def __display_search_list_slot(self):
        """
        Displays the editing anime in the editing widget. Gets called
        automatically after the search list parsing is complete
        """
        self.logger_gui.debug(
                            "== pyAniTrackGui::__display_search_list_slot ==")

        #/* Disconnectiong itemChanged signal
        #* to allow population of the editing_tree_widget
        #* without the edit_anime_on_change slot being fired*/
        self.window.editing_tree_widget.itemChanged.disconnect(
                                                    self.__edit_anime_on_change)

        criteria = ["ID", "Title", "Type", "Episodes", "Watched Episodes",
                    "Score", "Status", "Start Date", "End Date"]
        values =[   self.editing_item_id,
                    self.anime_list_obj.anime_list[
                                self.editing_item_id].get_title(),
                    self.anime_list_obj.anime_list[
                                self.editing_item_id].get_type(),
                    self.anime_list_obj.anime_list[
                                self.editing_item_id].get_episodes(),
                    self.anime_list_obj.anime_list[
                                self.editing_item_id].get_watched_episodes(),
                    self.anime_list_obj.anime_list[
                                self.editing_item_id].get_score(),
                    self.anime_list_obj.anime_list[
                                self.editing_item_id].get_status(),
                    self.anime_list_obj.anime_list[
                                self.editing_item_id].get_start_date(),
                    self.anime_list_obj.anime_list[
                                self.editing_item_id].get_end_date()
                    ]

        for index, value in enumerate(values):
            item = QTreeWidgetItem(
                        self.window.editing_tree_widget.invisibleRootItem())
            item.setText(0, criteria[index])
            item.setText(1, str(values[index]))
            # THIS IF DOES NOT WORK TODO
            if (    criteria[index] == "Score" or
                    criteria[index] == "Watched Episodes"):
                item.setFlags(item.flags() | Qt.ItemIsEditable)

        # /* Resizing columns as needed */
        self.window.editing_tree_widget.resizeColumnToContents(0);
        self.window.editing_tree_widget.resizeColumnToContents(1);

        self.window.synopsis_text_browser.setText(
                                    self.anime_list_obj.anime_list[
                                        self.editing_item_id].get_synopsis())

        #/* Reconnecting the itemChanged signal and edit_anime_on_change slot */
        self.window.editing_tree_widget.itemChanged.connect(
                                                    self.__edit_anime_on_change)

        # Now that we're done displaying the data on the editing lists, lets
        # display the image.
        self.__get_image()

    def __get_image(self):
        """
        Will get the image, downloading it if neccesarry, else simply displaying
        the already downloaded image. Gets called after the synopsis and other
        information is already displayed. Called by __display_search_list_slot()
        """
        self.logger_gui.debug("== MainGUI::__get_image ==")
        image_file = QFile(self.config["General"]["image_path"]
                                + self.editing_item_id + ".jpeg")
        if (not image_file.exists()):
            self.__download_image()
        else:
            self.display_image_signal.emit()

    def __display_image_slot(self):
        """
        Will display the downloaded image. Gets called by the
        __download_complete slot.
        """
        self.logger_gui.debug("== MainGUI::__display_image_slot ==")
        scene = QGraphicsScene(self.window.graphicsView)
        image = QImage()
        image.load(self.config["General"]["image_path"]
                    + self.editing_item_id + ".jpeg")
        pix_map = QPixmap
        pix_map = pix_map.fromImage(image)
        pix_map = pix_map.scaled(self.window.graphicsView.size(),
                                 Qt.KeepAspectRatio, Qt.SmoothTransformation)
        scene.addPixmap(pix_map)
        self.window.graphicsView.setScene(scene)
        #self.window.graphicsView.show()

    @pyqtSlot(str)
    def __display_label_slot(self, message):
        """
        Slot to display message in statusbar, stays visable for 5s
        """
        self.window.statusbar.showMessage(message, 5000)

    @pyqtSlot(int)
    def __update_progress_bar_slot(self, progress):
        """
        Updates the progressbar, connected to the NetworkHandler's
        downloadProgress signal
        """
        self.logger_gui.debug("** Progress_Bar_Update: %s", progress)
        self.window.progressBar.setValue(progress)
        if (progress >= 100):
            self.display_label_signal.emit("--> Complete <--")

    @pyqtSlot(QTreeWidgetItem, int)
    def __search_anime_on_click(self, item, col):
        """
        Gets called by the doubleClicked() signal of the viewing widgets.
        Calls __refresh_search_list, with the title of the anime to be found
        as a parameter.
        """
        self.editing_item_id = item.text(0)
        self.__refresh_search_list(item.text(1))

    @pyqtSlot(QTreeWidgetItem, int)
    def __edit_anime_on_change(self, item, col):
        """
        Gets called by the itemChanged() signal of the editing_tree_widget.
        Will create and modify a object in the self.updating_anime_list class
        member.

        NOTE: This slot is connected and disconnected by the __parse_search_list
        function on every call. This allows the population of the
        editing_tree_widget without the slot being called 1024k times
        """
        self.logger_gui.debug("== MainGUI::__edit_anime_on_change")

        if self.editing_item_id not in self.updating_anime_list.anime_list:
            # Copy the anime being edited to the updating_anime_list
            self.updating_anime_list.anime_list[
                    self.editing_item_id] = self.anime_list_obj.anime_list[
                                                        self.editing_item_id]

        if (item.text(0) == "Score"):
            self.updating_anime_list.anime_list[
                            self.editing_item_id].set_score(item.text(1))
        elif (item.text(0) == "Watched Episodes"):
            self.updating_anime_list.anime_list[
                        self.editing_item_id].set_watched_episodes(item.text(1))


    def __update_mal(self):
        """
        test
        """

        self.logger_gui.debug("== MainGUI::__update_mal")
        host = "http://" + self.config["MAL"]["username"] 
        host += ":" + self.config["MAL"]["password"] + "@" + "myanimelist.net"
        for key, anime in self.updating_anime_list.anime_list.items():
            query = "/api/" + self.config["MAL"]["username"] +"/anime/update/" + key + ".xml"
            request =   "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n"
            request +=      "<entry>"
            request +=          "<episode>" + anime.get_watched_episodes() + "</episode>";

            #If watched_episodes = amount_of_episodes
            if (int(anime.get_watched_episodes()) == int(self.anime_list_obj.anime_list[key].get_episodes())):
                request +=      "<status>completed</status>"
            else:
                request +=      "<status>" + anime.get_watched_status().replace(" ", "").toLowerCase().strip() + "</status>"
            request +=          "<score>" + str(anime.get_score()) + "</score>"
            request +=      "\r\n</entry>"
            self.logger_gui.debug (" - XML: %s", request)
            if (self.network_handle.upload_file(host, query, request)):
                self.network_handle.start()
