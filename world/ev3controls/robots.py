#!/usr/bin/env python3
from world.abstract.orientation.directions import Direction, opposite, strDirection
from world.ev3controls import movements




class MyCompanion(object):

    facingDirection=Direction.NORTH
    current_location="Nowhere"

    def __init__(self, direction=None):
        if direction is not None:
            self.facingDirection=direction


    def turn_to_direction(self, direction):

        if not isinstance(direction, Direction):
            try:
                direction=strDirection(direction)
            except:
                raise TypeError("Not a valid Direction {}".format(repr(direction)))

        # if self.facingDirection==direction:
        #     pass
        # elif self.facingDirection==opposite(direction):
        #     movements.turnback()
        # else:
        #     left_yes=(self.facingDirection-direction)%2 if self.facingDirection<2 else (self.facingDirection-direction)%2-1
        #     #Because if N or S, you need to turn left when the difference is odd; if W or E, turn left when the difference is even
        #     if left_yes:
        #         movements.turnleft()
        #     else:
        #         movements.turnright()
        self.facingDirection=direction
        return str(self.facingDirection)


    def run_by_distance(self, distance):
        movements.run_by_distance(distance)



    def react(self,*args):
        action=self.__getattribute__(args[0])
        if hasattr(action, '__call__'):
            return action(*args[1:])
        else:
            return str(action)

