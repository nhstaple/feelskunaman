import argparse
import os

tasks = [(x.split('.')[0]) for x in os.listdir('./tasks')]

def GetParser():
    parser = argparse.ArgumentParser(
        prog='Feels Kuna Man - test',
        description='A simple program to predict user emotions based off Spotify playlists'
    )

    parser.add_argument(
        '--task',
        default='honey',
        type=str,
        choices=tasks
    )

    parser.add_argument(
        '--num',
        default=-1,
        type=int
    )

    parser.add_argument(
        '--seed',
        default=-1,
        type=int
    )

    return parser