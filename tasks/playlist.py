
from argparse import Namespace
from helpers.spotify.client import Client
from helpers.objects.playlist import Playlist

def execute(args:Namespace):
    playlist:Playlist = Client().getPlaylist(args.url, args.num)

    if args.print:
        print(playlist)
    else:
        print(playlist.name)
        if len(playlist.description):
            print(playlist.description)
        print('by ' + playlist.owner)
        print(playlist.emotive.__repr__().replace('valence  ', 'valence μ').replace('arousal  ', 'arousal μ'))

