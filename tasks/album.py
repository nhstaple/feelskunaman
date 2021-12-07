
from argparse import Namespace
from helpers.spotify.client import Client
from helpers.objects.album import Album

def execute(args: Namespace):
    album: Album = Client().getAlbum(args.url, args.num)
    if args.print:
        print(album)
    else:
        print(album.name)
        print('by ' + album.artist)
        print(album.emotive)
