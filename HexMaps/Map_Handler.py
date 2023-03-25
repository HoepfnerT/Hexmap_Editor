from pygame.math import Vector2
from Map import Map
from Hex_Coords_Handler import Hex_Coords_Handler as HexCoords
from Selection_Tile import Selection_Tile

class Map_Handler():
    """
    Keep track of information of the map, including
    Offset, Scaling, two selected squares.
    """
    def __init__(self, map = Map(), offset = HexCoords(0,0), scale = 20, main_select = Selection_Tile(), secondary_select = Selection_Tile()):
        self.MAP    = map
        self.offset = offset
        self.scale  = scale
        self.main_select, self.secondary_select = main_select, secondary_select
        self.selects = [self.main_select, self.secondary_select]
        self.key_to_tile = {i: i for i in range(10)}
        

    def new_map(self): 
        self.MAP    = Map()
        self.offset = HexCoords(0,0)
        self.scale  = 20
        self.main_select, self.secondary_select = Selection_Tile(), Selection_Tile()
        self.selects = [self.main_select, self.secondary_select] 
        
    def change_key_to_tile(self, key, tile):
        try: self.key_to_tile[key] = tile
        except KeyError: print("Wrong key.")

    def get_key_to_tile(self, key):
        return self.key_to_tile[key]

    # load/save map from file
    def load_map_from_file(self, filename = "map.data" ):   self.MAP.load_from_file(filename)
    def save_map_to_file(self, filename = "map.data" ):     self.MAP.save_to_file(filename)
    # set a tile on the map
    def set_tile_on_map(self, u,v, key): self.MAP.set_tile(u,v,self.key_to_tile[key])    
    def set_tiles_on_map(self, lst, key): 
        for u,v in lst: self.MAP.set_tile(u,v,self.key_to_tile[key])    
    def shift_offset(self, u,v): self.offset += (u,v)
    
    # Get if tiles selected 
    def get_select(self, secondary=0):        return self.selects[secondary].is_active()
    # Get selected tiles screen coordinates
    def get_select_coords(self, secondary=0): 
        for hex in self.selects[secondary].get_hex_tile():
            yield self.hex_to_screen_coords(*hex)
    def get_select_tile(self, secondary=0):   return self.selects[secondary].get_hex_tile()
    def increase_selection_radius(self, inc, secondary = 0):
        self.selects[secondary].increase_radius(inc)
    # get scaling factor
    def get_scale(self):                return self.scale


    # return corners of the polygon centered at x,y
    def hexshape(self, x, y):
        offset, v = Vector2(x, y), Vector2(0,-self.scale)
        return [ v.rotate(d) + offset for d in range(0,361,60) ]
    # return for all visible hexes content and shape on screen as (content, [list of corners]) 
    def get_visible_hexes(self, width, height):
        for tile_id, pos in self.MAP.get_visible_hexes(width/self.scale, height/self.scale, top_left = self.offset.get_hex_tile()): 
            yield (tile_id, self.hex_to_screen_coords(*pos), self.scale)


    # change scaling factor, keep focus on focus point
    def change_scale(self, incr, focus):     
        coords_focus    = self.screen_to_coords(*focus)
        coords_origin   = self.screen_to_coords(0,0)
        self.offset    += coords_focus - coords_origin
        self.scale     += incr
        self.scale      = min(max(self.scale, 10),100)
        coords_focus    = self.screen_to_coords(*focus)
        coords_origin   = self.screen_to_coords(0,0)
        self.offset    -= coords_focus - coords_origin


    # compute screen coords 
    def get_screen_coords(self, p: HexCoords):  return ((p-self.offset)*self.scale).get_eucl_coords()
    def hex_to_screen_coords(self, u, v):       return self.get_screen_coords(HexCoords(u,v))
    def screen_to_coords(self, x, y):           return HexCoords.from_eucl_coords(x,y)/self.scale + self.offset
    def screen_to_hex_coords(self, x, y):       return self.screen_to_coords(x,y).get_hex_coords()

    # Select Hexagon as 0 = main, 1 = secondary
    def select(self, x,y, secondary = 0):     
        self.selects[secondary].select(*self.screen_to_hex_coords(x,y))
     # Move selected tile with weadyx-Keys
    def move_select(self, s, secondary=0):            self.selects[secondary].move(s)
    # Move offset with mouse
    def move_with_mouse(self, rel):             self.offset -= HexCoords.from_eucl_coords(*rel)/self.scale    
