# Manga Indexer

This is a scrapy based utility that is used to index entire manga websites at a time.

It is designed to detect manga and it's attributes, then output it in a programmable format.

Attributes include:

+ Title
+ Tags
+ Authors
+ Description
+ Status
+ Alternate names

It is meant to be used in conjunction with another project that uses this information meaningfully.

Supported sites:
================
- [x] https://mangadex.org
- [x] https://manganelo.com
- [x] https://mangakakalot.com

> Full list of supported sites at: https://github.com/neet-lord/manga-indexer/blob/master/docs/supported_sites.md

Installation:
=============
> :information_source:  The project is still in the development phase, so it's kind of hacky.

    git clone https://github.com/neet-lord/manga-indexer.git
    
    cd manga-indexer

    python3 -m venv venv
    
    source venv/bin/activate

    python3 -m pip install requirements.txt

    
Basic Usage:
============
> Use manga-indexer to get a snapshot of https://mangakakalot.com: 
>
>       ./manga-indexer.py -s mangakakalot.com -o mangakakalot_site_snapshot.json
>
> By default, manga-indexer uses rotating proxies. However, you can disable that functionality to improve the speed of indexing.
>
>       ./manga-indexer.py -s manganelo.com -o manganelo_index.json --no-proxy
>
> You can also use different file formats:
>
>       ./manga-indexer.py -s mangadex.com -o mangadex_index.xml -f xml
>     
> You can find a more detailed user documentation at:
>  
> + https://github.com/neet-lord/manga-indexer/tree/master/docs/usage/getting_started.md

Developers:
===========

For developers, comments are your best friend. However, I will later include development tips when I feel like it.