#!/usr/bin/env python3
from world.abstract.orientation.directions import Direction, opposite, strDirection
from world.ev3controls import movements




class MyCompanion(object):

    facingDirection=Direction.NORTH
    territory_list=["Employee_Desk_A","MeetingRoom","CoffeeLocation"]
    curr_location_index=None  # if 0 meaning it's at Employee_Desk_A, etc...
    territory_routing=[[None,[("turn_to_direction","East"),("run_by_distance","100")],[("go_to_location","MeetingRoom"),("go_to_location","CoffeeLocation")]],
                       [[("turn_to_direction","West"),("run_by_distance","100")],None,[("turn_to_direction","South"),("run_by_distance","200")]],
                       [[("go_to_location","MeetingRoom"),("go_to_location","Employee_Desk_A")],[("turn_to_direction","North"),("run_by_distance","200")],None]]

    def __init__(self, direction=None):
        if direction is not None:
            self.facingDirection=direction


    def turn_to_direction(self, direction):

        if not isinstance(direction, Direction):
            try:
                direction=strDirection(direction)
            except:
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
        self.facingDirection=direction
        movements.speak("Now facing {}".format(direction))
        return str(self.facingDirection)

    def run_by_distance(self, distance):
        movements.run_by_distance(distance)

    def go_to_location(self,destination):
        destination_index=self.territory_list.index(destination)
        if destination_index==self.curr_location_index:
            movements.speak("I am already at {}".format(destination))
        else:
            movements.speak("Target Destination {}".format(destination))
            instructions=self.territory_routing[self.curr_location_index][destination_index]
            for instruction_tuple in instructions:
                myfunc=self.__getattribute__(instruction_tuple[0])
                myfunc(instruction_tuple[1])
            self.curr_location_index=destination_index
            movements.speak("Arrived at {}".format(destination))

    def get_coffee(self):
        starting=self.curr_location_index
        self.go_to_location("CoffeeLocation")
        movements.fetchCoffee()
        self.go_to_location(self.territory_list[starting])

    def react(self,*args):
        action=self.__getattribute__(args[0])
        if hasattr(action, '__call__'):
            return action(*args[1:])
        else:
            return str(action)

