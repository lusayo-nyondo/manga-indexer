import datetime, scrapy

from ..items import *

class MangaParser:
    def parse_manga(self, response):
        # This method will gather all of the necessary HTML elements
        # that contain all of the necessary manga details.
        # After that, it will pass this information to a detail gathering
        # method that will create a data structure (MangaItem object) that
        # contains the manga's information.

        info_div = response.css('.manga-info-top')
        summary_div = response.xpath('//*[@id="noidungm"]')
        chapters_div = response.css('.chapter-list')
        details_response = {
            'manga_details': info_div,
            'manga_summary': summary_div
        }

        manga_details = self.get_manga_overview(details_response)

        chapters = self.gather_chapters(chapters_div)
        manga_details['chapters'] = chapters

        return manga_details

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
                    author_item['author_url'] = 'https://www.clickmanga.com/authors/' + author_item['author_name']

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
        print('Text nodes are: ', text_nodes)
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

    def gather_chapters(self, chapters_overview_div):
        chapter_elements = chapters_overview_div.css('.row span:first-of-type')
        div = chapter_elements.get()

        chapter_items = list()

        for chapter_element in chapter_elements:
            external_sources = list()
            
            chapter_href = chapter_element.css("a::attr('href')").get()

            resp_chapter_number = chapter_href.split(':')[-1].strip().split('_')[-1]
            resp_chapter_title = chapter_element.css("a::text").get()
            
            chapter_item = ChapterItem()
            
            chapter_item['url'] = chapter_href
            chapter_item['chapter_name'] = resp_chapter_title
            chapter_item['chapter_number'] = resp_chapter_number

            chapter_items.append(chapter_item)

        return chapter_items
