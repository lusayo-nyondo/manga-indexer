import os, sys, traceback, datetime, json

from scrapy import Spider, Request
from scrapy.utils.serialize import ScrapyJSONEncoder

class BaseMangaListSpider(Spider):
    name = 'BaseMangaList'
    
    def __init__(self,
        sitename,
        spider_instance=None,
        export_dir='./data',
        log_dir='./logs',
        **kwargs
    ):
        
        self.__fatal_error_log = ''
        self.__process_log = ''
        self._start_url = self.__set_start_url()
        
        print('start url: {}'.format(self._start_url))
        input('just waiting for the rain to rain down')

        self.__set_start_url()
        self.__set_parsers()

        self.spider_instance = spider_instance

        if self.spider_instance == None:
            self.spider_instance = 'temp_mangalist_' + str(datetime.datetime.utcnow().timestamp())
        
        self.export_dir = export_dir
        self.log_dir = log_dir
        self.sitename = sitename

        self.prepare_logs()

    def __set_start_url(self) -> str:
        """
        set the starting url
        """
    
    def __set_parsers(self) -> None:
        """
            Register parsers here.
        """
    
    def prepare_logs(self) -> None:
        """ This prepares the filesystem environment for logging three pieces of information:
                1. The exceptions that occurred, resulting in it's failure to gather a particular manga.
                2. The manga that could not be gathered successfully, and why.
                3. The manga that has been gathered successfully.

        """
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

        self.__fatal_error_log = os.path.join(
            self.log_dir,
            'errors.log'
        )
        
        self.proc_log = os.path.join(
            self.log_dir,
            'proc.log'
        )

    def start_requests(self):       
        yield Request(
            url=self._start_url,
            callback=self.process_manga_list
        )

    def process_manga_list(self, response):
        """ This method does three things:
                1. It fetches the total number of pages of manga.
                2. It generates URLs for requesting those pages.
                3. It yields a request object for each page.
        """

        self.__set_parsers()

        pager = self.Pager(response)
        page_list = pager.__iter__()

        for page in page_list:
            yield Request(
                url=page,
                callback=self.parse_manga_list_page
            )

    def parse_manga_list_page(self, response):
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
            manga = parser.parse_manga(response)
            print('manga parsed successfully \n\n\n\n %s', manga)
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

            log = open(self.__fatal_error_log, "a+")
            log.write(log_details)
            log.close()

    def json_encode_manga_item(self, manga_details):
        _encoder = ScrapyJSONEncoder()
        json_encoded = _encoder.encode(manga_details)
        return json_encoded

