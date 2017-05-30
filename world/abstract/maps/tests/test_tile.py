from world.abstract.maps import Tile

a=Tile.Tile("a")
b=Tile.Tile("b",[a,None,None,None])
c=Tile.Tile("c",[b,None,None,None])

c.neighbors[0].id="i have a new name now"
print(b.id)