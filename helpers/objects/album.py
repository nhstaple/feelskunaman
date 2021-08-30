from helpers.affect.scherer import Scherer2D
from helpers.objects.track import Track
from helpers.music.tracks import decode_mode, decode_key, decode_ms

class Album():
    def __init__(self, features: dict, tracks: list):
        self._tracks: str = tracks
        self.name: str = features['name']
        self.artist: str = features['artist']
        self.id: str = features['id']
        self.num_tracks: float = len(tracks)
        self.genres: list(str) = features['genres']
        self.popularity: str = features['popularity']
        self.release_date: str = features['release_date']
        self.url: str = features['url']

        self.total_time_ms: float = 0
        for track in tracks:
            self.total_time_ms = self.total_time_ms + track.duration_ms
        
    
    def getVectors(self) -> list:
        return [ song.emotive for song in self._tracks]
    
    def __repr__(self) -> str:
        emotions: list = self.getVectors()
        u_valence: float = 0
        u_arousal: float = 0
        for emotive in emotions:
            u_valence = u_valence + emotive.getValence()
            u_arousal = u_arousal + emotive.getArousal()
        mean: Scherer2D = Scherer2D(u_valence, u_arousal)
        labels = mean.getLabels()
        intensity = '{:.2f}'.format(mean.getIntensity())

        val = 'ALBUM.meta\n'
        val = val + '  name       {:>s}\n'.format(self.name)
        val = val + '  artist     {:>s}\n'.format(self.artist)
        val = val + '  num tracks {:>d}\n'.format(self.num_tracks)
        val = val + '  popularity {:>d}\n'.format(self.popularity)
        val = val + '  length     {:>s}\n'.format(decode_ms(self.total_time_ms))
        val = val + '  url        {:>s}\n'.format(self.url)
        val = val + 'ALBUM.tracks\n'
        for track in self._tracks:
            val = val + '  {:s}\n'.format(track.name)
            val = val + '    {}\n'.format(Scherer2D.__repr__(track.emotive).replace('\n', '\n    '))
        val = val + 'ALBUM.emotions\n'
        val = val + '  valence    {:>s}\n'.format(labels[0])
        val = val + '  arousal    {:>s}\n'.format(labels[1])
        val = val + '  intensity  {:>s}\n'.format(intensity)
        val = val + '  angle      {:>s}\n'.format(mean.getAngle(rad=False))
        return val

