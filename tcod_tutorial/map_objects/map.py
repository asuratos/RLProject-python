import numpy as np

from map_objects.tile import Tile
from map_objects.rooms import Room, RoomRect

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles
    
    #generate map
    def make_map(self):
        for _ in range(50):
            pass
