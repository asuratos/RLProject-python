import numpy as np

from map_objects.tile import Tile
from map_objects.rooms import Room, RoomRect

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dugout = np.array([[]])
        self.doors = None
        self.walls = {
            '+y' : [] ,
            '+x' : [] ,
            '-y' : [] ,
            '-x' : [] 
        }

        self.roomcount = 1

    def __str__(self):
        strlist = [''] * self.height
        for x in range(self.width):
            for y in range(self.height):
                if np.any((self.doors == [x,y]).all(1)):
                    strlist[y] += '+'
                elif np.any((self.dugout == [x, y]).all(1)):
                    strlist[y] += '.'
                else:
                    strlist[y] += '#'

        return '\n'.join(strlist)

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles
    
    def clear_check(self, space1, space2):
        if  (space1 < [1,1]).any() or (space1 > [self.width-2,self.height-2]).any():
            return False
        
        s1mins = space1.min(0)
        s1maxs = space1.max(0)

        neighborhood = space2[np.logical_and((space2 >= s1mins).all(1),(space2 <= s1maxs).all(1))]

        for pt in neighborhood:
            if np.any((space1[:] == pt).all(1)):
                return False
        
        return True

    def place_door(self,pt):
        if self.doors is not None:
            self.doors = np.vstack((self.doors, pt))
        else:
            self.doors = pt

    def attach_room(self, room, attach_pts):

        for pt in attach_pts:
            if self.clear_check(room.spaces + pt, self.allbounds):

                self.dugout = np.vstack((self.dugout, room.spaces + pt))

                self.place_door(pt)

                for key in room.boundary:
                    self.walls[key] = np.vstack((self.walls[key], 
                                                 room.boundary[key] + pt))

                self.allbounds = np.vstack([bound for bound in self.walls.values()])

                self.roomcount += 1
                return True
            
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
        
        for key in self.walls:
            self.walls[key] = initroom.boundary[key] + shift
        self.allbounds = np.vstack([bound for bound in self.walls.values()])

        for _ in range(maxrooms):
            # make a new room
            newroom = RoomRect(np.random.randint(5,10), np.random.randint(5,10), hallwaychance=0.75)
            np.random.choice(newroom.transforms)()
            
            # np.random.shuffle(self.walls)
            # find place for newroom
            for _ in range(2):
                if self.attach_room(newroom,self.walls[newroom.facing]):
                    break
                else:
                    np.random.choice(newroom.transforms)()

            
            if self.dugout.shape[0] / (self.height*self.width) > 0.6:
                break

        print('finish')

if __name__ == '__main__':
    a = Map(50,30)
    a.make_map(10)
    print(a)