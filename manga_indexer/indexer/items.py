import scrapy

class MangaItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    alternate_names = scrapy.Field()
    tags = scrapy.Field()
    authors = scrapy.Field()
    status = scrapy.Field()
    description = scrapy.Field()
    chapters = scrapy.Field()

    def __str__(self):
        return self['title']

class ChapterItem(scrapy.Item):
    idx = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    
    def __str__(self):
        return self['url']
