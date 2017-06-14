#!/usr/bin/env python3
from world.abstract.orientation.directions import Direction, opposite, left, right, strDirection
from world.ev3controls import movements

_turning = "turn_to_direction"
_running = "run_by_distance"
_go_to_flag = "go_to_location"


class MyCompanion(object):

    facingDirection=Direction.NORTH
    territory_list=["Employee_Desk_A","MeetingRoom","CoffeeLocation"]
    curr_location_index=0  # if 0 meaning it's at Employee_Desk_A, etc...
    territory_routing =  [[[], [], []],
                         [[("turn_to_direction", "West"), ("run_by_distance", "50")], [], []],
                         [[("go_to_location", "MeetingRoom"), ("go_to_location", "Employee_Desk_A")],[("turn_to_direction", "North"), ("run_by_distance", "60")], []]]

    # territory_routing=[[[],[("turn_to_direction","East"),("run_by_distance","50")],[("go_to_location","MeetingRoom"),("go_to_location","CoffeeLocation")]],
    #                    [[("turn_to_direction","West"),("run_by_distance","50")],[],[("turn_to_direction","South"),("run_by_distance","60")]],
    #                    [[("go_to_location","MeetingRoom"),("go_to_location","Employee_Desk_A")],[("turn_to_direction","North"),("run_by_distance","60")],[]]]

    wandering_memory=[]
    starting_posn=0
    ending_posn=0

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

    def _reverse(self, origin_i, destination_i):
        instruction_tuples=self.territory_routing[destination_i][origin_i]
        reversed_instructions = []
        turning_cursor = 0
        runing_cursor = 0

        for instruction_tuple in instruction_tuples:
            if instruction_tuple[0] == _go_to_flag:
                return [instruction_tuples[1],(_go_to_flag,self.territory_list[destination_i])]
            elif instruction_tuple[0] == _turning:
                opposite_direction_s = str(opposite(strDirection(instruction_tuple[1]))).split(".")[1]
                reversed_instructions.insert(turning_cursor, (_turning,opposite_direction_s))
                turning_cursor+=1
                runing_cursor=turning_cursor
            elif instruction_tuple[0] == _running:
                reversed_instructions.insert(runing_cursor,instruction_tuple)
                turning_cursor=0
                runing_cursor+=1
            else:
                raise Exception("Unknown instruction")
        return reversed_instructions


    def _do_as_instructed(self,instructions):
        for instruction_tuple in instructions:
            myfunc=self.__getattribute__(instruction_tuple[0])
            myfunc(instruction_tuple[1])

    def go_to_location(self,destination):
        if self.wandering_memory: #go back to last known location if you've ben wandering
            instructions=self._reverse(self.wandering_memory)
            self._do_as_instructed(instructions)
            self.wandering_memory=[]
        destination_index=self.territory_list.index(destination)
        movements.speak("Target Destination {}".format(destination))
        if destination_index==self.curr_location_index:
            return("I am already at {}".format(destination))
        elif destination_index>self.curr_location_index:
            instructions=self._reverse(self.curr_location_index,destination_index)
            self._do_as_instructed(instructions)
        else:
            instructions=self.territory_routing[self.curr_location_index][destination_index]
            self._do_as_instructed(instructions)
        self.curr_location_index=destination_index
        return("Arrived at {}".format(destination))

    def turnLeft(self):
        movements.turnleft()
        self.facingDirection=left(self.facingDirection)

    def turnRight(self):
        movements.turnright()
        self.facingDirection=right(self.facingDirection)

    def turnBack(self):
        movements.turnback()
        self.facingDirection=opposite(self.facingDirection)

    def go_straight(self):
        self.starting_posn=movements.moveforward()
        return "Advancing"

    def stop(self):
        self.ending_position=movements.stop()
        travel_distance=self.ending_position-self.starting_posn
        if travel_distance>0:
            self.wandering_memory.append((_turning, str(self.facingDirection).split(".")[1]))
            self.wandering_memory.append((_running,str(travel_distance*(movements.cm_to_rots))))

    def mark(self, name):#flushing the routing memory
        last_known_index=self.curr_location_index
        last_known_name=self.territory_list[last_known_index]

        ref_for_dummy=[(_go_to_flag,last_known_name),(_go_to_flag,name)]
        for i in range(last_known_index,len(self.territory_list)):
            self.territory_routing[i].insert(last_known_index,ref_for_dummy)

        self.territory_list.insert(last_known_index,name)#register the location
        self.territory_routing[last_known_index].insert(last_known_index,self.wandering_memory)
        self.wandering_memory=[]
        ref_by_dummy=[]
        for j in range(0,last_known_index):
            ref_for_dummy.append([(_go_to_flag,last_known_name),(_go_to_flag,self.territory_list[j])])
        self.territory_routing.insert(last_known_index,ref_by_dummy)


    def react(self,*args):
        action=self.__getattribute__(args[0])
        if hasattr(action, '__call__'):
            return action(*args[1:])
        else:
            return str(action)

    #
    # def get_coffee(self):
    #     starting = self.curr_location_index
    #     self.go_to_location("CoffeeLocation")
    #     movements.fetchCoffee()
    #     self.go_to_location(self.territory_list[starting])

