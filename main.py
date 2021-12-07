
from argparse import Namespace
from parsers.feelsparser import FeelsParser

import tasks.index as BigBrain

def main(args: Namespace):
    print('\nFeels Kuna Man - a tool for Music Emotion Recognition\n')
    BigBrain.execute(args)

if __name__ == '__main__':
    from parsers.feelsparser import FeelsParser
    import sys

    args = FeelsParser().parse_args(sys.argv[1:])
    main(args)