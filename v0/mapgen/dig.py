import numpy as np

# from map_objects.tile import Tile
from mapgen.rooms import Room, RoomRect, RoomCross
from graphs.graph import Graph

class RoomWrapper:
    '''
    Wrapper that flattens room vector coordinates into 1d form used by the map
    digger class
    '''
    def __init__(self, room):
        self._room = room

    def __getattr__(self,attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        
        return getattr(self._room, attr)

    @property
    def spaces(self):
        return self._room.spaces

    @property
    def boundary(self):
        return self._room.boundary

class RoomPicker:
    '''
    Class that handles picking and generating rooms to send to the floor digger
    '''
    def __init__(self, profile = 'default'):
        self.floortypes = {
            'default': {
                'rooms' : [RoomRect, RoomCross],
                'roomsp' : [0.5,0.5],
                'sizes' : ['small','medium','large'],
                'sizesp' : [0.45, 0.5, 0.05]
            },
            'allsquares':{
                'rooms' : [RoomRect],
                'roomsp' : None,
                'sizes' : ['small','medium','large'],
                'sizesp' : [0.3, 0.5, 0.2]
            },
            'allcrosses':{
                'rooms' : [RoomCross],
                'roomsp' : None,
                'sizes' : ['small','medium','large'],
                'sizesp' : [0.3, 0.5, 0.2]
            }
        }

        self.profile = self.floortypes[profile]

    def get_room(self, **params):
        _room = np.random.choice(self.profile['rooms'], p = self.profile['roomsp'])
        _size = np.random.choice(self.profile['sizes'], p = self.profile['sizesp'])
        return RoomWrapper(_room(size = _size, **params))


class Digger:
    def __init__(self, width, height, letters = False, floortype = 'default'):
        self.width = width
        self.height = height
        # self.tiles = self.initialize_tiles()
        self.lettersflag = letters # this flag shouldn't be in this class

        self.floor = np.zeros((self.width, self.height), dtype = int)
        self.doors = None
        self.connections = np.zeros((self.width, self.height), dtype = int)
        self.walls = {
            '+y' : [] ,
            '+x' : [] ,
            '-y' : [] ,
            '-x' : [] 
        }

        self.roomgraph = Graph()
        self.roomcount = 1

        self.roomgen = RoomPicker(floortype)

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
                    self.connections[room.boundary[key] + pt] = self.roomcount

                self.allbounds = np.hstack([bound for bound in self.walls.values()])
                return True
            
        return False

    #generate map
    def dig_floor(self, maxrooms):

        # make initial room
        initroom = RoomWrapper(RoomRect(size = 'medium', hallwaychance = 0))
        
        # place somewhere random on map
        shift = np.random.randint(min(self.width, self.height) - 9, size = 2)

        # stamp onto temporary list of spots to dig out
        self.floor[initroom.spaces + shift] = self.roomcount
        
        for key in self.walls:
            self.walls[key] = initroom.boundary[key] + shift
            self.connections[self.walls[key]] = self.roomcount

        self.allbounds = np.vstack([bound for bound in self.walls.values()])
        self.roomgraph.add_node(self.roomcount)

        for _ in range(maxrooms):
            # make a new room
            newroom = self.roomgen.get_room(hallwaychance = 0.5)
            
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
