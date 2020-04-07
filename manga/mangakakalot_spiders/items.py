# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AuthorItem(scrapy.Item):

    author_name = scrapy.Field()
    author_status = scrapy.Field()
    author_url = scrapy.Field()

    def __str__(self):
        return self['author_name']


class TranslatorItem(scrapy.Item):

    translator_name = scrapy.Field()
    translator_status = scrapy.Field()
    translator_url = scrapy.Field()

    def __str__(self):
        return self['translator_name']


class TagItem(scrapy.Item):
    type_name = scrapy.Field()

    def __str__(self):
        return self['type_name']


class TagItem(scrapy.Item):
    tag_type = scrapy.Field()
    tag_name = scrapy.Field()

    def __str__(self):
        return self['tag_name']


class SourceItem(scrapy.Item):

    source_name = scrapy.Field()
    url_expression = scrapy.Field()

    def __str__(self):
        return self['source_name']


class ExternalResourceItem(scrapy.Item):
    RESOURCE_TYPES = [
        ('Scrapable Web Page', 'Scrapable Web Page'),
        ('Static Resource', 'Static Resource'),
    ]

    resource_type = scrapy.Field()
    resource_short_name = scrapy.Field()
    url_expression = scrapy.Field()
    resource_processing_script = scrapy.Field()

    def __str__(self):
        return self['url_expression']
    

class AlternateNameItem(scrapy.Item):

    language = scrapy.Field()
    characters = scrapy.Field()
    alternate_name = scrapy.Field()

    def __str__(self):
        return self['alternate_name']


class MangaItem(scrapy.Item):
    STATUSES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed')
    ]

    manga_name = scrapy.Field()
    alternate_names = scrapy.Field()
    manga_year = scrapy.Field()
    chapter_sources = scrapy.Field()
    manga_status = scrapy.Field()
    original_publisher = scrapy.Field()
    banner_image_url = scrapy.Field()
    views = scrapy.Field()
    description = scrapy.Field()
    manga_authors = scrapy.Field()
    manga_translators = scrapy.Field()
    tags = scrapy.Field()
    added_on = scrapy.Field()
    updated_on = scrapy.Field()
    chapters = scrapy.Field()

    def __str__(self):
        return self['manga_name']


class ChapterItem(scrapy.Item):
    user = scrapy.Field()
    chapter_number = scrapy.Field()
    chapter_name = scrapy.Field()
    views = scrapy.Field()
    updated_on = scrapy.Field()
    url = scrapy.Field()
    external_sources = scrapy.Field()
    pages = scrapy.Field()    

    def __str__(self):
        return self['manga'].manga_name + ' - ' + str(self.chapter_number)


class EventItem(scrapy.Item):
    event_name = scrapy.Field()
    event_type = scrapy.Field()
    event_url = scrapy.Field()
    event_banner_image_url = scrapy.Field()
    event_description = scrapy.Field()
    affected_mangas = scrapy.Field()
    affected_users = scrapy.Field()
    affected_tags = scrapy.Field()

    def __str__(self):
        return self['event_name']


class PageItem(scrapy.Item):
    page_number = scrapy.Field()
    source_image_url = scrapy.Field()
    external_sources = scrapy.Field()    

    def __str__(self):
        return self['chapter'].__str__() + ' - ' + str(self['page_number'])

