import scrapy
import json
import sys
import os

from scrapy.utils.serialize import ScrapyJSONEncoder

PROJECT_ROOT = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        __file__
                    )
                )
            )
        )
    )
)

sys.path.append(PROJECT_ROOT)
print(sys.path)

from mangakakalot_spiders.items import *

class MangakakalotChapterPagesSpider(scrapy.Spider):
    name = 'MangakakalotChapterPagesSpider'

    chapter_id = None
    chapter_url = None

    def start_requests(self):
        if self.chapter_url == None or self.chapter_id == None:
            print('No start request or chapter id. Exiting scraper.')
            return
   
        yield scrapy.Request(
            url=self.chapter_url,
            callback=self.parse_chapter
        )

    
    def parse_chapter(self, response):

        pages = self.gather_page_details(response)
        chapter = Chapter.objects.get(id=self.chapter_id)

        for page_item in pages:
            page = Page.objects.get_or_create(
                chapter_id=self.chapter_id,
                page_number=page_item['page_number'],
                source_image_url=page_item['source_image_url'],
            )

            page = page[0]

            external_source = ExternalResource.objects.get_or_create(
                resource_type='Static Resource',
                resource_short_name='Manga Page',
                url_expression=page_item['external_sources'][0]
            )

            external_source = external_source[0]

            page.external_sources.add(external_source)

            page.save()


    def gather_page_details(self, response):
        images = response.css('#vungdoc img')

        pages = list()

        for image in images:
            resp_image_url = image.css('::attr(src)').get()
            resp_page_no = resp_image_url.split('/')[-1].strip().split('.')[0]
            resp_page_urls = list()
            resp_page_urls.append(resp_image_url)

            page_item = PageItem()

            page_item['page_number'] = resp_page_no
            page_item['source_image_url'] = resp_image_url
            page_item['external_sources'] = resp_page_urls

            pages.append(page_item)

        return pages