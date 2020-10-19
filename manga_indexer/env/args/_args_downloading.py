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
