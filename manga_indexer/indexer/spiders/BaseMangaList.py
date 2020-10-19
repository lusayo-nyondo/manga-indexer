import os, sys, traceback, datetime, json

from scrapy import Spider, Request

class BaseMangaListSpider(Spider):
    name = 'BaseMangaList'
    
    def __init__(self,
        event_log='./events.log',
        process_log='./proc.log',
        output_file='./data.json',
        sitename=None,
        **kwargs
    ):
        
        self.__event_log = event_log
        self.__process_log = process_log

        self._start_url = self._set_start_url()
        self._set_parsers()

    def _set_start_url(self) -> str:
        """
        set the starting url
        """
    
    def _set_parsers(self) -> None:
        """
            Register parsers here.
        """

    def start_requests(self) -> None:       
        yield Request(
            url=self._start_url,
            callback=self.process_manga_list
        )

    def process_manga_list(self, response) -> Request:
        """ This method does three things:
                1. It fetches the total number of pages of manga.
                2. It generates URLs for requesting those pages.
                3. It yields a request object for each page.
        """

        pager = self.Pager(response)
        page_list = pager._get_page_list()

        for page in page_list:
            yield Request(
                url=page,
                callback=self.parse_manga_list_page
            )

    def parse_manga_list_page(self, response) -> Request:
        """ This method does two things:
                1. It fetches the urls for mangas from a particular manga page.
                2. It yields a request object for each individual manga.
        """
        page_parser = self.MangaPageParser(response)
        manga_urls = page_parser._get_manga_on_page()
        
        for manga_url in manga_urls:
            yield Request(
                url=manga_url,
                callback=self.process_fetched_manga
            )

    def process_fetched_manga(self, response):
        try:
            parser = self.MangaParser(response)
            manga = parser.parse_manga()

            yield manga
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)

            exc_details = ''

            for line in lines:
                exc_details += '\t' + line + '\r\n'

            timestamp = datetime.datetime.utcnow()

            log_details = '[ERROR: ' + str(timestamp) + ']\r\n'
            log_details += '\tWHILE TRYING TO FETCH THE URL: ' + response.request.url

            log_details += exc_details

            log = open(self.__event_log, "a+")
            log.write(log_details)
            log.close()
