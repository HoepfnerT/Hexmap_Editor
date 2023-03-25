class Hex_Coords_Handler():
    """
    Keeps track of coordinates in hexagonal and euclidean forms.
    Hexagonal Coords: u = right, v = up right, (w = up left), Euclidean Coords: x = right, y = up
    A: (u,v,w) = (u-w, v+w) ---> (x,y)          Ainv: (x,y) ---> (u,v,0)  
    A      = ( SQRT3, SQRT3/2 )                 Ainv   = ( 1/SQRT3, -1/3 )
             (   0,     3/2   )                          (    0,     2/3 )          
    """

    @staticmethod
    def hex_to_eucl(u,v,w=0):   return (((u-w)+(v+w)/2)* 3**0.5, 3*(v+w)/2) 
    @staticmethod
    def eucl_to_hex(x,y):       return (x/3**0.5-y/3, 2*y/3)
  
    def __init__(self, u, v, w = 0):    self.u, self.v = u-w, v+w 

    @classmethod
    def from_eucl_coords(cls, x, y):
        u, v = cls.eucl_to_hex(x,y)
        return cls(round(u), round(v))

    def get_hex_coords(self):       return (self.u, self.v)
    def get_hex_tile(self):         return (round(self.u), round(self.v))
    def get_eucl_coords(self):      return self.hex_to_eucl(self.u, self.v)
    def set_coords(self, u,v):      self.u, self.v = u, v
    def set_coords_eucl(self, x,y): self.u, self.v = self.eucl_to_hex(x,y)

    
    ##### DUNDER METHODS FOR ARITHMETICS #####

    def __repr__(self):                         return f"Hex_Coords_Handler({self.u},{self.v})"
    def __str__(self):                          return f"Hex Coordinates (u,v) = {self.get_hex_coords()}, at euclidean coordinates (x,y) = {self.get_eucl_coords()}."
    def __nonzero__(self):                      return (self.u == 0 and self.v == 0)
    def __eq__(self,other):                     return (self.u == other.u and self.v == other.v)
    def __add__(self, other): 
        if type(other) == Hex_Coords_Handler:   return Hex_Coords_Handler(self.u + other.u, self.v + other.v)
        if type(other) == tuple:                return Hex_Coords_Handler(self.u + other[0], self.v + other[1])
        raise TypeError(f"Cannot resolve Hex_Coords_Handler.__add__() for: {repr(self)} + {repr(other)}.", )
    def __iadd__(self, other): 
        if type(other) == Hex_Coords_Handler:
            self.u = self.u + other.u
            self.v = self.v + other.v
        elif type(other) == tuple:
            self.u = self.u + other[0]
            self.v = self.v + other[1]
        else:
            raise TypeError(f"Cannot resolve Hex_Coords_Handler.__iadd__() for: {repr(self)} += {repr(other)}.", )
        return self
    def __radd__(self, other):                  return self + other
    def __sub__(self, other):   
        if type(other) == Hex_Coords_Handler:   return Hex_Coords_Handler(self.u - other.u, self.v - other.v)
        if type(other) == tuple:                return Hex_Coords_Handler(self.u - other[0], self.v - other[1])
        raise TypeError(f"Cannot resolve Hex_Coords_Handler.__sub__() for: {repr(self)} - {repr(other)}.", )
    def __isub__(self, other): 
        if type(other) == Hex_Coords_Handler:
            self.u = self.u - other.u
            self.v = self.v - other.v
        elif type(other) == tuple:
            self.u = self.u - other[0]
            self.v = self.v - other[1]
        else:
            raise TypeError(f"Cannot resolve Hex_Coords_Handler.__isub__() for: {repr(self)} -= {repr(other)}.", )
        return self
    def __rsub__(self, other):                  return self - other
    def __mul__(self, other):                   
        if type(other) in [int, float]:         return Hex_Coords_Handler(other * self.u, other * self.v)
        raise TypeError(f"Cannot resolve Hex_Coords_Handler.__mul__() for: {repr(self)} * {repr(other)}.", )
    def __imul__(self, other):
        self.u, self.v = self.u * other, self.v * other
        return self
    def __rmul__(self, other):                  return self * other
    def __div__(self, other):                   
        if type(other) in [int, float]:         return Hex_Coords_Handler(self.u / other, self.v / other)
        raise TypeError(f"Cannot resolve Hex_Coords_Handler.__div__() for: {repr(self)} / {repr(other)}.", )
    def __rdiv__(self, other):                  return self / other
    def __idiv__(self,other):
        self.u, self.v = self.u / other, self.v/other
        return self
    def __truediv__(self, other):               return self.__div__(other)
    def __rtruediv__(self,other):               return self.__rdiv__(other)
    def __itruediv__(self, other):              return self.__idiv__(other)
    def __neg__(self):                          return Hex_Coords_Handler(-self.u, -self.v)
    def __abs__(self):                          return self.u + self.v                                  #hexagonal disctance to origin
    def __len__(self):                          return (3*((self.u+self.v)**2 - self.u*self.v))**0.5    #euclidean distance to origin