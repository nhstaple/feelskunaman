# test.py
## Description: driver to test development features 

from argparse import Namespace

def parseTask(args:Namespace):
    taskName = args.task
    num = args.num
    import json
    from json.decoder import JSONDecodeError
    try:
        file = open(taskName)
        task = json.load(file)
        file.close()
    except JSONDecodeError as err:
        print('error- couldnt open task!')
        print(fp)
        print(err)
        sys.exit(-1)

    if 'playlist' in task:
        from helpers.SpotifyAPI.client import Client
        spotify = Client()
        url = task['playlist']
        res = spotify.GetPlaylist(url=url, max_num=num, display=True)

        from helpers.math.mean import ComputeMean
        mean = ComputeMean(res['data'])

        from helpers.display.dict import DisplayDict
        print('\nmean data:')
        DisplayDict(mean, '  ')

        from helpers.affect.scherer import Scherer
        emotive = Scherer(
            2 * mean['valence'] - 1,
            2 * mean['danceability'] - 1
        )
        (labels, degrees) = emotive.getLabels()
        print('\nin degs: {:.2f} (2D Scherer normalized vector)'.format(degrees))
        print('labels : {0:s}, {1:s}'.format(labels[0], labels[1]))

        # spotify.GetAnalysis(res['songIDs'][0], True)

def main(args:Namespace):
    print('\nFeels Kuna Man - a haphazard tool to check on the homie\'s feels using his Spotify weekly plalist\n')
    parseTask(args)

if __name__ == '__main__':
    from parsers.test import GetParser 
    import sys
    args = GetParser().parse_args(sys.argv[1:])
    main(args)