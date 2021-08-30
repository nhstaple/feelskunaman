
from argparse import Namespace
from helpers.spotify.client import Client

def execute(args: Namespace):
    song = Client().getTrack(args.url)
    print(song)