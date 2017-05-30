from enum import IntEnum


class Direction(IntEnum):
    NORTH=0
    SOUTH=1
    EAST=2
    WEST=3


_oppo=[Direction.SOUTH,Direction.NORTH,Direction.WEST,Direction.EAST]


def opposite(direction):
    if isinstance(direction, Direction):
        return _oppo[direction]
    else:
        raise TypeError("Not a valid Direction {}".format(repr(direction)))
