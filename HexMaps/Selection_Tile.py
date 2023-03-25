from Hex_Coords_Handler import Hex_Coords_Handler as HexCoords


class Selection_Tile():
    """ 
        Keep track of a hex tile.
        Can be active or inactive, can be moved around with key inputs
    """ 
    def __init__(self, coords = HexCoords(0,0), active = False):
        self.coords, self.active = coords, active
        self.radius = 1
    def is_active(self):                        return self.active
    def toggle(self):                           self.active = not self.active
    def set_active(self, active: bool):         self.active = abs
    def set_eucl_coords(self, x,y):             self.coords.set_eucl(x,y)
    def set_hex_coords(self, u,v):              self.coords.set(u,v)
    def increase_radius(self, inc):             self.radius = min(10, max(1, self.radius + inc))
    def get(self):                              return (self.active, self.coords)
    def get_radius(self):                       return self.radius
    def get_hex_coords(self):      
        for r in range(self.radius+1):
            for u in range(r):
                for v in range(r): 
                    yield (self.coords + HexCoords(u,-v)).get_hex_coords()
                    yield (self.coords + HexCoords(-u,v)).get_hex_coords()
                for w in range(1,u): 
                    yield (self.coords + HexCoords(u,0,w)).get_hex_coords()
                    yield (self.coords + HexCoords(-u,0,-w)).get_hex_coords()
    def get_hex_tile(self):
        for u,v in self.get_hex_coords():
            yield (round(u),round(v))
    def get_coords(self):                       return self.coords
    def select(self, u,v):
        tile = HexCoords(u,v)
        if self.coords == tile:     self.toggle()
        else:                       self.coords, self.active = tile, True
    # move according to weadyx k
    def move(self, key):
        if key == "s": self.toggle()
        elif key == "w": self.coords += (0,-1)
        elif key == "e": self.coords += (1,-1)
        elif key == "a": self.coords += (-1,0)
        elif key == "d": self.coords += (1,0)
        elif key == "y" or key == "z": self.coords += (-1,1)
        elif key == "x": self.coords += (0,1)