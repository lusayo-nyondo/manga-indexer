def _args_downloading(parser):

    args = parser.add_argument_group('Downloading options')

    args.add_argument(
        '-f',
        '--format',
        type=str,
        dest='format',
        default='json',
        help=(
            'Specify an output format. Supported formats are:\r\n'
            'json, xml, yaml'
        )
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
