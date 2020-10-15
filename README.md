# Manga Indexer

This is a scrapy based utility that is used to index entire websites at a time.

The point of the indexer is to arrive at a single json file, per manga, per site, that contains references to all of the chapters of that manga.

It is designed to detect new manga and new chapters efficiently.

Fetching the actual chapter is actually done through another package https://github.com/neet-lord/manga-py.git
