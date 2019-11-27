import numpy as np

# from map_objects.tile import Tile
from mapgen.rooms import Room, RoomRect
from graphs.graph import Graph

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
    def __init__(self, width, height, letters = False):
        self.width = width
        self.height = height
        # self.tiles = self.initialize_tiles()
        self.lettersflag = letters

        self.floor = np.zeros((self.width * self.height), dtype = int)
        self.doors = None
        self.connections = np.zeros((self.width * self.height), dtype = int)
        self.walls = {
            '+y' : [] ,
            '+x' : [] ,
            '-y' : [] ,
            '-x' : [] 
        }

        self.roomgraph = Graph()
        self.roomcount = 1

    def __str__(self):
        strlist = [''] * self.height
        for x in range(self.width):
            for y in range(self.height):
                pt = x + self.width * y
                if pt in self.doors:
                    strlist[y] += '+'
                elif self.floor[pt] > 0:
                    if self.lettersflag:
                        strlist[y] += f'{chr(ord("a") - 1 + self.floor[pt])}'
                    else:
                        strlist[y] += '.'
                else:
                    if self.lettersflag:
                        strlist[y] += '.'
                    else:
                        strlist[y] += '#'


        return '\n'.join(strlist)

    # def initialize_tiles(self):
    #     tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

    #     return tiles
    

    def clear_check(self, space1, space2):
        # check boundaries
        if (space1 // self.width == 0).any() or (space1 % self.width == 0).any() or  \
           ((space1+1) % self.width == 0).any() or (space1 // self.width == self.height -1).any():
            return False
        
        # narrow down the search
        s1miny = np.amin(space1 // self.width)
        s1maxy = np.amax(space1 // self.width)
        s1minx = np.amin(space1 % self.width)
        s1maxx = np.amax(space1 % self.width)
        
        neighborhood = space2[np.logical_and.reduce(np.stack((
            space2 // self.width >= s1miny,
            space2 // self.width <= s1maxy,
            space2 % self.width >= s1minx,
            space2 % self.width <= s1maxx
        )))]

        if np.intersect1d(space1, neighborhood).size != 0:
            return False
        
        return True

    def place_door(self,pt):
        if self.doors is not None:
            self.doors = np.append(self.doors, pt)
        else:
            self.doors = pt

    def attach_room(self, room, attach_pts):

        for pt in attach_pts:
            if (pt // self.width == 0) or ((pt+1) // self.width == self.height -1) or\
                (pt % self.width == 0) or ((pt+1) % self.width == 0):
                continue
            
            _invalidpts = np.append(self.allbounds, np.argwhere(self.floor > 0))
            
            if self.clear_check(room.spaces + pt, _invalidpts):

                self.roomcount += 1
                self.roomgraph.add_node(self.roomcount)
                self.roomgraph.add_edge(self.roomcount, self.connections[int(pt)])

                self.floor[room.spaces + pt] = self.roomcount 

                self.place_door(pt)

                for key in room.boundary:
                    self.walls[key] = np.hstack((self.walls[key], 
                                                 room.boundary[key] + pt))
                    for shift in room.boundary[key] + pt:
                        self.connections[int(shift)] = self.roomcount

                self.allbounds = np.hstack([bound for bound in self.walls.values()])
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
        self.floor[initroom.spaces + shift] = self.roomcount
        
        for key in self.walls:
            self.walls[key] = initroom.boundary[key] + shift
            for pt in initroom.boundary[key] + shift:
                self.connections[pt] = self.roomcount

        self.allbounds = np.vstack([bound for bound in self.walls.values()])
        self.roomgraph.add_node(self.roomcount)

        for _ in range(maxrooms):
            # make a new room
            newroom = RoomWrapper(RoomRect(np.random.randint(5,10), 
                                np.random.randint(5,10), hallwaychance=0.75),
                                self.width)
            newroom.transform()
            
            # np.random.shuffle(self.walls)
            # find place for newroom
            for _ in range(2):
                if self.attach_room(newroom, self.walls[newroom.facing]):
                    break
                else:
                    newroom.transform()

            
            if np.count_nonzero(self.floor) / (self.height*self.width) > 0.6:
                break

        # print('finish')

if __name__ == '__main__':
    a = Digger(50,30)
    a.dig_floor(10)
    print(a)
