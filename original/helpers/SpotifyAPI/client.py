# client.py | helpers.SpotifyAPI
from os import error
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from helpers.affect.scherer import Scherer

class Client:
    def __init__(self, seed=int):
        self._seed = seed
        from helpers.SpotifyAPI.supersecret import clientID, secretKey 
        self._client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(clientID, secretKey))
    
    def GetSong(self, songID:str, preserve = False):
        features = self._client.audio_features(songID)[0]
        data = Client.__StripSongData(features, True)
        meta = self._client.track(songID)
        if preserve:
            data['artist'] = meta['artists'][0]['name']
            data['name'] = meta['name']
            data['album'] = meta['album']['name']
            data['popularity'] = meta['popularity']
            data['duration_ms'] = meta['duration_ms']
        valence = 2 * data['valence'] - 1
        arousal = 2 * data['danceability'] - 1
        return Scherer(valence, arousal), data

    def GetPlaylist(self, url:str, max_num:int = -1, display:bool = True):
        if max_num > 100: max_num = 100  
        # initialize return variables
        songIDs: list(str)     = []
        vectors: list(Scherer) = []
        data   : list(dict)    = []

        # grab the playlist ID
        playlistID = (url.split('/'))[-1]

        # query the spotify api for the playlist data
        playlistData = self._client.playlist(playlistID)

        if self._seed > -1:
            import random
            random.Random(self._seed).shuffle(playlistData['tracks']['items'])

        if display:
            print('name: ' + playlistData['name'])
            if(len(playlistData['description'])): print('description: ' + playlistData['description'])
            print('owner: ' + playlistData['owner']['display_name'])
            print('playlist:')
        
        n = len(playlistData['tracks']['items'])
        bounds = range(0, n)
        if max_num > 0: bounds = range(0, max_num)

        names: list(str) = []
        artists: list(str) = []
        links: list(str) = []
        for i in bounds:
            current = playlistData['tracks']['items'][i]['track']
            ID = current['id']
            songIDs.append(ID)
            names.append(current['name'])
            links.append(current['external_urls']['spotify'])
            artists.append(current['artists'][0]['name'])
        
        # get the data for the songs
        i = 0
        for result in self._client.audio_features(songIDs):
            song = Client.__StripSongData(result)
            song['name'] = names[i]
            song['url']  = links[i]
            song['artist'] = artists[i]
            data.append(song)

            emotive = Scherer(
                valence=2 * song['valence'] - 1,
                arousal=2 * song['danceability'] - 1
            )

            vectors.append(emotive)
            if display:
                print('\t- ({0:3d}°) {1:s}'.format(round(emotive.getDeg()), names[i]))
                print('\t\t ' + links[i] + '\n')
            
            i = i + 1

        return {
            'songIDs': songIDs,
            'data': data,
            'vectors': vectors,
            'url': url,
            'name': playlistData['name'],
            'description': playlistData['description']
        }

    def GetAnalysis(self, url:str, cacheToJSON:bool = False):
        res = self._client.audio_analysis(url)
        del res['track']['codestring'] ; del res['track']['code_version']
        del res['track']['echoprintstring'] ; del res['track']['echoprint_version']
        del res['track']['synchstring'] ; del res['track']['synch_version']
        del res['track']['rhythmstring'] ; del res['track']['rhythm_version']
        
        if cacheToJSON:
            import json
            f = open('./cache/dump.json', 'w')
            json.dump(res, f)
            f.close()
        return res

    @staticmethod
    def __StripSongObject(song:dict, preserve: bool = False):
        #try:
        if not preserve:
            del song['artists']
            del song['track']
            del song['album']
        del song['available_markets']
        del song['external_ids']
        del song['external_urls']
        del song['disc_number']
        del song['episode']
        del song['is_local']
        del song['preview_url']
        del song['track_number']
        del song['type']
        return song

    @staticmethod
    def __StripSongData(data:dict, preserve: bool = False):
        del data['uri']
        del data['track_href']
        del data['analysis_url']
        del data['id']
        del data['type']
        return data

