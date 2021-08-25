# client.py | helpers.SpotifyAPI
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Client:
    def __init__(self):
        from helpers.SpotifyAPI.supersecret import clientID, secretKey 
        self._client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(clientID, secretKey))
    
    def GetPlaylist(self, url:str, max_num:int = -1, display:bool = True):
        # print('playlist URL:\n{:s}\n'.format(url))
        
        # initialize return variables
        songIDs = list()
        data    = list()

        # grab the playlist ID
        playlistID = (url.split('/'))[-1]
        # print('playlistID:\n{:s}\n'.format(playlistID))

        # query the spotify api for the playlist data
        playlistData = self._client.playlist(playlistID)
        # print('return query keys')
        # print(playlistData.keys())
        # print('\nplaylist.tracks keys')
        # print(playlistData['tracks'].keys())
        # print('\nplaylist.tracks.items keys')
        # print(playlistData['tracks']['items'][0])

        if display:
            print('name : ' + playlistData['name'])
            if(len(playlistData['description'])):
                print('description: ' + playlistData['description'])
            print('owner: ' + playlistData['owner']['display_name'])
            # display the titles of songs
            print('songs:')
            bounds = range(0, len(playlistData['tracks']['items']))
            if max_num > 0: bounds = range(0, max_num)
            for i in bounds:
                current_song = playlistData['tracks']['items'][i]['track']
                current_song = Client.__StripSongObject(current_song)
                songIDs.append(current_song['id'])
                print('\t- {:s}'.format(current_song['name']))

        # get the data for the songs
        for result in self._client.audio_features(songIDs):
            data.append(Client.__StripSongData(result))
        # print(data[0])

        return {
            'songIDs': songIDs,
            'data': data,
            'url':url,
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
    def __StripSongObject(song:dict):
        del song['album'] ; del song['available_markets'] ; del song['artists']
        del song['external_ids'] ; del song['external_urls'] ; del song['disc_number']
        del song['episode'] ; del song['is_local'] ; del song['preview_url']
        del song['track_number']; del song['track'] ; del song['type']
        return song

    @staticmethod
    def __StripSongData(data:dict):
        del data['uri'] ; del data['track_href'] ; del data['analysis_url']
        del data['id']; del data['type']
        # arousal = data['danceability']
        # del data['danceability']
        # data['arousal'] = arousal
        return data

