import numpy as np

from map.mapgen.dig import Digger
from map.tiles import TileFactory

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def update_fov(self, new_start):
        pass
        # calculate fov
        # update visible/inviible flags

    def initialize_digger(self, floortype = 'default'):
        self.digger = Digger(self.w, self.h, floortype)
    
    def dig_floor(self):
        self.digger.dig_floor()

    def initialize_tiles(self):
        # todo: write interface class for Digger -> Tilelist init (generalize this)
        # can probably move this to the tile module
        _floors = np.argwhere(self.digger.floor).tolist()
        _doors = self.digger.doors.tolist()

        _tilefactory = TileFactory()
        self.tiles = [[None for _ in range(self.w)] for _ in range(self.h)]

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

    @property
    def is_walkable(self, x, y):
        return self.tiles[x][y].is_walkable

    @property
    def blocks_vision(self, x, y):
        return self.tiles[x][y].blocks_vision

    @property
    def is_seen(self, x, y):
        return self.tiles[x][y].is_seen
    
    @property
    def tileat(self, x ,y):
        return self.tiles[x][y]