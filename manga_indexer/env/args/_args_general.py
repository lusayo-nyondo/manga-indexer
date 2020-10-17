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
            'A complete list of sites can be found at: https://github.com/neet-lord/manga-indexer/docs/supported_sites.lst'
        )
    )

    args.add_argument(
        '-e',
        '--use-estate',
        dest='use_estate',
        action='store_true',
        help=(
            'Create or use a tracked indexing project.\r\n'
            'This is useful if, for example, you only want you update your already existing index records\r\n'
            'to fetch new manga rather than index the entire site.'
        )
    )
