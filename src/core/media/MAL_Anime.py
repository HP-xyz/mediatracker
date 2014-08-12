__author__="dvorak"
__date__ ="$Dec 17, 2011 7:46:20 PM$"
from core.media import Media
class MAL_Anime(Media.Media):
    __SYNONYMS_DELIMETER = ';'
    __english_title = ""
    __synonyms = []
    __episodes = 0
    __score = 0
    __type = ""
    __status = ""
    __watched_episodes = 0
    __watched_status = ""
    __start_date = ""
    __end_date = ""
    __synopsis = ""
    def __init__(self):
        super(MAL_Anime, self).__init__()

    """
    Generic GET Functions
    ===========================
    """
    def get_english_title(self):
        return self.__english_title
    def get_synonyms(self):
        return self.__synonyms
    def get_episodes(self):
        return self.__episodes
    def get_watched_episodes(self):
        return self.__watched_episodes
    def get_score(self):
        return self.__score
    def get_type(self):
        return self.__type
    def get_status(self):
        return self.__status
    def get_watched_status(self):
        return self.__watched_status
    def get_start_date(self):
        return self.__start_date
    def get_end_date(self):
        return self.__end_date
    def get_synopsis(self):
        return self.__synopsis

    """
    Generic SET Functions
    ===========================
    """
    
    def set_english_title(self, english_title):
        self.__english_title = english_title
    def set_synonyms(self, synonyms):
        self.__synonyms = synonyms
    def set_episodes(self, episodes):
        self.__episodes = episodes
    def set_watched_episodes(self, watched_episodes):
        self.__watched_episodes = watched_episodes
    def set_score(self, score):
        self.__score = int(score)
    def set_type(self, type):
        self.__type = type
    def set_status(self, status):
        self.__status = status
    def set_watched_status(self, watched_status):
        self.__watched_status = watched_status
    def set_start_date(self, start_date):
        self.__start_date = start_date
    def set_end_date(self, end_date):
        self.__end_date = end_date
    def set_synopsis(self, synopsis):
        self.__synopsis = synopsis
    

if __name__ == "__main__":
    print ("Please run python_anime_tracker.py")
