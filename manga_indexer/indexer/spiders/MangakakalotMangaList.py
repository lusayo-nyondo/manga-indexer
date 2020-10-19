from scrapy import Spider, Request

from manga_indexer.indexer.spiders import BaseMangaListSpider

from manga_indexer.indexer.parsers.sites import (
    MangakakalotMangaPager,
    MangakakalotMangaPageParser,
    MangakakalotMangaParser
)

class MangakakalotSpider(BaseMangaListSpider):
    name = 'MangakakalotMangaList'

    def _set_start_url(self):
        return 'https://mangakakalot.com/manga_list'
    
    def _set_parsers(self):
        self.Pager = MangakakalotMangaPager
        self.MangaPageParser = MangakakalotMangaPageParser
        self.MangaParser = MangakakalotMangaParser
