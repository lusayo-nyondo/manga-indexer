from scrapy.http import Response, Request

from manga_indexer.indexer.items import MangaItem

class BaseMangaParser:
    _document = None

    def __init__(self, response):
        assert isinstance(response, Response)
        self._document = response

    def parse_manga(self) -> MangaItem:
        """
        Build a MangaItem object that will be serialized to represent the manga.
        """
        title = self._get_title()
        description = self._get_description()
        alternate_names = self._get_alternate_names()
        tags = self._get_tags()
        status = self._get_status()
        authors = self._get_authors()

        url = self._get_url()

        manga_item: MangaItem = MangaItem()

        manga_item['title'] = title
        manga_item['description'] = description
        manga_item['tags'] = tags
        manga_item['alternate_names'] = alternate_names
        manga_item['authors'] = authors
        manga_item['status'] =  status
        manga_item['url'] = url
        
        return manga_item

    def _get_title(self) -> str:
        return ''

    def _get_status(self) -> str:
        return 'Unknown'
    
    def _get_tags(self) -> list:
        return list()

    def _get_alternate_names(self) -> list:
        return list()

    def _get_authors(self) -> list:
        return list()

    def _get_description(self) -> list:
        return list()
    
    def _get_url(self) -> str:
        return self._document.request.url

class BaseMangaPageParser:
    def __init__(self, response):
        assert isinstance(response, Response)
        self._document = response

    def _get_manga_on_page(self) -> list:
        """
        Fetch all of the urls for manga that are on this page.
        """
        
    def _get_page_url(self, page_number) -> str:
        return self._document.request.url
    

class BaseMangaPager:
    def __init__(
        self,
        response,
        manga_page_parser=None,
        manga_parser=None
    ):
        assert isinstance(response, Response)
        
        self._document = response
        self.__current_page = None
        self._page_list = None

        self.manga_parser = manga_parser
        self.manga_page_parser = manga_page_parser

    def _get_page_count(self) -> int:
        return len(self._get_page_list())

    def _get_page_list(self) -> list:
        return list()

