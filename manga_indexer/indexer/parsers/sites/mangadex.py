from scrapy.http import Request

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
        ).get()

        return title
    
    def _get_status(self) -> str:
        status = self._document.xpath(
            '/html/body/div[4]/div[2]'
            '/div/div/div[2]/div[10]/div[2]/text()'
        ).get()

        return status

    def _get_description(self) -> str:
        description = self._document.css(
            '#content.container div.card.mb-3 '
            'div.card-body.p-0 div.row.edit '
            'div.col-xl-9.col-lg-8.col-md-7 '
            'div.row.m-0.py-1.px-0.border-top:nth-child(12) '
            'div.col-lg-9.col-xl-10'
        ).get()

        return description

    def _get_tags(self) -> str:
        tags = self._document.css(
            '#content.container div.card.mb-3 div.card-body.p-0 '
            'div.row.edit div.col-xl-9.col-lg-8.col-md-7 '
            'div.row.m-0.py-1.px-0.border-top div.col-lg-9.col-xl-10 '
            '.badge::text'
        ).getall()

        return tags

    def _get_alternate_names(self) -> str:
        alternate_names = self._document.xpath(
            '/html/body/div[4]/div[2]'
            '/div/div/div[2]/div[2]'
            '/div[2]/ul/li/text()'
        ).getall()

        return alternate_names

    def _get_authors(self) -> str:
        authors = self._document.xpath(
            '/html/body/div[4]/div[2]/div'
            '/div/div[2]/div[(position() >= 2) and (position() <= 4)]'
            '/div[2]/a/text()'
        ).getall()

        return authors
    
    def _get_url(self) -> str:
        return self._document.request.url

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
        
