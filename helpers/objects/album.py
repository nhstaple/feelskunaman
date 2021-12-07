
from helpers.affect.scherer import Emotive2D
from helpers.music.tracks import decode_ms

from helpers.visualization.plotting import DrawVectors

class Album():
    def __init__(self, features: dict, tracks: list):
        self._tracks: str      = tracks
        self.name: str         = features['name']
        self.artist: str       = features['artist']
        self.artist_id: str    = features['artist_id']
        self.id: str           = features['id']
        self.num_tracks: float = len(tracks)
        self.genres: list(str) = features['genres']
        self.popularity: str   = features['popularity']
        self.release_date: str = features['release_date']
        self.url: str          = features['url']

        self.total_time_ms: float = 0
        for track in tracks:
            self.total_time_ms = self.total_time_ms + track.duration_ms

        emotions: list = self.getVectors()
        u_v: float = 0
        u_a: float = 0
        for emotive in emotions:
            u_v = u_v + emotive.getValence()
            u_a = u_a + emotive.getArousal()
        self.emotive = Emotive2D(u_v / self.num_tracks, u_a / self.num_tracks)
    
    def getVectors(self) -> list:
        return [ song.emotive for song in self._tracks]
    
    def __repr__(self, show_tracks: bool = True) -> str:
        val = 'ALBUM.meta\n'
        val = val + '  name       : {:>s}\n'.format(self.name)
        val = val + '  artist     : {:>s}\n'.format(self.artist)
        val = val + '  num tracks : {:>d}\n'.format(self.num_tracks)
        val = val + '  popularity : {:>d}\n'.format(self.popularity)
        val = val + '  length     : {:>s}\n'.format(decode_ms(self.total_time_ms))
        val = val + '  url        : {:>s}\n'.format(self.url)
        if show_tracks:
            val = val + 'ALBUM.tracks\n'
            for track in self._tracks:
                val = val + '  {:s}\n'.format(track.name)
                val = val + '    {}\n'.format(Emotive2D.__repr__(track.emotive).replace('\n', '\n    '))
        val = val + 'ALBUM.emotions\n'
        val = val + '  {}\n'.format(Emotive2D.__repr__(self.emotive).replace('\n', '\n  '))
        return val

    def plot(self, normalize: bool):
        DrawVectors('Album ' + self.name, self.getVectors(), self._tracks, normalize)
