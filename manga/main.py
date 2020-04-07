from scrapy import cmdline
import datetime
import os
import sys

def start_crawling_job(crawler_name, instance_prefix):
    timestamp = datetime.datetime.utcnow().timestamp()
    spider_instance_name = instance_prefix + str(timestamp)

    spiders_path = os.path.realpath(os.path.join(__file__, '../'))

    os.chdir(spiders_path)
    start_spider_command = "scrapy crawl " + crawler_name + " -s JOBDIR=data/crawls/" + spider_instance_name + ' -a spider_instance=' + spider_instance_name

    cmdline.execute(start_spider_command.split())

    water = ''

#start_crawling_job('MangakakalotSitemap', 'mangakakalot_sitemap_spiders')
start_crawling_job('MangakakalotMangaList', 'mangakakalot_mangalist_spiders')

#spiders_path = os.path.realpath(os.path.join(__file__, '../'))
#os.chdir(spiders_path)
#start_spider_command = "scrapy crawl MangakakalotMangaList -s JOBDIR=data/crawls/mangakakalot_mangalist_spiders1564652942.867156 -a spider_instance=mangakakalot_mangalist_spiders1564652942.867156"
#cmdline.execute(start_spider_command.split())
