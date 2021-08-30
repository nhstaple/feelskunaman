
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from helpers.spotify.supersecret import CLIENT_ID, SECRET_KEY 
import numpy as np
import random

from helpers.objects.track import Track
from helpers.objects.album import Album

class Client:
    def __init__(self, seed: np.short=-1):
        self.creds   = SpotifyClientCredentials(CLIENT_ID, SECRET_KEY)
        self._seed   = seed
        self._client = spotipy.Spotify(client_credentials_manager=self.creds)
    
    @staticmethod
    def _makeTrack(meta: dict, data: dict):
        features = dict()
        features['artist']      = meta['artists'][0]['name']
        features['artist_id']   = meta['artists'][0]['id']
        features['name']        = meta['name']
        features['album']       = meta['album']['name']
        features['album_id']    = meta['album']['id']
        features['popularity']  = meta['popularity']
        features['duration_ms'] = meta['duration_ms']
        features['valence']     = 2 * data['valence'] - 1
        features['arousal']     = 2 * data['danceability'] - 1
        features['id']          = data['id']
        features['url']         = meta['external_urls']['spotify']
        features['tempo']       = int(data['tempo'])
        features['mode']        = data['mode']
        features['key']         = data['key']
        return Track(features)

    def _makeAlbum(self, meta: dict, trackIDs: list):
        features = dict()
        features['name']         = meta['name']
        features['artist']       = meta['artists'][0]['name']
        features['genres']       = meta['genres']
        features['popularity']   = meta['popularity']
        features['release_date'] = meta['release_date']
        features['id']           = meta['id']
        features['url']          = meta['external_urls']['spotify']

        tracks: list(Track) = self.getTracks(trackIDs)
        return Album(features, tracks)

    def getTracks(self, urls: str):
        data = self._client.audio_features(urls)
        meta = self._client.tracks(urls)['tracks']
        return [ Client._makeTrack(meta[i], data[i]) for i in range(0, len(data)) ]
        
    def getTrack(self, url: str):
        data = self._client.audio_features(url)[0]
        meta = self._client.track(url)
        return Client._makeTrack(meta, data)

    def getAlbum(self, url:str, num: int):
        if num > 100:
            print('Warning: maximum supported number is 100')
            num = 100

        # initialize return variables
        trackIDs: list(str) = []
        features: dict = {}

        # query the spotify api for the playlist data
        playlistData = self._client.album(url)

        if self._seed > -1:
            random.Random(self._seed).shuffle(playlistData['tracks']['items'])
        
        n = len(playlistData['tracks']['items'])
        if num <= 0:
            num = n
        elif n > num:
            num = n
        
        bounds = range(0, num)
        for i in bounds:
            track_i = playlistData['tracks']['items'][i]
            trackIDs.append(track_i['id'])
        
        return self._makeAlbum(playlistData, trackIDs)



