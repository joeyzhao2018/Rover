from enum import IntEnum


class Direction(IntEnum):
    NORTH=0
    SOUTH=1
    EAST=2
    WEST=3


_oppo=[Direction.SOUTH,Direction.NORTH,Direction.WEST,Direction.EAST]
_left=[Direction.WEST,Direction.EAST,Direction.NORTH,Direction.SOUTH]
_right=[Direction.EAST,Direction.WEST,Direction.SOUTH,Direction.NORTH]


def opposite(direction):
    if isinstance(direction, Direction):
        return _oppo[direction]
    else:
        raise TypeError("Not a valid Direction {}".format(repr(direction)))

def left(direction):
    if isinstance(direction, Direction):
        return _left[direction]
    else:
        raise TypeError("Not a valid Direction {}".format(repr(direction)))

def right(direction):
    if isinstance(direction, Direction):
        return _right[direction]
    else:
        raise TypeError("Not a valid Direction {}".format(repr(direction)))

def strDirection(direction_str):
    d_low=direction_str.lower()
    if d_low in ['n','north']:
        return Direction.NORTH
    elif d_low in ['s','south']:
        return Direction.SOUTH
    elif d_low in ['w','west']:
        return Direction.WEST
    elif d_low in ['e','east']:
        return Direction.EAST
