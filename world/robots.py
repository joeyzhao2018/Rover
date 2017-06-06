#!/usr/bin/env python3
from world.abstract.orientation.directions import Direction, opposite
from world.abstract.maps.Tile import Tile
from world.ev3controls import movements

_turn_map={

}


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
        else:
            left_yes=(self.facingDirection-direction)%2 if self.facingDirection<2 else (self.facingDirection-direction)%2-1
            #Because if N or S, you need to turn left when the difference is odd; if W or E, turn left when the difference is even
            if left_yes:
                movements.turnleft()
            else:
                movements.turnright()



    def run_until_btn(self):
        movements.run_direct()
