#!/usr/bin/env python3
from world.abstract.orientation.directions import Direction, opposite
from world.abstract.maps.Tile import Tile
from world.ev3controls import movements

class MyCompanion(object):

    facingDirection=Direction.NORTH
    current_tile=Tile()

    def turn_to_direction(self, direction):
        if not isinstance(direction, Direction):
            raise TypeError("Not a valid Direction {}".format(repr(direction)))

        if self.facingDirection==direction:
            pass
        elif self.facingDirection==opposite(direction):
            movements.turnback()
