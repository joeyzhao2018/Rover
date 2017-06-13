from world.abstract.orientation.directions import Direction, opposite


a=Direction.NORTH
b=Direction.SOUTH
c=Direction.EAST
d=Direction.WEST

print(str(a).split('.')[1])

assert opposite(a)==b
assert opposite(b)==a
assert opposite(c)==d
assert opposite(d)==c

