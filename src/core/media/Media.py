__author__="dvorak"
__date__ ="$Jan 18, 2012 6:43:58 PM$"
import logging
class Media:
    """
    Base class for all media classes. Defines abstract members and functions.
    """
    __title = ""
    __image_url = None
    def __init__(self):
        self.logger_anime_handler = logging.getLogger("Media")
        self.logger_anime_handler.debug(" === Media::__init__ ===")

    def get_title(self):
        """
        Return title of media
        """
        return self.__title
    def set_title(self, title):
        """
        Set title of media
        """
        self.__title = title

    def get_image_url(self):
        """
        Return image url of media. None if it does not exist
        """
        return self.__image_ur
    def set_image_url(self, image_url):
        """
        Set the image url of the media.
        """
        self.__image_url = image_url

    def to_xml(self):
        """
        Returns an XML representation of the object. This NEEDS to be overridden
        by the subclass.
        """
        raise NotImplementedError