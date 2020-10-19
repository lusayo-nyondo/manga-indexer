import sys, os

from manga_indexer.settings import SUPPORT_ROOT


from manga_indexer.env.args import parser
args = parser.parse_args()

BOT_NAME = 'manga_indexer'

SPIDER_MODULES = ['indexer.spiders']
NEWSPIDER_MODULE = 'indexer.spiders'


USER_AGENT = 'Mozilla/5.0'
ROBOTSTXT_OBEY = True

#DOWNLOAD_DELAY = 3
#CONCURRENT_REQUESTS_PER_DOMAIN = 16

DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

ITEM_PIPELINES = {
    'indexer.pipelines.MangaIndexerPipeline': 630,
}


ROTATING_PROXY_LIST_PATH = None

if args.proxy_list_path:
    ROTATING_PROXY_LIST_PATH = args.proxy_list_path
else:
    ROTATIING_PROXY_LIST_PATH = os.path.join(
        SUPPORT_ROOT,
        'proxies.txt'
    )

ROTATING_PROXY_PAGE_RETRY_TIMES = 10