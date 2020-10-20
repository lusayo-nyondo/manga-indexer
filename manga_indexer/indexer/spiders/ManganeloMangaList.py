from scrapy import Spider, Request

from manga_indexer.indexer.spiders import BaseMangaListSpider

from manga_indexer.indexer.parsers.sites import (
    ManganeloMangaPageParser,
    ManganeloMangaParser,
    ManganeloMangaPager
)

class MangakakalotSpider(BaseMangaListSpider):
    name = 'ManganeloMangaList'

    def _set_start_url(self):
        return 'https://manganelo.com/genre-all'
    
    def _set_parsers(self):
        self.Pager = ManganeloMangaPager
        self.MangaPageParser = ManganeloMangaPageParser
        self.MangaParser = ManganeloMangaParser
