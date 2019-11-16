import numpy as np

from map_objects.tile import Tile
from map_objects.rooms import Room, RoomRect

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dugout = np.array([[]])

    def __str__(self):
        strlist = [''] * self.height
        for x in range(self.width):
            for y in range(self.height):
                if [x,y] in self.dugout:
                    strlist[x] += '.'
                else:
                    strlist[x] += '#'

        return '\n'.join(strlist)


    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles
    
    def clear_check(self, space1, space2):
        for pt in space1:
            if pt in space2:
                return False
        
        return True

    def get_neighbors(self, point):
        return [point + [1,0], point + [0,1],
                point + [-1,0], point + [0,-1]]

    def get_bounds(self, space):
        bounds = np.array([])
        for point in space:
            for neighbor in self.get_neighbors(point):
                if neighbor not in space and neighbor not in bounds:
                    np.append(bounds, neighbor, axis = 0)

        return bounds

    def attach_room(self, room, pt, tries = 4):
        for _ in range(tries):
            if self.clear_check(room.space + pt, self.dugout):
                return True
            else:
                room.transforms[np.random.randint(len(room.transforms))]()
            
            return False

    #generate map
    def make_map(self, maxrooms):

        # make initial room
        initroom = RoomRect(10,10, hallwaychance = 0)
        
        # place somewhere random on map
        initroom.spaces += [np.random.randint(1, self.height - 10),
                            np.random.randint(1, self.width - 10)]

        # stamp onto temporary list of spots to dig out
        self.dugout = initroom.spaces

        for _ in range(maxrooms):
            # make a new room
            newroom = RoomRect(np.random.randint(5,10), np.random.randint(5,10))
            
            # find place for newroom
            for attach_pt in self.get_bounds(self.dugout):
                if self.attach_room(newroom, attach_pt):
                    np.append(self.dugout, newroom.spaces + attach_pt)

if __name__ == '__main__':
    a = Map(50,50)
    a.make_map(25)