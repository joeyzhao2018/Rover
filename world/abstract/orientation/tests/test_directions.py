from world.abstract.orientation.directions import Direction, opposite

print(_json_config)

a=Direction.NORTH
b=Direction.SOUTH
c=Direction.EAST
d=Direction.WEST

print(str(a))

assert opposite(a)==b
assert opposite(b)==a
assert opposite(c)==d
assert opposite(d)==c

