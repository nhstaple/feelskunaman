# test.py
## Description: driver to test development features 

from json.decoder import JSONDecodeError
import sys, getopt

def displayHelp():
    print('TODO help command')
    sys.exit(0)

def parseTask(taskName):
    TASK_DIR = './tasks/'
    FILE_TYPE = '.json'
    fp = TASK_DIR + taskName + FILE_TYPE
    try:
        import json
        file = open(fp)
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
        res = spotify.GetPlaylist(url)

        from helpers.math.mean import ComputeMean
        mean = ComputeMean(res['data'])
        
        from helpers.display.dict import DisplayDict
        print('\nmean data:')
        DisplayDict(mean, '  ')

        valence = mean['valence']
        arousal = mean['danceability']
        if valence >= 0.50:
            print('result  - happy')
        else:
            print('result  - sad')
        if arousal >= 0.50:
            print('result  - awake')
        else:
            print('result  - tired')
        # print(spotify.GetAnalysis(res['songIDs'][0]))
    else:
        displayHelp()

def main(argv):
    try:
        # https://docs.python.org/3/library/getopt.html
        opts, args = getopt.getopt(
            argv,
            'ht:',
            [ 'task=' ]
        )
    except getopt.GetoptError:
        displayHelp()

    for opt, arg in opts:
        if opt == 'h': displayHelp()
        elif opt in ('-t', '--task'): parseTask(arg)

if __name__ == '__main__':
    main(sys.argv[1:])