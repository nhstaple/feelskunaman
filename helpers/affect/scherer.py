
from helpers.math.vector import Vec2D
from typing import Tuple, Union
import numpy as np
from enum import Enum

VALENCE_RIGHT = 'happy'
VALENCE_LEFT  = 'sad'
AROUSAL_UP    = 'awake'
AROUSAL_DOWN  = 'bored'

class EPosition(Enum):
    QUAD1 = 0
    QUAD2 = 1
    QUAD3 = 2
    QUAD4 = 3

    @staticmethod
    def encode(v:Vec2D) -> Enum:
        angle = v.getAngle(rad=False)
        if angle >= 0 and angle <= 90:
            return EPosition.QUAD1
        elif angle >= 90 and angle <= 180:
            return EPosition.QUAD2
        elif angle >= 180 and angle <= 270:
            return EPosition.QUAD3
        else:
            return EPosition.QUAD4

    # TODO python 3.10 supports match-case
    @staticmethod
    def decode(quadrant:Enum) -> Tuple[str, str]:
        if quadrant == EPosition.QUAD1:
            return VALENCE_RIGHT, AROUSAL_UP
        elif quadrant == EPosition.QUAD2:
            return VALENCE_LEFT, AROUSAL_UP
        elif quadrant == EPosition.QUAD3:
            return VALENCE_LEFT, AROUSAL_DOWN
        elif quadrant == EPosition.QUAD4:
            return VALENCE_RIGHT, AROUSAL_DOWN
        else:
            raise TypeError('Unsupported value!')

    @staticmethod
    def getQuad(encoding:Enum) -> str:
        if encoding == EPosition.QUAD1:
            return 'Quad I'
        elif encoding == EPosition.QUAD2:
            return 'Quad II'
        elif encoding == EPosition.QUAD3:
            return 'Quad III'
        elif encoding == EPosition.QUAD4:
            return 'Quad IV'
        else:
            raise TypeError('Unsupported value!')

class Emotive2D():
    def __init__(self, valence:np.double, arousal:np.double):
        if valence == 0 and arousal == 0:
            raise ValueError('Both inputs cannot be zero!')
        self._data:Vec2D = Vec2D(valence, arousal)
    
    def getIntensity(self, ord:Union[int, str] = None) -> np.double:
        return self._data.norm(ord)

    def getDirection(self, rad:bool = True) -> np.double:
        return self._data.getAngle(rad)

    def getAngle(self, rad:bool = True) -> str:
        if rad: return '{:5.2f}π'.format(self._data.getAngle(rad) / np.pi)
        else  : return '{:5.2f}°'.format(self._data.getAngle(rad))
    
    def normalize(self, set:bool = False) -> Union[Vec2D, None]:
        return self._data.normalize(set)
    
    def getPosEncoding(self):
        return EPosition.encode(self._data)
    
    def getQuad(self):
        return EPosition.getQuad(self.getPosEncoding())

    def getLabels(self):
        return EPosition.decode(
            EPosition.encode(self._data)
        )

    def getValence(self):
        val, aro = self._data.getComponents()
        return val

    def getArousal(self):
        val, aro = self._data.getComponents()
        return aro

    def getValues(self):
        return self._data.getComponents()

    def __repr__(self) -> str:
        pos = self.getPosEncoding()
        dim1, dim2 = EPosition.decode(pos)
        quad = EPosition.getQuad(pos)
        valence, arousal = self._data.getComponents()
        intensity, angle  = self._data.polar(rad=False)

        val = str()
        val = val + 'valence  : {0:>7s}  ({1:^8.3f})\n'.format(dim1, valence)
        val = val + 'arousal  : {0:>7s}  ({1:^8.3f})\n'.format(dim2, arousal)
        val = val + 'intensity: {0:>7.2f}\n'.format(intensity)
        val = val + 'angle    : {0:>7.2f}° ({1:^8s})'.format(angle, quad)
        return val