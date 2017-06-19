#!/usr/bin/env python3
from world.abstract.orientation.directions import Direction, opposite, left, right, strDirection
from world.ev3controls import movements
import threading
import configparser
from random import randint
from time import sleep

cp = configparser.ConfigParser()
cp.read("../ev3controls/map.cfg")
known_routings = eval(cp.get("map", "routings"), {}, {})
known_names = eval(cp.get("map", "names"), {}, {})
_turning = "turn"
_running = "run"
_go_to_flag = "go"


class MyCompanion(object):

    facingDirection=Direction.NORTH
    territory_list=known_names
    curr_location_index=0  # if 0 meaning it's at territory_list[0], etc...
    territory_routing =  known_routings
    wandering_memory=[]
    starting_posn=0
    ending_posn=0
    roaming=False
    in_transit=False

    def __init__(self, direction=None):
        if direction is not None:
            self.facingDirection=direction
        # self.start_roaming()

    def turn(self, direction):
        if not isinstance(direction, Direction):
            try:
                direction=strDirection(direction)
            except:
                raise TypeError("Not a valid Direction {}".format(repr(direction)))

        if self.facingDirection==direction:
            pass
        elif self.facingDirection==opposite(direction):
            print("turning 180 degree")
            movements.turnback()
        else:
            left_yes=(self.facingDirection-direction)%2 if self.facingDirection<2 else (self.facingDirection-direction)%2-1
            #Because if N or S, you need to turn left when the difference is odd; if W or E, turn left when the difference is even
            if left_yes:
                print("turning left")
                movements.turnleft()
            else:
                print("turning right")
                movements.turnright()
        self.facingDirection=direction
        print("Now facing {}".format(direction))
        movements.speak("Now facing {}".format(direction))
        return str(self.facingDirection)

    def run(self, distance):
        print("running by distance {}".format(distance))
        movements.run_by_distance(distance)

    def _reverse(self, origin_i, destination_i):
        instruction_tuples=self.territory_routing[destination_i][origin_i]
        reversed_instructions = []
        turning_cursor = 0
        runing_cursor = 0

        for instruction_tuple in instruction_tuples:
            if instruction_tuple[0] == _go_to_flag:
                return [instruction_tuples[0],(_go_to_flag,self.territory_list[destination_i])]
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

    def go(self,destination):
        if self.wandering_memory: #go back to last known location if you've ben wandering
            instructions=self._reverse(self.wandering_memory)
            self._do_as_instructed(instructions)
            self.wandering_memory=[]
        destination_index=self.territory_list.index(destination)
        movements.speak("Target Destination {}".format(destination))
        print("Target Destination {}".format(destination))
        if destination_index==self.curr_location_index:
            print("I am already at {}".format(destination))

            return("I am already at {}".format(destination))
        elif destination_index>self.curr_location_index:
            instructions=self._reverse(self.curr_location_index,destination_index)
            self._do_as_instructed(instructions)
        else:
            instructions=self.territory_routing[self.curr_location_index][destination_index]
            self._do_as_instructed(instructions)
        self.curr_location_index=destination_index
        print ("Arrived at {}".format(destination))
        return("Arrived at {}".format(destination))

    def go_to_location(self,destination):
        self.in_transit=True
        self.go(destination)
        self.in_transit=False

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

    def __start_roaming(self):
        self.roaming=True
        while self.roaming:
            target_index=randint(0, len(self.territory_list)-1)
            print("target index {}".format(target_index))
            self.go_to_location(self.territory_list[target_index])

    def start_roaming(self):
        t1 = threading.Thread(target=self.__start_roaming)
        t1.start()
        return("Started roaming")

    def stop_roaming(self):
        self.roaming=False
        while self.in_transit:
            sleep(1)
        movements.wait_till_finish()
        return("I just stopped roaming around")

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

