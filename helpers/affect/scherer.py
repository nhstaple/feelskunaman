
import numpy as np
import copy as cp

labels = {
    'valence': {
        'happy': [
            np.pi*-1/2,
            np.pi*1/2
        ],
        'sad': [
            np.pi*1/2,
            np.pi*3/2
        ]
    },
    'arousal': {
        'awake': [
            0,
            np.pi
        ],
        'asleep': [
            np.pi,
            np.pi*2
        ]
    }
}

class Scherer:
    def __init__(self, valence: float, arousal: float):
        self._vector = np.array([valence, arousal], dtype=float)
        self._vector = self._vector / np.linalg.norm(
            np.array([valence, arousal], dtype=float)
        )
    
    def getVector(self):
        return cp.copy(self._vector)
    
    def _getTheta(self):
        return np.arctan2(self._vector.take(1), self._vector.take(0))

    def getLabels(self):
        theta = self._getTheta()
        degs = theta * 180 / np.pi
        res = list()
        
        # valence - good / bad 
        ## happy
        if theta >= labels['valence']['happy'][0] and theta <= labels['valence']['happy'][1]:
            res.append('happy')
        ## sad 
        elif theta >= labels['valence']['sad'][0] and theta <= labels['valence']['sad'][1]:
            res.append('sad')

        # arousal - engaged / lethargic 
        if theta >= labels['arousal']['awake'][0] and theta <= labels['arousal']['awake'][1]:
            res.append('awake')
        ## sad 
        elif theta >= labels['arousal']['asleep'][0] and theta <= labels['arousal']['asleep'][1]:
            res.append('asleep')
        return res, degs
