
from argparse import ArgumentParser

def FeelsParser() -> ArgumentParser:
    parser:ArgumentParser = ArgumentParser(
        prog='Feels Kuna Man',
        description='A simple program to analyze emotions in music with Spotify\'s API'
    )

    # the URL pointing to Spotify data
    parser.add_argument(
        'url',
        default='',
        type=str
    )

    # indicates how many songs to take from a playlist. -1 means take all (up to 100)
    parser.add_argument(
        '--num',
        default=-1,
        type=int
    )

    # display info
    parser.add_argument(
        '--print',
        action='store_true',
        default=False
    )

    # displays the item(s)
    parser.add_argument(
        '--plot',
        help='creates a plot to visualize results',
        action='store_true'
    )

    # normalizes vectors when plotting
    parser.add_argument(
        '--normalize',
        help='normalizes emotives when plot is set',
        action='store_true'
    )

    return parser
