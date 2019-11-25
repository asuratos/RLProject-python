import numpy as np

# from map_objects.tile import Tile
from mapgen.rooms import Room, RoomRect

class RoomWrapper:
    '''
    Wrapper that flattens room vector coordinates into 1d form used by the map
    digger class
    '''
    def __init__(self, room, mapwidth):
        self._room = room
        self.mapwidth = mapwidth

    def __getattr__(self,attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        
        return getattr(self._room, attr)

    @property
    def spaces(self):
        return self._room.spaces[:,0] + (self.mapwidth * self._room.spaces[:,1])

    @property
    def boundary(self):
        return {key : bound[:,0] + (self.mapwidth * bound[:,1]) for (key,bound) in self._room.boundary.items()}


class Digger:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # self.tiles = self.initialize_tiles()

        self.floor = np.array([[]])
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
                pt = x + self.width * y
                if pt in self.doors:
                    strlist[y] += '+'
                elif pt in self.floor:
                    strlist[y] += '.'
                else:
                    strlist[y] += '#'

        return '\n'.join(strlist)

    # def initialize_tiles(self):
    #     tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

    #     return tiles
    
    def flatten(self, space):
        return space[:,0] + (space[:,1] * self.width)


    def clear_check(self, space1, space2):
        # check boundaries
        if (space1 <= self.width).any() or (space1 % self.width == 0).any() or  \
           ((space1+1) % self.width == 0).any() or (space1 >= ((self.width -1) * self.height)).any():
            return False
        
        # figure out how to narrow down the thing
        # s1mins = space1.min(0)
        # s1maxs = space1.max(0)

        # neighborhood = space2[np.logical_and((space2 >= s1mins).all(1),(space2 <= s1maxs).all(1))]
        if np.intersect1d(space1, space2).size != 0:
            return False
        
        return True

    def place_door(self,pt):
        if self.doors is not None:
            self.doors = np.append(self.doors, pt)
        else:
            self.doors = pt

    def attach_room(self, room, attach_pts):

        for pt in attach_pts:
            
            if self.clear_check(room.spaces + pt, self.allbounds):

                self.floor = np.append(self.floor, room.spaces + pt)

                self.place_door(pt)

                for key in room.boundary:
                    self.walls[key] = np.hstack((self.walls[key], 
                                                 room.boundary[key] + pt))

                self.allbounds = np.hstack([bound for bound in self.walls.values()])

                self.roomcount += 1
                return True
            
        return False

    #generate map
    def dig_floor(self, maxrooms):

        # make initial room
        initroom = RoomWrapper(RoomRect(10,10, hallwaychance = 0, shift = 0),
                            self.width)
        
        # place somewhere random on map
        shift = np.random.randint(1, self.width - 10) + \
                (np.random.randint(1, self.height - 10) * self.width)

        # stamp onto temporary list of spots to dig out
        self.floor = initroom.spaces + shift
        
        for key in self.walls:
            self.walls[key] = initroom.boundary[key] + shift

        self.allbounds = np.vstack([bound for bound in self.walls.values()])

        for _ in range(maxrooms):
            # make a new room
            newroom = RoomWrapper(RoomRect(np.random.randint(5,10), 
                                np.random.randint(5,10), hallwaychance=0.75),
                                self.width)
            np.random.choice(newroom.transforms)()
            
            # np.random.shuffle(self.walls)
            # find place for newroom
            for _ in range(2):
                if self.attach_room(newroom, self.walls[newroom.facing]):
                    break
                else:
                    np.random.choice(newroom.transforms)()

            
            if self.floor.shape[0] / (self.height*self.width) > 0.6:
                break

        print('finish')

if __name__ == '__main__':
    a = Digger(50,30)
    a.dig_floor(10)
    print(a)