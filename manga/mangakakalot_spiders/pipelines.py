from scrapy.exporters import XmlItemExporter

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MangakakalotSpidersPipeline(object):
    def process_item(self, item, spider):
        return item

class PerMangaNameXmlExportPipeline(object):

    def open_spider(self, spider):
        self.manga_name_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.manga_name_to_exporter.values():
            exporter.finish_exporting()
            exporter.file_close()

    def _exporter_for_item(self, item):
        manga_name = item['manga_name']

        if manga_name not in self.manga_name_to_exporter:
            f = open('{}.xml'.format(manga_name), 'w+')
            exporter = XmlItemExporter()
            exporter.start_exporting()
            self.manga_name_to_exporter[manga_name] = exporter

        return self.manga_name_to_exporter[manga_name]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item

