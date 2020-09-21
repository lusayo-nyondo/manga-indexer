import os, sys, traceback, datetime, json, scrapy
from .MangaParser import MangaParser

class MangakakalotMangaListSpider(scrapy.Spider):
    name = 'MangakakalotMangaList'
    
    fatal_error_log = ''
    process_log = ''

    sitemap_instance = None

    manga_list_start_url = 'https://mangakakalot.com/manga_list/'

    def __init__(self, sitename, spider_instance=None, export_dir='./data', log_dir='./logs', **kwargs):
        
        self.spider_instance = spider_instance

        if self.spider_instance == None:
            self.spider_instance = 'temp_mangakakalot_sitemap_' + str(datetime.datetime.utcnow().timestamp())
        
        self.export_dir = export_dir
        self.log_dir = log_dir
        self.sitename = sitename

        self.prepare_logs()

    def prepare_logs(self):
        """ This prepares the filesystem environment for logging three pieces of information:
                1. The exceptions that occurred, resulting in it's failure to gather a particular manga.
                2. The manga that could not be gathered successfully, and why.
                3. The manga that has been gathered successfully.

        """
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

        self.fatal_error_log = os.path.join(
            self.log_dir,
            'errors.log'
        )
        
        self.proc_log = os.path.join(
            self.log_dir,
            'proc.log'
        )

    def start_requests(self):       
        yield scrapy.Request(
            url=self.manga_list_start_url,
            callback=self.parse_manga_list_urls
        )

    def parse_manga_list_urls(self, response):
        """ This method does three things:
                1. It fetches the total number of pages of manga.
                2. It generates URLs for requesting those pages.
                3. It yields a request object for each page.
        """
        total_number_of_pages = int(response.css(".page_last::attr('href')").get().split('&')[-1].split('=')[-1])
        request_regex_url = 'https://mangakakalot.com/manga_list?type=latest&category=all&state=all&page='

        proc_params = 'Total number of pages: {n}'

        for x in range(total_number_of_pages):
            yield scrapy.Request(
                url=request_regex_url + str(x + 1),
                callback=self.parse_manga_list_page
            )

    def parse_manga_list_page(self, response):
        """ This method does two things:
                1. It fetches the urls for mangas from a particular manga page.
                2. It yields a request object for each individual manga.
        """
        manga_urls = response.css(".list-truyen-item-wrap > a:first-of-type::attr('href')").getall()

        for manga_url in manga_urls:
            yield scrapy.Request(
                url=manga_url,
                callback=self.process_fetched_manga
            )

    def process_fetched_manga(self, response):
        try:
            parser = MangaParser()
            manga = parser.parse_manga(response)
            
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

            log = open(self.fatal_error_log, "a+")
            log.write(log_details)
            log.close()

    def json_encode_manga_item(self, manga_details):
        _encoder = ScrapyJSONEncoder()
        json_encoded = _encoder.encode(manga_details)
        return json_encoded

    def log_failed_manga_scrape(self, manga_details):
        json_encoded = self.json_encode_manga_item(manga_details)

        details_gathered = '[REQUEST]:::' + response.url + '\r\n'
        details_gathered += '\t[TIMESTAMP]:::' + str(datetime.datetime.utcnow()) + '\r\n'
        details_gathered += '\t[DETAILS GATHERED]:::' + json_encoded + '\r\n'

        file = open(self.failed_output_file, 'a+')
        file.write(details_gathered)
        file.close()

        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)

        exc_details = ''

        for line in lines:
            exc_details += '\t\t' + line + '\r\n'

        timestamp = datetime.datetime.utcnow()
        log_details = '[ERROR PARSING MANGA WHILE REQUESTING FOR THE RESOURCE: ' + response.url + '\r\n'
        log_details += '\t[' + str(timestamp) + ']\r\n'
        log_details += exc_details

        log = open(self.failed_output_file + '.log', "a+")
        log.write(log_details)
        log.close()
    
    def record_successful_manga_scrape(self, manga_details):
        json_encoded = self.json_encode_manga_item(manga_details)

        # Serialize the JSON of the MangaItem built
        file = open(self.successful_output_file, 'a+')
        file.write(json.dumps(json_encoded, indent=4) + ",\r\n")
        file.close()

        # Print output to the console. Only enable for debugging purposes
        # because it severely slows down the spider.
        # print(json.dumps(json_encoded, indent=4))