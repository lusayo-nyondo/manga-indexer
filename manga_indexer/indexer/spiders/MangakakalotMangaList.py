from scrapy import Spider, Request

from manga_indexer.indexer.spiders import BaseMangaListSpider

from manga_indexer.indexer.parsers.sites import (
    MangakakalotMangaPager,
    MangakakalotMangaPageParser,
    MangakakalotMangaParser
)

class MangakakalotSpider(BaseMangaListSpider):
    name = 'MangakakalotMangaList'

    def __init__(self,
        sitename,
        spider_instance=None,
        export_dir='./data',
        log_dir='./logs',
        **kwargs
    ):
        BaseMangaListSpider.__init__(
            self,
            sitename,
            spider_instance=None,
            export_dir='./data',
            log_dir='./logs',
            **kwargs
        )

        self._start_url = self.__set_start_url()
        self.__set_parsers()

    def __set_start_url(self):
        return 'https://mangakakalot.com/manga_list'
    
    def __set_parsers(self):
        self.Pager = MangakakalotMangaPager
        self.MangaPageParser = MangakakalotMangaPageParser
        self.MangaParser = MangakakalotMangaParser
