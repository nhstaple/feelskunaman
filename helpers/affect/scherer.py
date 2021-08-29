
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
        self._valence = valence
        self._arousal = arousal
        self._vector = np.array([valence, arousal], dtype=float)
        self._vector = self._vector / np.linalg.norm(
            np.array([valence, arousal], dtype=float)
        )
    
    def __repr__(self):
        labels, angle = self.getLabels()
        value = '\n'
        value = value + 'in degs: {:.2f}° '.format(angle)
        
        angle = self.getDeg()
        if angle >= 0 and angle <= 90: value = value + '(Quad I)'
        elif angle >= 90 and angle <= 180: value = value + '(Quad II)'
        elif angle >= 180 and angle <= 270: value = value + '(Quad III)'
        else: value = value + '(Quad IV)'

        value = value + '\nvalence: {:.2f}'.format(self._valence)
        value = value + '\narousal: {:.2f}'.format(self._arousal)
        value = value + '\nlabels : {0:s}, {1:s}'.format(labels[0], labels[1])

        return value

    def getComponents(self): return self._valence, self._arousal

    @staticmethod
    def _radToDeg(rad): return rad * 180 / np.pi

    def getVector(self): return cp.copy(self._vector)

    def getDeg(self): return Scherer._radToDeg(self.getRad())

    def getRad(self):
        angle = np.arctan2(self._arousal, self._valence)
        if angle < 0: angle = angle + 2 * np.pi
        return angle
    
    def getLabels(self):
        theta = self.getRad()
        degs = self.getDeg()
        res = list()
        
        # valence - good / bad 
        ## happy
        if theta >= labels['valence']['happy'][0] and theta <= labels['valence']['happy'][1]:
            res.append('happy')
        ## sad 
        else:
            res.append('sad')

        # arousal - engaged / lethargic
        ## awake / aroused
        if theta >= labels['arousal']['awake'][0] and theta <= labels['arousal']['awake'][1]:
            res.append('awake')
        ## asleep / passive
        else:
            res.append('asleep')
        return res, degs
