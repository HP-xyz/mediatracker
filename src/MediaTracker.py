__author__ = "dvorak"
__date__ = "$Dec 17, 2011 7:28:58 PM$"
import logging
import configparser


class MediaTracker:
    def __init__(self):
        self.__setup_logging()

        logging.info('== pyAniTrack Started ==')
        logging.debug("=== pyAniTrack INIT ===")

        self.config = configparser.ConfigParser()

        try:
            self.config.read_file(open('./config.conf'))
            logging.debug(" -- Successfully opened config file")
        except:
            logging.error("Could not read ./config.conf")

        if (self.config["General"]["GUI"] == "True"):
            logging.info(" ++ Starting GUI")
            self.start_gui()
        else:
            logging.info(" -- Starting without GUI")

    def __setup_logging(self):
        logging.basicConfig(
            filename='MediaTracker.log',
            level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M',
            filemode='a')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def start_gui(self):
        logging.debug(" == pyhton_anime_trackter::start_gui == ")
        from gui import MainGUI

        MainGUI.MainGUI()


if __name__ == "__main__":
    obj = MediaTracker()
