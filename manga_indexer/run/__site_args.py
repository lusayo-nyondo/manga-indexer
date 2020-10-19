sites = dict()

sites.setdefault(
    'mangakakalot.com',
    {
        'spider_name': 'MangakakalotMangaList',
        'process_instance_prefix': 'mangakakalot_spider_run',
        'sitename': 'mangakakalot.com'
    }
)

sites.setdefault(
    'manganelo.com',
    {
        'spider_name': 'ManganeloMangaList',
        'process_instance_prefix': 'manganelo_spider_run',
        'sitename': 'manganelo.com'
    }
)

sites.setdefault(
    'mangadex.org',
    {
        'spider_name': 'MangadexMangaList',
        'process_instance_prefix': 'mangadex_spider_run',
        'sitename': 'mangadex.org'
    }
)
