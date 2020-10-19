def _args_downloading(parser):

    args = parser.add_argument_group('Downloading options')

    args.add_argument(
        '-f',
        '--format',
        type=str,
        dest='format',
        default='json',
        choices=[
            'json',
            'xml',
            'csv'
        ],
        help='Specify an output format.'
    )

    args.add_argument(
        '-o',
        '--output',
        dest='output',
        type=str,
        help=(
            'Specify an output file.'
        )
    )

    args.add_argument(
        '-p',
        '--proxy-list',
        dest='proxy_list',
        type=str,
        help=(
            'Specify a file from which to read a set of rotating proxies.'
        )
    )
