
import argparse
import os
from typing import DefaultDict

def FeelsParser():
    parser = argparse.ArgumentParser(
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

    # sets the seed for shuffling the playlist when --num is less than the total songs in a playlist
    parser.add_argument(
        '--seed',
        type=int,
        default=-1
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

    # creates an interactive plot
    parser.add_argument(
        '--interactive',
        help='creates an interactive plot if plot is true',
        action='store_true'
    )

    # noramlizes values on plot
    parser.add_argument(
        '--normalize',
        help='normalizes values when plot is true',
        action='store_true'
    )

    return parser
