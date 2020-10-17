import os

from scrapy.exporters import XmlItemExporter


class MangaIndexerPipeline(object):
    def process_item(self, item, spider):
        print('%s what we are now processings \n\n\n\n\n\n\n\n\nafasdfasdfasdfsadsfdf', item)
        return item

class PerMangaNameXmlExportPipeline(object):
    def open_spider(self, spider):
        self.manga_name_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.manga_name_to_exporter.values():
            exporter.finish_exporting()
            exporter.file_close()

    def _exporter_for_item(self, item, export_dir):
        manga_name = item['manga_name']

        file_name = os.path.join(
            export_dir,
            '{}.xml'.format(
                manga_name
            )
        )

        if manga_name not in self.manga_name_to_exporter:
            f = open(
                file_name.format(
                    manga_name
                ), 'wb')
            
            f.write(item)
            
            exporter = XmlItemExporter(f)
            exporter.start_exporting()
            
            self.manga_name_to_exporter[manga_name] = exporter

        return self.manga_name_to_exporter[manga_name]

    def process_item(self, item, spider):
        export_dir = os.path.join(
            spider.export_dir,
            spider.spider_instance
        )
        
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        exporter = self._exporter_for_item(item, export_dir)
        exporter.export_item(item)

        return item

