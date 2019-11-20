import numpy as np

from map_objects.tile import Tile
from map_objects.rooms import Room, RoomRect

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dugout = np.array([[]])
        self.walls = np.array([[]])

        self.roomcount = 1

    def __str__(self):
        strlist = [''] * self.height
        for x in range(self.width):
            for y in range(self.height):
                if np.any((self.dugout == [x, y]).all(1)):
                    strlist[y] += '.'
                else:
                    strlist[y] += '#'

        return '\n'.join(strlist)


    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles
    
    def clear_check(self, space1, space2):
        if  (space1 < [1,1]).any() or (space1 > [self.width-1,self.height-1]).any():
            return False

        for pt in space1:
            if np.any((space2[:] == pt).all(1)):
                return False
        
        return True

    def attach_room(self, room, pt, tries = 10):
        _bounds = np.array([elem for elem in self.walls if (elem != pt).all()])
        _bounds = np.vstack((_bounds, self.dugout))

        for _ in range(tries):
            if self.clear_check(room.spaces + pt, _bounds):
                self.dugout = np.vstack((self.dugout, room.spaces + pt))
                self.walls = np.vstack((self.walls, room.boundary + pt))

                self.walls = self.walls[np.all(np.any((self.walls-self.dugout[:, None]), axis=2), axis=0)]
                self.roomcount += 1
                return True
            else:
                room.transforms[np.random.randint(len(room.transforms))]()
            
        return False

    #generate map
    def make_map(self, maxrooms):

        # make initial room
        initroom = RoomRect(10,10, hallwaychance = 0, shift = 0)
        
        # place somewhere random on map
        shift = [np.random.randint(1, self.width - 10),
                 np.random.randint(1, self.height - 10)]

        # stamp onto temporary list of spots to dig out
        self.dugout = initroom.spaces + shift
        self.walls = initroom.boundary + shift

        for _ in range(maxrooms):
            # make a new room
            newroom = RoomRect(np.random.randint(5,10), np.random.randint(5,10), hallwaychance=0.75)
            
            np.random.shuffle(self.walls)
            # find place for newroom
            for attach_pt in self.walls:
                 if self.attach_room(newroom, attach_pt):
                    break

        print('finish')

if __name__ == '__main__':
    a = Map(50,30)
    a.make_map(10)
    print(a)