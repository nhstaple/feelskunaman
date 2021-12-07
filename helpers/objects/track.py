
from helpers.affect.scherer import Emotive2D
from helpers.music.tracks import decode_mode, decode_key, decode_ms
class Track():
    def __init__(self, features:dict):
        self.emotive: Emotive2D = Emotive2D(
            features['valence'], features['arousal']
        )
        self.name:str          = features['name']
        self.artist:str        = features['artist']
        self.artist_id:str     = features['artist_id']
        self.album:str         = features['album']
        self.album_id:str      = features['album_id']
        self.duration_ms:float = features['duration_ms']
        self.tempo:int         = features['tempo']
        self.mode:int          = features['mode']
        self.key:int           = features['key']
        self.url:str           = features['url']
        self.id:str            = str.split(self.url, '/')[-1]
        self.popularity:int    = features['popularity']
        self.explicit:bool     = features['explicit']

    def __repr__(self) -> str:
        labels = self.emotive.getLabels()
        intensity = '{:.2f}'.format(self.emotive.getIntensity())

        val = 'TRACK.meta\n'
        val = val + '  name       {:>s}\n'.format(self.name)
        val = val + '  artist     {:>s}\n'.format(self.artist)
        val = val + '  album      {:>s}\n'.format(self.album)
        val = val + '  popularity {:>d}\n'.format(self.popularity)
        val = val + '  length     {:>s}\n'.format(decode_ms(self.duration_ms))
        val = val + '  tempo      {:>d}bpm\n'.format(int(self.tempo))
        val = val + '  url        {:>s}\n'.format(self.url)
        val = val + 'TRACK.tonal\n'
        val = val + '  mode       {:>s}\n'.format(decode_mode(self.mode))
        val = val + '  key        {:>s}\n'.format(decode_key(self.key))
        val = val + 'TRACK.emotions\n'
        val = val + '  valence    {:>s}\n'.format(labels[0])
        val = val + '  arousal    {:>s}\n'.format(labels[1])
        val = val + '  intensity  {:>s}\n'.format(intensity)
        val = val + '  angle      {:>s}\n'.format(self.emotive.getAngle(rad=False))
        return val
