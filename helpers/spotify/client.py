
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from helpers.spotify.supersecret import CLIENT_ID, SECRET_KEY 
import numpy as np
import random

from helpers.objects.track import Track
from helpers.objects.album import Album
from helpers.objects.playlist import Playlist

class Client:
    def __init__(self, seed:np.short=-1):
        self.creds   = SpotifyClientCredentials(CLIENT_ID, SECRET_KEY)
        self._seed   = seed
        self._client = spotipy.Spotify(client_credentials_manager=self.creds)

    @staticmethod
    def _makeTrack(meta:dict, data:dict):
        features:dict = dict()
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
        features['explicit']    = meta['explicit']
        return Track(features)

    def getTracks(self, urls:str):
        n:np.short     = len(urls)
        data:list(str) = list()
        meta:list(str) = list()
        if n > 50:
            meta = self._client.tracks(urls[:50])['tracks']
            meta = meta + self._client.tracks(urls[50:])['tracks']
            data = self._client.audio_features(urls[:50])
            data = data + self._client.audio_features(urls[50:])
        else:
            meta = self._client.tracks(urls)['tracks']
            data = self._client.audio_features(urls)
        return [ Client._makeTrack(meta[i], data[i]) for i in range(0, n) ]
        
    def getTrack(self, url:str):
        data = self._client.audio_features(url)[0]
        meta = self._client.track(url)
        return Client._makeTrack(meta, data)

    def _makeAlbum(self, meta:dict, trackIDs:list):
        features:dict = dict()
        features['name']         = meta['name']
        features['artist']       = meta['artists'][0]['name']
        features['artist_id']    = meta['artists'][0]['id']
        features['genres']       = meta['genres']
        features['popularity']   = meta['popularity']
        features['release_date'] = meta['release_date']
        features['id']           = meta['id']
        features['url']          = meta['external_urls']['spotify']

        tracks:list(Track) = self.getTracks(trackIDs)
        return Album(features, tracks)

    def getAlbum(self, url:str, num:np.short=100):
        if num > 100:
            print('Warning: maximum supported number is 100')
            num = 100

        # initialize return variables
        trackIDs:list(str) = []

        # query the spotify api for the playlist data
        albumData:dict = self._client.album(url)

        if self._seed > -1:
            random.Random(self._seed).shuffle(albumData['tracks']['items'])
        
        n:np.short = len(albumData['tracks']['items'])
        if num <= 0:
            num = n
        elif n > num:
            num = n
        
        bounds:range = range(0, num)
        for i in bounds:
            track_i = albumData['tracks']['items'][i]
            trackIDs.append(track_i['id'])
        
        return self._makeAlbum(albumData, trackIDs)

    def _makePlaylist(self, meta:dict, trackIDs:list):
        features:dict = {}
        
        features['name']        = meta['name']
        features['owner']       = meta['owner']['display_name']
        features['owner_id']    = meta['owner']['id']
        features['id']          = meta['id']
        features['url']         = meta['external_urls']['spotify']
        features['description'] = meta['description']

        tracks:list(Track)      = self.getTracks(trackIDs)
        features['artists']     = [ track.artist    for track in tracks ]
        features['artists_id']  = [ track.artist_id for track in tracks ]
        features['albums']      = [ track.album     for track in tracks ]
        features['albums_id']   = [ track.album_id  for track in tracks ]

        return Playlist(features, tracks)

    def getPlaylist(self, url:str, num:np.short=100):
        if num > 100 or num < 1:
            print('Warning: maximum supported number is 100')
            num = 100
        
        trackIDs:list(str) = []

        playlistData:dict = self._client.playlist(url)
        
        if self._seed > -1:
            random.Random(self._seed).shuffle(playlistData['tracks']['items'])
        
        n:np.short = len(playlistData['tracks']['items'])
        if num > n: num = n

        bounds:range = range(0, num)
        for i in bounds:
            track_i = playlistData['tracks']['items'][i]['track']
            trackIDs.append(track_i['id'])

        return self._makePlaylist(playlistData, trackIDs)


