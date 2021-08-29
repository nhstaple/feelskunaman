
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
    def encode(v: Vec2D) -> Enum:
        angle = v.getAngle(rad=False)
        if angle >= 0 and angle <= 90:
            return EPosition.QUAD1
        elif angle >= 90 and angle <= 180:
            return EPosition.QUAD2
        elif angle >= 180 and angle <= 360:
            return EPosition.QUAD3
        else:
            return EPosition.QUAD4

    # TODO python 3.10 supports match-case
    @staticmethod
    def decode(quadrant: Enum) -> Tuple[str, str]:
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
    def getQuad(encoding: Enum) -> str:
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

class Scherer2D():
    def __init__(self, valence: np.double, arousal: np.double):
        if valence == 0 and arousal == 0:
            raise ValueError('Both inputs cannot be zero!')
        self._data = Vec2D(valence, arousal)
    
    def getIntensity(self, ord: Union[int, str] = None) -> np.double:
        return self._data.norm(ord)

    def getDirection(self, rad: bool = True) -> np.double:
        return self._data.getAngle(rad)

    def normalize(self, set: bool = True) -> Union[Vec2D, None]:
        return self._data.normalize(set)
    
    def getPosEncoding(self):
        return EPosition.encode(self._data)
    
    def __repr__(self) -> str:
        pos = self.getPosEncoding()
        dim1, dim2 = EPosition.decode(pos)
        quad = EPosition.getQuad(pos)
        valence, arousal = self._data.getComponents()
        intensity, angle  = self._data.polar(rad=False)
        return 'valence  : {0:>7s}  ({1:^8.3f})\narousal  : {2:>7s}  ({3:^8.3f})\nintensity: {4:>7.2f}\nangle    : {5:>7.2f}° ({6:^8s})'.format(dim1, valence, dim2, arousal, intensity, angle, quad)