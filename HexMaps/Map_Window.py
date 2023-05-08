import pygame
import time, math, sys
from pygame.math import Vector2
from Map_Handler import Map_Handler
import Tools
import Event_Handler


class Map_Window:

    def __init__(self, MAP_HANDLER, MAP_FPS = 10, WINDOW_WIDTH = 1200, WINDOW_HEIGHT = 900, STARTING_SCALE = 20, TITLE = "Hexmap Editor"):
        
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.MAP_FPS                           = MAP_FPS

        ## CONSTANTS ##
        self.WHITE, self.GRAY1, self.GRAY2, self.GRAY3, self.BLACK, self.RED, self.GREEN, self.BLUE = (255,255,255), (192,192,192), (128,128,128), (64,64,64), (0,0,0), (200,0,0), (0,200,0), (0,0,200)
        self.SHADING                            = [self.GRAY1, self.GRAY2, self.GRAY3, self.BLACK, self.WHITE]
        self.BORDER_WIDTH                       = 2
        self.SIDEBAR_WIDTH_QUOTIENT             = 3
        self.BLINK                              = Tools.Blink(self.MAP_FPS/4) # Alternating between True and False


        self.WINDOW_WIDTH, self.WINDOW_HEIGHT   = (WINDOW_WIDTH, WINDOW_HEIGHT) 
        self.WINDOW_RECT                        = pygame.Rect(0,0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.DISPLAY                            = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.RESIZABLE)
        self.CANVAS                             = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.MAP_WIDTH, self.MAP_HEIGHT          = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.MAP_TOPLEFT                         = (0,0)

        self.MAP_RECT                            = pygame.Rect(*self.MAP_TOPLEFT, self.MAP_WIDTH, self.MAP_HEIGHT)

        self.STARTING_SCALE                     = STARTING_SCALE
        self.HEX_IMG_WIDTH, self.HEX_IMG_HEIGHT = (567, 655)
        self.HEX_BORDER                         = 0.025


        self.TILES_DICT_SCALE                   = self.STARTING_SCALE
        self.TILES_DICT                         = {}
        self.DISPLAY_DICT                       = {}
        self.RESCALE_IMG                        = lambda scale: (math.ceil((2+self.HEX_BORDER)*scale*self.HEX_IMG_WIDTH/self.HEX_IMG_HEIGHT), math.ceil((2+self.HEX_BORDER)*scale))
        
        self.MAP_HANDLER                        = MAP_HANDLER
        self.MAP_HANDLER.load_map_from_file()
        
    def new_map(self):
        self.MAP_HANDLER.new_map()

    def on_resize(self):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT     = pygame.display.get_surface().get_size()
        self.DISPLAY                         = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.RESIZABLE)
        self.CANVAS                          = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
    
        self.SIDEBAR_WIDTH, self.SIDEBAR_HEIGHT   = (int(min(self.WINDOW_HEIGHT/self.SIDEBAR_WIDTH_QUOTIENT, self.WINDOW_WIDTH/self.SIDEBAR_WIDTH_QUOTIENT)), self.WINDOW_HEIGHT)
        self.MAP_WIDTH, self.MAP_HEIGHT         = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.MAP_RECT                       = pygame.Rect(*self.MAP_TOPLEFT, self.MAP_WIDTH, self.MAP_HEIGHT)

    
    def rescale_dict(self, scale):    # rescale the hex images 
        if self.TILES_DICT_SCALE == scale: return 
        for key, img in self.TILES_DICT.items(): 
                self.TILES_DICT[key] = pygame.transform.scale(pygame.image.load(f"hex_tiles/{key}.png").convert_alpha(), self.RESCALE_IMG(scale))
        self.TILES_DICT_SCALE = scale

    def clear(self):
        self.DISPLAY.fill((255,255,255))

    def draw_map(self):
        # reset background
        pygame.draw.rect(self.DISPLAY, self.BLACK, self.WINDOW_RECT)
        pygame.draw.rect(self.DISPLAY, self.WHITE, self.MAP_RECT)
        # draw hexes
        self.rescale_dict(self.MAP_HANDLER.get_scale()) # check if rescaling needed
        for tile, pos, scale in self.MAP_HANDLER.get_visible_hexes(self.MAP_WIDTH, self.MAP_HEIGHT):
            if tile not in self.TILES_DICT: 
                try: self.TILES_DICT[tile] = pygame.transform.scale(pygame.image.load(f"hex_tiles/{tile}.png").convert_alpha(), self.RESCALE_IMG(scale))
                except: 
                    print(f"Tile {tile} not found.")
                    continue
            self.DISPLAY.blit(self.TILES_DICT[tile], pos - Vector2(scale,scale) + self.MAP_TOPLEFT)
            #pygame.draw.polygon(self.DISPLAY, self.SHADING[tile], hex)
        #blink main select or secondary select
        if self.BLINK.toggle():
            if self.MAP_HANDLER.get_select(): 
                for hex in self.MAP_HANDLER.get_select_coords():
                    pygame.draw.polygon(self.DISPLAY, self.GREEN, self.MAP_HANDLER.hexshape(*hex))
        else:
            if self.MAP_HANDLER.get_select(secondary = 1): 
                for hex in self.MAP_HANDLER.get_select_coords(secondary=1):
                    pygame.draw.polygon(self.DISPLAY, self.BLUE, self.MAP_HANDLER.hexshape(*hex))
        #draw border
        pygame.draw.rect(self.DISPLAY, self.BLACK, self.MAP_RECT, width=self.BORDER_WIDTH )


    def draw(self):
        self.draw_map()
        #self.draw_sidebar()
        
    def handle_event(self, event):
        Event_Handler.handle_event(event, self.MAP_HANDLER, self.MAP_RECT)