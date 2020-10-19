import os

from scrapy.exporters import XmlItemExporter

class MangaIndexerPipeline(object):
    def process_item(self, item, spider):
        return item
