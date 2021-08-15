def ComputeMean(data:list):
    n = len(data)
    res = {
        'energy': 0,
        'loudness': 0,
        'speechiness': 0,
        'acousticness': 0,
        'instrumentalness': 0,
        'liveness': 0,
        'valence': 0,
        'danceability': 0,
        'tempo': 0
    }

    for song in data:
        for feature in res:
            res[feature] = song[feature] + res[feature]
    
    for feature in res:
        res[feature] = res[feature] / n
    
    return res
