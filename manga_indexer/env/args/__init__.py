import argparse

from ._args_general import _args_general
from ._args_downloading import _args_downloading

parser = argparse.ArgumentParser(
    prog='manga-indexer',
    description=(
        'This is a tool for indexing manga websites in order to'
        'gather a complete list of manga that are available on that site.'
    )
)

_args_general(parser)
_args_downloading(parser)

