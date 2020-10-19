# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MangaItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()

    def __str__(self):
        return self['title']

