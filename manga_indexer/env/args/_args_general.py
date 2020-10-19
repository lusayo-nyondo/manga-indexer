def _args_general(parser):

    args = parser.add_argument_group('General Options')

    args.add_argument(
        '-s',
        '--site',
        type=str,
        dest='site',
        default='https://mangakakalot.com',
        help=(
            'Specify a website that you want to index.\r\n'
            'The default is https://mangakakalot.com\r\n'
            'A complete list of sites can be found at: https://github.com/neet-lord/manga-indexer/blob/master/docs/supported_sites.md'
        )
    )

    args.add_argument(
        '-j',
        '--job-dir',
        dest='crawl_dir',
        help=(
            'Set a job dir for the scrapy job.\r\n'
            'This is useful if you want to resume the indexing at a later time.\r\n'
        )
    )

    args.add_argument(
        '-l',
        '--log-file',
        dest='log_file',
        help=(
            'Set an event log for the indexer.'
        )
    )

    args.add_argument(
        '-L',
        '--log-level',
        dest='log_level',
        default='DEBUG',
        choices=[
            'DEBUG',
            'INFO',
            'ERROR',
            'CRITICAL'
        ],
        help=(
            'Set a logging level for the scrapy spider.'
            'Note, this log is different from the general event log.'
        )
    )
