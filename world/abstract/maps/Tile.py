from world.abstract.orientation.directions import Direction, opposite
from copy import copy

class Tile(object):
    neighbors=[None,None,None,None]
    name="origin"
    id_by_origin=[0,0,0,0]
    tag=[]
    origins=[]


    def __init__(self,name,neighbors=None, last_tile=None, new_movement=None):
        self.name=name

        if neighbors is not None:
            self.neighbors=neighbors

        elif isinstance(last_tile,Tile) and isinstance(new_movement,Direction):
            direction_from=opposite(new_movement)
            self.neighbors[direction_from]=last_tile
            self.id_by_origin=copy(last_tile.id_by_origin)
            self.id_by_origin[new_movement]+=1
            self.origins=copy(last_tile.origins)
            self.origins.append(new_movement)

