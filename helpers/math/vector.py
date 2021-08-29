# helpers.math.vector.py
## author - nick
## description - a 2D linear algebra vector class. For use in Scherer space

from abc import abstractclassmethod
import numpy as np
import copy as cp
from typing import Tuple, Union

class Vector():
    def __init__(self):
        self._vec: np.ndarray
    
    def array(self) -> np.ndarray:
        return cp.copy(self._vec)

    @staticmethod
    def dot(v1, v2) -> np.double:
        if not isinstance(v1, Vector):
            raise TypeError('First parameter is not of Vector. Got {} instead.'.format(type(v1)))
        if not isinstance(v2, Vector):
            raise TypeError('Second parameter is not of Vector. Got {} instead.'.format(type(v2)))
        return np.dot(v1._vec, v2._vec)

    def norm(self, ord: Union[int, str] = None) -> np.double:
        return np.linalg.norm(x=self._vec, ord=ord)

    @abstractclassmethod
    def normalize(self): pass

    @abstractclassmethod
    def _getRad(self): pass

    @abstractclassmethod
    def _getDeg(self): pass

    @abstractclassmethod
    def getComponents(self) -> Tuple: pass

class Vec2D(Vector):    
    def __init__(self, x1: np.double, x2: np.double):
        self._vec = np.array( [x1, x2], dtype=np.double)

    def __repr__(self) -> str:
        return '< {0:>5.2f}, {1:>5.2f} >'.format(self._vec.item(0), self._vec.item(1))

    def normalize(self, set: bool = False) -> Union[Vector, None]:
        if not set:
            v = self.array() / self.norm()
            return Vec2D(v.item(0), v.item(1))
        else:
            self._vec = self._vec / self.norm()

    def _getRad(self) -> np.double:
        x1 = self._vec.item(0)
        x2 = self._vec.item(1)
        angle = np.arctan2(x2, x1)
        if angle < 0: angle = angle + 2 * np.pi
        return angle

    def _getDeg(self) -> np.double:
        return self._getRad() * 180 / np.pi

    def getAngle(self, rad: bool = True) -> np.double:
        if rad: return self._getRad() 
        else:   return self._getDeg()

    def polar(self, rad: bool = True) -> Tuple[np.double, np.double]:
        return self.norm(), self.getAngle(rad) 

    def getComponents(self) -> Tuple[np.double, np.double]:
        return self._vec.item(0), self._vec.item(1)
