from enum import Enum


class Side(Enum):
    YES = 1
    NO = 2

    def __str__(self):
        if self == Side.YES:
            return "yes"
        else:
            return "no"
