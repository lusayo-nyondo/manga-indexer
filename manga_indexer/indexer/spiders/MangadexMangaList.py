from scrapy import Spider, Request

from manga_indexer.indexer.spiders import BaseMangaListSpider

from manga_indexer.indexer.parsers.sites import (
    MangadexMangaPager,
    MangadexMangaPageParser,
    MangadexMangaParser
)

class MangadexSpider(BaseMangaListSpider):
    name = 'MangadexMangaList'

    def _set_start_url(self):
        return 'https://mangadex.org/titles'
    
    def _set_parsers(self):
        self.Pager = MangadexMangaPager
        self.MangaPageParser = MangadexMangaPageParser
        self.MangaParser = MangadexMangaParser
