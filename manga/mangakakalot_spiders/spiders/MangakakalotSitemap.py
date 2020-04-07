# -*- coding: utf-8 -*-
import datetime
import json
import sys
import traceback

#from ..
#from mangakakalot_spiders import MangaItem
from ..items import *
from scrapy.utils.serialize import ScrapyJSONEncoder


class MangakakalotSitemapSpider(scrapy.spiders.SitemapSpider):
    name = 'MangakakalotSitemap'
    allowed_domains = ['mangakakalot.com', 'manganelo.com']

    sitemap_rules = [
        ('/manga/', 'process_fetched_manga'),
    ]

    error_log_folder = 'data/error_logs/'
    successful_output_file_folder = 'data/results_successful/'
    failed_output_file_folder = 'data/results_failed/'

    fatal_error_log = ''
    successful_output_file = ''
    failed_output_file = ''

    sitemap_urls = ['https://www.mangakakalot.com/sitemap.xml']
    sitemap_follow = ['sitemap_']

    spider_instance = None

    def closed(self):
        follow_up_command = 'python3 manga_updater.py'

    def process_fetched_manga(self, response):
        try:
            if (self.spider_instance == None):
                self.spider_instance = 'temp_mangakakalot_sitemap_' + str(datetime.datetime.utcnow().timestamp())

            self.successful_output_file = self.successful_output_file_folder + self.spider_instance + '.json'
            self.failed_output_file = self.failed_output_file_folder + self.spider_instance + '.json'
            self.fatal_error_log = self.error_log_folder + self.spider_instance + '.log'

            self.parse_manga(response)
            
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)

            exc_details = ''

            for line in lines:
                exc_details += '\t' + line + '\r\n'

            timestamp = datetime.datetime.utcnow()
            log_details = '[ERROR: ' + str(timestamp) + ']\r\n'
            log_details += exc_details

            log = open(self.fatal_error_log, "a+")
            log.write(log_details)
            log.close()

    def parse_manga(self, response):
        # This method will gather all of the necessary HTML elements
        # that contain all of the necessary manga details.
        # After that, it will pass this information to a detail gathering
        # method that will create a data structure (MangaItem object) that
        # contains the manga's information.

        # Get the parent HTML element(s) that
        # contain all of the relevant information.
        info_div = response.css('.manga-info-top')
        summary_div = response.xpath('//*[@id="noidungm"]')
        chapters_div = response.css('.chapter-list')

        # Aggregate the parent HTML elements into
        # one memory reference.
        details_response = {
            'manga_details': info_div,
            'manga_summary': summary_div
        }

        # Pass the variable above to the method that builds
        # a MangaItem object.
        manga_details = ''
        try:
            manga_details = self.get_manga_overview(details_response)
            # For manga kakalot spiders, I can safely say that the
            # chapter overview is on the same page as the manga overview.
            chapter_sources = self.get_chapter_sources(response)
            manga_details['chapter_sources'] = chapter_sources
            
            # Regardless of recording the chapter overview page, we still
            # record the pages for each individual chapter.
            chapters = self.gather_external_chapter_source_urls(chapters_div)
            manga_details['chapters'] = chapters

        except:
            if manga_details is None:
                raise
            else:
                _encoder = ScrapyJSONEncoder()

                # Encode the MangaItem object as JSON.
                json_encoded = _encoder.encode(manga_details)

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

                return

        # Initialize an encoder that will convert the MangaItem object
        # into serializable JSON.
        _encoder = ScrapyJSONEncoder()

        # Encode the MangaItem object as JSON.
        json_encoded = _encoder.encode(manga_details)

        # Serialize the JSON of the MangaItem built
        file = open(self.successful_output_file, 'a+')
        file.write(json.dumps(json_encoded, indent=4) + ",\r\n")
        file.close()

        # Print output to the console. Only enable for debugging purposes
        # because it slows down the spider.
        # print(json.dumps(json_encoded, indent=4))

    def get_chapter_sources(self, response):
        chapter_sources = list()
        chapter_sources.append(response.url)

        return chapter_sources
    
    def get_manga_overview(self, details_response):
        # this method will gather all of the necessary parameters
        # for a particular manga. It will have the following

        info_div = details_response['manga_details']
        summary_div = details_response['manga_summary']

        # Initialize items for storing authors, tags, and translators details

        authors = self.gather_author_list(info_div)
        tags = self.gather_tag_list(info_div)
        translators = self.gather_translator_list(info_div)

        manga_details = self.gather_manga_details(info_div, summary_div)

        manga = self.build_manga(manga_details, authors, translators, tags)

        self.validate_manga(manga)

        return manga

    def gather_author_list(self, info_div):
        list_items = info_div.css('.manga-info-text li')
        author_items = list()

        for list_item in list_items:
            text = list_item.css("::text").get()

            if text is None:
                continue

            text = text.lower()

            if text.__contains__('author(s)'):
                # This is an author listing item
                author_list = list_item.css('a')

                for author in author_list:
                    author_item = AuthorItem()

                    author_item['author_name'] = author.css('::text').get()
                    author_item['author_url'] = 'https://www.mangahive.com/authors/' + author_item['author_name']

                    author_items.append(author_item)

        return author_items

    def gather_translator_list(self, info_div):
        return list()

    def gather_tag_list(self, info_div):
        list_items = info_div.css('.manga-info-text li')
        tag_items = list()

        for list_item in list_items:
            text = list_item.css("::text").get()

            if text is None:
                continue

            text = text.lower()

            if text.__contains__('genres'):
                # This is an author listing item
                tag_list = list_item.css('a')

                for tag in tag_list:
                    tag_item = TagItem()
                    tag_item['tag_type'] = 'mangakakalot_tag'
                    tag_item['tag_name'] = tag.css('::text').get()

                    tag_items.append(tag_item)

        return tag_items

    def gather_manga_details(self, info_div, summary_div):

        exception_list = list()

        manga_item: MangaItem = MangaItem()
        manga_item['manga_name'] = info_div.css('li h1::text').get()
        manga_item['alternate_names'] = self.gather_alternate_names(info_div)
        manga_item['manga_year'] = self.gather_manga_year(info_div)
        manga_item['manga_status'] = self.gather_manga_status(info_div)
        manga_item['original_publisher'] = self.gather_original_publisher(info_div)
        manga_item['banner_image_url'] = self.gather_banner_image_url(info_div)
        manga_item['description'] = self.gather_manga_summary(summary_div)
        manga_item['added_on'] = datetime.datetime.now()
        manga_item['updated_on'] = self.gather_last_updated(info_div)

        return manga_item

    def gather_manga_detail(self, action, method, descriptor, html_node, output_object, exception_list):
        try:
            output_object[descriptor] = method(html_node)
            return output_object
        except:
            exception_detail = {
                'action': action,
                'exception_details': sys.exc_info()
            }

            exception_list.append(exception_detail)

    def gather_alternate_names(self, candidate_list_div):
        candidate_list = candidate_list_div.css('li .story-alternative::text').get()

        if candidate_list == None:
            return

        candidate_list = candidate_list.split(":")
        candidate_list.pop(0)
        candidate_list = candidate_list[0].split(';')

        alternate_names = list()

        for item in candidate_list:
            if item is None:
                continue

            alternate_name = AlternateNameItem()
            alternate_name['alternate_name'] = item

            alternate_names.append(alternate_name)

        return alternate_names

    def gather_banner_image_url(self, candidate_div):
        return candidate_div.css(".manga-info-pic img::attr('src')").get()

    def gather_manga_year(self, candidate_div):
        # mangakakalot does not record manga year
        return None

    def gather_manga_status(self, candidate_div):
        list_items = candidate_div.css('li')

        for list_item in list_items:
            text_nodes = list_item.css('::text').getall()

            if text_nodes is None:
                continue

            for text in text_nodes:
                text_str = text.strip()

                if text_str == '':
                    continue

                if text.lower().__contains__('status: '):
                    split = text.split(':')
                    split = split.pop(0)

                    status = split.strip()

                    return status

    def gather_original_publisher(self, candidate_div):
        return None

    def gather_manga_summary(self, candidate_div):
        text_nodes = candidate_div.css('::text').getall()
        description = ''

        return text_nodes[2]

    def gather_last_updated(self, candidate_div):
        list_items = candidate_div.css('li')

        for list_item in list_items:
            last_updated = self.gather_text_node_with_label(list_item, 'last updated : ')

            if last_updated == None:
                continue

            return last_updated

        return None

    def gather_text_node_with_label(self, parent_node, label_str):
        text_nodes = parent_node.css('::text').getall()

        if text_nodes is None:
            return None

        for text in text_nodes:
            text_str = text.strip()

            if text_str == '':
                continue

            if text.lower().__contains__(label_str):
                split = text_str.split(':')
                split.pop(0)

                result = ':'.join(split)

                return result

        return None

    def build_manga(self, manga_details, authors, translators, tags):
            manga_details['manga_authors'] = authors
            manga_details['manga_translators'] = translators
            manga_details['tags'] = tags

            return manga_details

    def validate_manga(self, manga_details):
        # Check if the scraper has populated all of the necessary fields. If it hasn't dump the
        #  manga details fetched to a common file, and try to provide a reason for why
        # this manga failed its basic scraper check.

        return True

    def gather_external_chapter_source_urls(self, chapters_overview_div):
        chapter_elements = chapters_overview_div.css('.row span:first-of-type')
        div = chapter_elements.get()

        chapter_items = list()

        for chapter_element in chapter_elements:
            resp_chapter_urls = list()
            
            chapter_href = chapter_element.css("a::attr('href')").get()

            resp_chapter_urls.append(chapter_href)
            
            resp_chapter_number = chapter_href.split(':')[-1].strip().split('_')[-1]
            
            resp_chapter_title = chapter_element.css("a::text").get()
            
            chapter_item = ChapterItem()

            chapter_item['url'] = chapter_href
            chapter_item['external_sources'] = resp_chapter_urls
            chapter_item['chapter_name'] = resp_chapter_title
            chapter_item['chapter_number'] = resp_chapter_number

            chapter_items.append(chapter_item)

        return chapter_items

