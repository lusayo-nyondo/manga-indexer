from scrapy.http import Request

from manga_indexer.indexer.parsers import (
    BaseMangaParser,
    BaseMangaPageParser,
    BaseMangaPager
)
class MangakakalotMangaPageParser(BaseMangaPageParser):
    def _get_manga_on_page(self) -> list:
        return self._document.css(".list-truyen-item-wrap > a:first-of-type::attr('href')").getall()

    def _get_page_url(self, page_number) -> str:
        return self._document.request.url

class MangakakalotMangaParser(BaseMangaParser):
    def _get_title(self) -> str:
        title = self._document.css('.manga-info-text li h1::text').get()
        
        return title
    
    def _get_tags(self) -> str:
        tags = self._document.css(
            'html body div.container '
            'div.main-wrapper div.leftCol '
            'div.manga-info-top ul.manga-info-text '
            'li:nth-child(7) a::text'
        ).get()

        return tags

    def _get_description(self) -> str:
        description =  self._document.css(
            '//*[@id="noidungm"]'
        ).get().strip()

        return description

    def _get_alternate_names(self) -> str:
        try:
            alternate_names = self._document.css(
                'html body div.container '
                'div.main-wrapper div.leftCol '
                'div.manga-info-top ul.manga-info-text '
                'li h2.story-alternative'
            ).get().split(',')

            return alternate_names
        except:
            return list()
        
    def _get_authors(self) -> str:
        authors = self._document.css(
            'html body div.container '
            'div.main-wrapper div.leftCol '
            'div.manga-info-top ul.manga-info-text '
            'li:nth-child(2) a::text'
        ).getall()

        return authors

    def _get_status(self) -> str:
        status = self._document.xpath(
            '/html/body/div[1]/div[2]/div[1]/div[3]/ul/li[3]'
        ).get().split(':')[-1]

        return status
        
    def _get_url(self) -> str:
        return self._document.request.url

class MangakakalotMangaPager(BaseMangaPager):
    def _get_page_list(self):
        if self._page_list is None:

            total_number_of_pages = int(self._document.css(".page_last::attr('href')").get().split('&')[-1].split('=')[-1])
            page_format = 'https://mangakakalot.com/manga_list?type=latest&category=all&state=all&page={page}'

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
        return int(self._document.css('.panel_page_number .group_page .page_select').get())
        
