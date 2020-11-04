from scrapy.http import Request

from lxml import etree as ET

from manga_indexer.indexer.items import ChapterItem

from manga_indexer.indexer.parsers import (
    BaseMangaParser,
    BaseMangaPageParser,
    BaseMangaPager
)

class MangadexMangaPageParser(BaseMangaPageParser):
    def _get_manga_on_page(self) -> list:
        mangas = self._document.css(".manga-entry .manga_title::attr('href')").getall()
        formatted_urls = list()
        
        for manga in mangas:
            formatted_urls.append(
                'https://mangadex.org{manga}'.format(
                    manga=manga
                )
            )

        return formatted_urls
    
    def _get_page_url(self, page_number) -> str:
        return self._document.request.url

class MangadexMangaParser(BaseMangaParser):
    def _get_title(self) -> str:
        title = self._document.css(
            '#content.container div.card.mb-3 '
            'h6.card-header.d-flex.align-items-center.py-2 '
            'span.mx-1::text'
        ).get().strip()

        return title
    
    def _get_status(self) -> str:
        status = ''

        try:
            status = self._document.xpath(
                '/html/body//div[contains(@class, \'edit\')]'
                '//div[contains(text(), \'Pub. status:\')]'
                '/../div[2]/text()'
            ).get().strip()
        except AttributeError:
            pass

        return status

    def _get_description(self) -> str:
        description = ''

        try:
            description = self._document.xpath(
                '/html/body//div[contains(@class, \'edit\')]'
                '//div[contains(text(), \'Description:\')]'
                '/../div[2]/text()'
            ).get().strip()
        except AttributeError:
            pass

        return description

    def _get_tags(self) -> str:
        tags = self._document.xpath(
            '/html/body//div[contains(@class, \'edit\')]'
            '//div[contains(text(), \'Demographic:\') '
            'or contains(text(), \'Genre:\') '
            'or contains(text(), \'Theme:\') '
            'or contains(text(), \'Format:\')]'
            '/../div[2]//a/text()'
        ).getall()

        return tags

    def _get_alternate_names(self) -> str:
        alternate_names = self._document.xpath(
            '/html/body//div[contains(@class, \'edit\')]'
            '//div[contains(text(), \'Alt name\')]'
            '/../div[2]//li/text()'
        ).getall()

        return alternate_names

    def _get_authors(self) -> str:
        authors = self._document.xpath(
            '/html/body//div[contains(@class, \'edit\')]'
            '//div[contains(text(), \'Author:\') '
            'or contains(text(), \'Artist:\')]'
            '/../div[2]/a/text()'
        ).getall()

        return authors

    def _get_url(self) -> str:
        return self._document.request.url

    def _get_chapters(self) -> list:
        chapters = list()

        chapters_nodes = self._document.xpath(
            '/html/body//div[contains(@class, \'chapter-row\')]'
            '//span[contains(@class, \'flag-gb\')]/../../div[2]/a'
        ).getall()

        chapters_nodes = chapters_nodes[::-1]

        n = len(chapters_nodes)

        for idx in range(n):
            node = ET.fromstring(chapters_nodes[idx])

            url = 'https://mangadex.org{}'.format(
                node.attrib['href']
            )
            
            name = node.text

            chapter = ChapterItem(
                idx=idx,
                name=name,
                url=url
            )

            chapters.append(chapter)

        return chapters


class MangadexMangaPager(BaseMangaPager):
    def _get_page_list(self):
        if self._page_list is None:

            element = self._document.css(
                '#content.container nav '
                'ul.pagination.justify-content-center '
                'li.page-item:last-child > a:nth-child(1)'
            )

            href = element.attrib['href']

            total_number_of_pages = int(href.split('/')[3])
            page_format = 'https://mangadex.org/titles/0/{page}'

            page_list = list()

            for x in range(total_number_of_pages):
                page_list.append(
                        page_format.format(
                        page=x+1
                    )
                )

            self.__page_list = page_list

        return self.__page_list

    def _get_current_page_number(self):
        return int(
            self._document.css(
                '#content.container nav '
                'ul.pagination.justify-content-center '
                'li.page-item.active'
            ).get()
        )
        
