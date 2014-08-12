import logging

__author__="dvorak"
__date__ ="$Dec 17, 2011 8:21:47 PM$"
from core import Anime

class AnimeList:
    def __init__(self):
        self.logger_anime_list_handler = logging.getLogger("AnimeList")
        self.logger_anime_list_handler.debug("=== AnimeList::__init__ ===")
        self.anime_list = {}

    def add_anime(self, id, title, synonyms, episodes, score, type, status,
                    watched_episodes, watched_status, start_date, end_date,
                    image_url):
        if id not in self.anime_list:
            anime_obj = Anime.Anime(title, synonyms, episodes, score, type,
                                    status, watched_episodes, watched_status,
                                    start_date, end_date, image_url)
            self.logger_anime_list_handler.info("++ %s : %s", id,
                                                 anime_obj.get_title())
            self.anime_list[id] = anime_obj
        else:
            self.logger_anime_list_handler.info("** %s already in list", id)

    def add_complete_anime(self, anime_obj):
        self.logger_anime_list_handler.info("Adding complete anime %s",
                                            anime_obj.get_id())

    def add_search(self, id, anime):
        self.logger_anime_list_handler.debug("=== add_search === ")
        self.logger_anime_list_handler.debug(" -- " + anime.get_synopsis())
        self.anime_list = self.__quicksort(self.anime_list)
        self.anime_list[id].set_synonyms(anime.get_synonyms())
        self.anime_list[id].set_status(anime.get_status())
        self.anime_list[id].set_start_date(anime.get_start_date())
        self.anime_list[id].set_end_date(anime.get_end_date())
        self.anime_list[id].set_synopsis(anime.get_synopsis())

if __name__ == "__main__":
    print ("Please run python_anime_tracker.py")
