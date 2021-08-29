
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from helpers.spotify.supersecret import CLIENT_ID, SECRET_KEY 
import numpy as np

from helpers.objects.track import Track

class Client:
    def __init__(self, seed: np.short=-1):
        self._seed   = seed
        self._client = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                CLIENT_ID,
                SECRET_KEY)
            )
    
    def getSong(self, url: str):
        data = self._client.audio_features(url)[0]
        meta = self._client.track(url)

        features = {}
        features['artist']      = meta['artists'][0]['name']
        features['name']        = meta['name']
        features['album']       = meta['album']['name']
        features['popularity']  = meta['popularity']
        features['duration_ms'] = meta['duration_ms']
        features['valence']     = 2 * data['valence'] - 1
        features['arousal']     = 2 * data['danceability'] - 1
        features['id']          = data['id']
        features['url']         = meta['external_urls']['spotify']
        features['tempo']       = data['tempo']
        features['mode']        = data['mode']
        features['key']         = data['key']

        return Track(url, features)

