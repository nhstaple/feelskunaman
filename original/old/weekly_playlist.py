import helper.system as system
import helper.io as io
import helper.maths as maths

# started from the bottom
system.Start()

# get the data from the playlist file
path_to_playlist = './playlist.txt'
[ url,       songIDs,       songData ] = io.GetPlaylistFromFile(path_to_playlist, 50)
[ url, top10_songIDs, top10_songData ] = io.GetPlaylistFromFile(path_to_playlist, 10)

# process the data
mean = {
    'all'  : maths.ComputeMean(songData),
    'top10': maths.ComputeMean(top10_songData)
}

# visualize the data
mean_emotion = {
    'top10': { 'valence': mean['top10']['valence'], 'arousal': mean['top10']['arousal'] },
    'all'  : { 'valence': mean['all']['valence'],   'arousal': mean['all']['arousal']   }
}

valence = mean_emotion['all']['valence']
arousal = mean_emotion['all']['arousal']
for key in mean_emotion:
    print('{0:8s}'.format(key, mean_emotion[key]))
    for feature in mean_emotion[key]:
        print('\t{0:8s}- {1:.4f}'.format(feature, mean_emotion[key][feature]))

if valence >= 0.50:
    print('result  - happy')
else:
    print('result  - sad')
if arousal >= 0.50:
    print('result  - awake')
else:
    print('result  - tired')

# now we here 
system.End({})