import argparse
import os

tasks = [(x.split('.')[0]) for x in os.listdir('./tasks')]

def GetParser():
    parser = argparse.ArgumentParser(
        prog='Feels Kuna Man - test',
        description='A simple program to predict user emotions based off Spotify playlists'
    )

    # corresponds to a .json file in ./tasks
    parser.add_argument(
        '--task',
        default='kuna',
        type=str,
        choices=tasks
    )

    # indicates how many songs to take from a playlist. -1 means take all
    parser.add_argument(
        '--num',
        default=-1,
        type=int
    )

    # sets the seed for shuffling the playlist when --num is less than the total songs in a playlist
    parser.add_argument(
        '--seed',
        default=-1,
        type=int
    )

    return parser