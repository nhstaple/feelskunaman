
from argparse import Namespace
from helpers.spotify.client import Client

def execute(args: Namespace):
    song = Client().getSong(args.url)
    
    print(song.name)
    print(song.artist)
    print(song.album)
    print(song.duration_ms)
    print(song.tempo)
    print(song.mode)
    print(song.key)
    print(song.emotive)