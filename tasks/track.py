
from argparse import Namespace
from helpers.spotify.client import Client
from helpers.objects.track import Track

def execute(args: Namespace):
    song: Track = Client().getTrack(args.url)
    if args.print:
        print(song)
    else:
        print(song.name)
        print('by ' + song.artist)
        print(song.emotive)
    
    if args.plot:
        print('WARNING: plotting for individual tracks is currently not supported')
