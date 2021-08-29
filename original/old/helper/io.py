import spotipy from spotipy.oauth2 import SpotifyClientCredentials

clientID  = 'fa0e3b01cf6a428f9fe0b8fe87414b3e'
secretKey = '8782bd8b67204046b1be84f7e641dd96'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(clientID, secretKey))

# returns playlist ID found in playlist.txt, and the spotify IDs for each song in the playlist
def GetPlaylistFromFile(fn:str, max_num:int):
    # open de way
    userPlaylist = open(fn, 'r')
    
    # initialize return variables
    url     = str()
    songIDs = list()
    data    = list()

    # initial loop sentinel 
    head = str('hello there')
    while len(head) > 0:
        head = userPlaylist.readline()
        # ignore comments, grab the first valid url, exit loop
        if head[0] != '#' and head[0:24] == 'https://open.spotify.com':
            url = head
            break
    print('playlist URL:\n{:s}\n'.format(url))

    # grab the playlist ID
    playlistID = (url.split('/'))[-1]
    print('playlistID:\n{:s}\n'.format(playlistID))

    # query the spotify api for the playlist data
    playlistData = spotify.playlist(playlistID)
    # print('return query keys')
    # print(playlistData.keys())
    # print('\nplaylist.tracks keys')
    # print(playlistData['tracks'].keys())
    # print('\nplaylist.tracks.items keys')
    # print(playlistData['tracks']['items'][0])

    # display the titles of songs
    print('songs:')
    for i in range(0, max_num):
        current_song = playlistData['tracks']['items'][i]['track']
        songIDs.append(current_song['id'])
        print('\t- {:s}'.format(current_song['name']))

    # get the data for the songs
    for result in spotify.audio_features(songIDs):
        data.append(StripSongData(result))
    # print(data[0])

    # close de way
    userPlaylist.close()
    return [ url, songIDs, data ]

def StripSongObject(song:dict):
    del song['album'] ; del song['available_markets'] ; del song['artists']
    del song['external_ids'] ; del song['external_urls'] ; del song['disc_number']
    del song['episode'] ; del song['is_local'] ; del song['preview_url']
    del song['track_number']; del song['track'] ; del song['type']
    return song

def StripSongData(data:dict):
    del data['uri'] ; del data['track_href'] ; del data['analysis_url']
    del data['id']; del data['type']
    arousal = data['danceability']
    del data['danceability']
    data['arousal'] = arousal
    return data


