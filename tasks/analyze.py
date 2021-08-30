
from argparse import Namespace
from typing import Tuple
from enum import Enum
from tasks import track, album

class EResource(Enum):
    TRACK = 0
    PLAYLIST = 1
    ALBUM = 2

    # TODO python 3.10 support match-case
    @staticmethod
    def encode(resource: str) -> Enum:
        if resource == 'track':
            return EResource.TRACK
        elif resource == 'playlist':
            return EResource.PLAYLIST
        elif resource == 'album':
            return EResource.ALBUM
        else:
            raise TypeError('Unsupported link!')

def validate_url(url: str) -> Tuple[Enum, str]:
    resource, id = url.split('/')[3:]
    return EResource.encode(resource), id

def execute(args: Namespace):
    resource, id = validate_url(args.url)

    if resource == EResource.TRACK:
        track.execute(args)
    elif resource == EResource.ALBUM:
        album.execute(args)
    else:
        raise TypeError('Only track and albums are supported!')