import numpy as np

from map.mapgen.dig import Digger
from map.tiles import TileFactory

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def initialize_digger(self, floortype = 'default'):
        self.digger = Digger(self.w, self.h, floortype)
    
    def dig_floor(self):
        self.digger.dig_floor()

    def initialize_tiles(self):
        # todo: write interface class for Digger -> Tilelist init
        _floors = np.argwhere(self.digger.floor).tolist()
        _doors = self.digger.doors.tolist()

        _tilefactory = TileFactory()
        self.tiles = [None] * self.w * self.h

        for _y in range(self.h):
            for _x in range(self.w):
                if [_x, _y] in _floors:
                    self.tiles[_x][_y] = _tilefactory.generate_tile('floor')
                elif [_x, _y] in _doors:
                    self.tiles[_x][_y] = _tilefactory.generate_tile('door_closed')
                else:
                    self.tiles[_x][_y] = _tilefactory.generate_tile('wall')

    @property
    def floorgraph(self):
        return self.digger.floorgraph
    
    @property
    def roomgraph(self):
        return self.digger.roomgraph

    @property
    def floor(self):
        return self.digger.floor