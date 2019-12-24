from map.mapgen.dig import Digger
from map.tiles import Tile

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h

        pass

    def initialize_digger(self, floortype = 'default'):
        self.digger = Digger(self.w, self.h, floortype)

    def initialize_tiles(self):
        self.tiles = [Tile() for _ in range(self.w * self.h)]
    
    def dig_floor(self):
        self.digger.dig_floor()