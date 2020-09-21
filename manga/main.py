from scrapy import cmdline
import datetime
import os
import sys

from manga.settings import *
    
def start_crawling_job(crawler_name, instance_prefix, sitename):
    timestamp = datetime.datetime.utcnow().timestamp()
    spider_instance_name = instance_prefix + str(timestamp)

    export_dir = os.path.join(
        MANGA_DOWNLOAD_ROOT,
        sitename
    )

    log_dir = os.path.join(
        LOG_ROOT,
        sitename
    )

    log_dir = os.path.join(
        log_dir,
        spider_instance_name
    )

    output_file = os.path.join(
        export_dir,
        '{}.json'.format(
            spider_instance_name
        )
    )

    os.chdir(APPLICATION_ROOT)

    command_template = "scrapy\tcrawl\t" + \
        crawler_name + \
            '\t-s\tJOBDIR=data/crawls/{spider_instance_name}' + \
            '\t-a\tspider_instance={spider_instance_name}' + \
            '\t-a\tsitename={sitename}' + \
            "\t-a\tlog_dir={log_dir}" + \
            "\t-a\texport_dir={export_dir}" + \
            "\t-o\toutput_file={output_file}:json"

    start_spider_command = command_template.format(
        spider_instance_name=spider_instance_name,
        sitename=sitename,
        log_dir=log_dir,
        export_dir=export_dir,
        output_file=output_file
    )

    print(start_spider_command)

    cmdline.execute(start_spider_command.split('\t'))

if __name__ == '__main__':
    start_crawling_job('MangakakalotMangaList', 'mangakakalot_spider_run', 'mangakakalot.com')
