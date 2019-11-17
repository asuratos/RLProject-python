import numpy as np

from tile import Tile
from rooms import Room, RoomRect

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
                if np.any((self.dugout == [x, y]).all(1)):
                    strlist[x] += '.'
                else:
                    strlist[x] += '#'

        return '\n'.join(strlist)


    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles
    
    def clear_check(self, space1, space2):
        for pt in space1:
            if np.any((space2[:] == pt).all(1)):
                return False
        
        return True

    def get_neighbors(self, point):
        return point + np.array([[1,0],
                                 [-1,0],
                                 [0,1],
                                 [0,-1]])

    def get_bounds(self, space):
        bounds = []
        for point in space:
            for neighbor in self.get_neighbors(point):
                if not np.any((space[:] == neighbor).all(1)):
                    bounds.append(neighbor)

        return np.array(bounds)

    def attach_room(self, room, pt, tries = 4):
        for _ in range(tries):
            if self.clear_check(room.spaces + pt, self.dugout):
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
            candidate_pts = self.get_bounds(self.dugout)
            for attach_pt in candidate_pts:
                if self.attach_room(newroom, attach_pt):
                    self.dugout = np.append(self.dugout, 
                                            newroom.spaces + attach_pt,
                                            axis = 0)
                    break

        print('finish')

if __name__ == '__main__':
    a = Map(50,50)
    a.make_map(1)
    print(a)