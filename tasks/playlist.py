
from argparse import Namespace
from helpers.spotify.client import Client
from helpers.objects.playlist import Playlist
import json

# TODO
## refractor to be apart of the feelsparser.py
SAVE_FILE = 'saved_data.json'

def execute(args:Namespace):
    playlist: Playlist = Client().getPlaylist(args.url, args.num)

    data: dict = playlist.toPythonDict()

    # TODO
    ## serialize data as a .json object
    if args.save:
        data: dict = playlist.toPythonDict()
        with open(SAVE_FILE, "w") as outfile:
            json.dump(data, outfile)

    if args.print:
        print(playlist)
    else:
        print(playlist.name)
        if len(playlist.description):
            print(playlist.description)
        print('by ' + playlist.owner)
        print(playlist.emotive.__repr__().replace('valence  ', 'valence μ').replace('arousal  ', 'arousal μ'))

    if args.plot:
        playlist.plot(args.normalize)

