# test.py
## Description: driver to test development features 

from argparse import Namespace
from helpers.display.plot import DrawVectors

def computePlaylist(url: str, seed: int, num: int):
    from helpers.SpotifyAPI.client import Client
    spotify = Client(seed)
    res = spotify.GetPlaylist(url=url, max_num=num, display=True)

    from helpers.math.mean import ComputeMean
    mean = ComputeMean(res['data'])

    from helpers.display.dict import DisplayDict
    print('\nmean data:')
    DisplayDict(mean, '  ')

    from helpers.affect.scherer import Scherer
    mean_valence = 2 * mean['valence'] - 1
    mean_arousal = 2 * mean['danceability'] - 1
    emotive = Scherer(mean_valence, mean_arousal)
    print(emotive)
    DrawVectors(res['name'], res['vectors'], res['data'])

def parsePlaylist(args: Namespace):
    if args.playlist:
        url = args.playlist
        computePlaylist(url, 0, -1)
    else:
        taskName = './tasks/' + args.task + '.json'
        num = args.num
        seed = args.seed
        import json
        from json.decoder import JSONDecodeError
        try:
            file = open(taskName)
            task = json.load(file)
            file.close()
        except JSONDecodeError as err:
            print('error- couldnt open task!')
            print(task)
            print(err)
            sys.exit(-1)

        if 'playlist' in task:
            computePlaylist(args.task, task['playlist'], seed, num)
            # spotify.GetAnalysis(res['songIDs'][0], True)

def parseSong(args: Namespace):
    songID = args.song
    if songID[0:31] != 'https://open.spotify.com/track/':
        print('invalid url!')
        exit()

    from helpers.SpotifyAPI.client import Client
    spotify = Client()
    emotive, data = spotify.GetSong(songID, True)

    import math
    length = int(data['duration_ms'] / 1000)
    min = math.floor(length / 60) ; sec = length - (60 * min)

    print('name\t' + data['name'])
    print('artist\t' + data['artist'])
    print('album\t' + data['album'])
    print('length\t' + str(min) + ' min ' + str(sec) + ' sec')
    print(emotive)
    DrawVectors(data['name'], [emotive], [data])

def main(args:Namespace):
    print('\nFeels Kuna Man - a haphazard tool to check on the homie\'s feels using his Spotify daily plalist\n')
    if args.song:
        parseSong(args)
    else:
        parsePlaylist(args)

if __name__ == '__main__':
    from parsers.test import GetParser 
    import sys
    args = GetParser().parse_args(sys.argv[1:])
    main(args)