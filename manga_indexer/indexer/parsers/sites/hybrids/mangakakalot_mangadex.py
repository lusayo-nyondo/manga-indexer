from scrapy.http import Response

from manga_indexer.indexer.parsers.sites import (
    MangakakalotMangaParser,
    ManganeloMangaParser
)

class MangakakalotMangadexMangaParser:

    def __init__(self, document):
        assert isinstance(document, Response)
        self._document = document
    
    def parse_manga(self):
        if self._document.request.url.startswith('https://manganelo.com'):
            return ManganeloMangaParser(
                self._document
            ).parse_manga()
        elif self._document.request.url.startswith('https://mangakakalot.com'):
            return MangakakalotMangaParser(
                self._document
            ).parse_manga()
        else:
            raise ValueError('This parser does not recognize any of the urls provided.')

