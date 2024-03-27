from enum import Enum

class QuadPosition(Enum):
    UPPER_LEFT = 1
    UPPER_RIGHT = 2
    LOWER_LEFT = 3
    LOWER_RIGHT = 4


class Observation(Enum):
    FREE = 0
    OCCUPIED = 1
    UNDISCOVERED = 2