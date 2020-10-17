#!venv/bin/python3

from manga_indexer.env.args import parser
from manga_indexer.run import start_crawling_job

if __name__ == '__main__':
    args = parser.parse_args()
    start_crawling_job('MangakakalotMangaList', 'mangakakalot_spider_run', 'mangakakalot.com')
