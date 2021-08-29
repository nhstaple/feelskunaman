
from helpers.affect.scherer import Scherer2D

class Track():
    def __init__(self, id: str, features: dict):
        self.id       = id
        self.emotive  = Scherer2D(
            features['valence'],
            features['arousal']
        )
        self.name        = features['name']
        self.artist      = features['artist']
        self.album       = features['album']
        self.duration_ms = features['duration_ms']
        self.tempo       = features['tempo']
        self.mode        = features['mode']
        self.key         = features['key']
    


