import pickle, math

class Map:
    """
    Stores the map as a 2D-Array and can yield all visible tiles.
    """

    def __init__(self, map = [], top=0, left=0):
        self.top, self.left, self.map = top, left, map
    def set_map(self, map): self.map = map
    def get(self,x,y):
        if x < self.left or y < self.top:   return 0
        try:                                return self.map[y - self.top][x - self.left]
        except IndexError:                  return 0

    def save_to_file(self, filename = "map.data"):
        with open(filename, 'wb') as f: pickle.dump([self.top, self.left, self.map], f)

    def load_from_file(self, filename = "map.data"):
        with open(filename, 'rb') as f: self.top, self.left, self.map = pickle.load(f)

    def set_empty(self):    self.top, self.left, self.map = 0,0,[[0]]

    def set_tile(self, u,v, val):
        print(self.map)
        x, y = u + v//2, v
        while x < self.left:
            for row in self.map:
                print(1)
                row.insert(0,0)
            self.left -= 1
        while x-self.left >= len(self.map[0]):
            for row in self.map:
                print(2)
                row.append(0)
        while y < self.top:
            print(3)
            self.map.insert(0, [0 for x in self.map[0]])
            self.top -= 1
        while y - self.top >= len(self.map):        
            print(4)
            self.map.append([0 for x in self.map[0]])
        self.map[y - self.top][x - self.left] = val

    # yield the content and (u,v) location of all visible tiles, computed with hexwidth = 1.
    def get_visible_hexes(self, width, height, top_left = (0,0)):
        nr_rows = int(height/1.5)+1
        nr_cols = int(width/3**0.5)+1
        for y in range(nr_rows+2,-2,-1):
            for x in range(top_left[1]//2-2, nr_cols+top_left[1]//2+2):
                lshift = (y+top_left[1])%2 * math.floor((y+top_left[1])/2) + (1-(y+top_left[1])%2)*math.ceil((y+top_left[1])/2)
                yield (self.get(x+top_left[0], y+top_left[1]), (top_left[0]+x-lshift, top_left[1]+y))

    def __str__(self): return str(self.map)