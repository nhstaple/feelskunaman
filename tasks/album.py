
from argparse import Namespace
from helpers.spotify.client import Client

def execute(args: Namespace):
    album = Client().getAlbum(args.url, args.num)
    print(album)
