import numpy as np

# from map_objects.tile import Tile
from mapgen.rooms import Room, RoomRect, RoomCross, RoomCircle
from mapgen.ca.ca import CAMap, Cave
from graphs.graph import Graph, GridGraph

class RoomWrapper:
    '''
    Interface class for rooms
    '''
    def __init__(self, room):
        self._room = room

    def __getattr__(self,attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        
        return getattr(self._room, attr)

    def shifted(self, shift):
        _shifted = self._room.spaces + shift
        return _shifted[:,0], _shifted[:,1]

class RoomPicker:
    '''
    Class that handles picking and generating rooms to send to the floor digger
    '''

    def __init__(self, w, h, profile = 'default'):
        self.floortypes = {
            'default': {
                'rooms' : [RoomRect, RoomCross, RoomCircle],
                'roomsp' : [0.35,0.45,0.2],
                'sizes' : ['small','medium','large'],
                'sizesp' : [0.55, 0.4, 0.05]
            },
            'allsquares':{
                'rooms' : [RoomRect],
                'roomsp' : None,
                'sizes' : ['small','medium','large'],
                'sizesp' : [0.3, 0.5, 0.2]
            },
            'allcircles':{
                'rooms' : [RoomCircle],
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
        if Cave in self.profile['rooms']:
            _CAMap = CAMap(w,h) 
            

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

        self.reset()

        self.roomgen = RoomPicker(width, height, floortype)

    def reset(self):        
        self.floorgraph = GridGraph()
        self.floor = np.zeros((self.width, self.height), dtype = int)
        self.doors = None

        self.connections = np.zeros((self.width, self.height), dtype = int)
        self.walls = np.empty_like(self.floor, dtype = '<U2')
        self.walls[:] = 'no'

        self.roomgraph = Graph()
        self.roomcount = 1
        
        
    def __str__(self):
        strlist = [''] * self.height
        for x in range(self.width):
            for y in range(self.height):
                pt = [x,y]
                if (self.doors == pt).all(1).any():
                    strlist[y] += '+'
                elif self.floor[x, y] > 0:
                    if self.lettersflag:
                        strlist[y] += f'{chr(ord("a") - 1 + self.floor[x,y])}'
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
        if (space1[:,0] >= self.width-1).any() or \
           (space1[:,1] >= self.height-1).any() or (space1 <= 0).any():
            return False
        
        # narrow down the search
        s1minx, s1miny = np.amin(space1, axis = 0)
        s1maxx, s1maxy = np.amax(space1, axis = 0)
        
        neighborhood = space2[(space2[:,1] >= s1miny) & 
                             (space2[:,1] <= s1maxy) &
                             (space2[:,0] >= s1minx) &
                             (space2[:,0] <= s1maxx)]

        for pt in space1:
            if (neighborhood[:] == pt).all(1).any():
                return False
        
        return True

    def place_door(self,pt):
        if self.doors is not None:
            self.doors = np.vstack((self.doors, pt))
        else:
            self.doors = pt
        
        self.floorgraph.add_node(pt.tolist())

    def dig_extradoors(self):
        # get list of possible points
        _u, _c = np.unique(self.connections[...,:-1], axis = 0, return_counts = True)
        
        # get list of points with exactly 2 connecting rooms
        _locs = _u[_c == 2]
        np.random.shuffle(_locs)
        
        # iterate over list
        for _pt in _locs:
            # get list of rooms attached to point
            _r1,_r2 = self.connections[(self.connections[...,:-1] == _pt).all(1)][...,-1]
            
            # if rooms are >2 rooms apart,            
            if self.roomgraph.get_dist(_r1, _r2) > 2:
                # poke hole
                self.place_door(_pt)
                
                # add connection to roomgraph
                self.roomgraph.add_edge(_r1,_r2)
                
            pass
        pass
    
    def attach_room(self, room, attach_pts):

        for pt in attach_pts:
            # border check
            if (pt <= 0).any() or (pt[0] >= self.width-1) or \
               (pt[1] >= self.height - 1):
                continue
            
            #this isn't correct
            _invalidpts = np.vstack((np.argwhere(self.walls != 'no'), np.argwhere(self.floor > 0)))
            
            if self.clear_check(room.spaces + pt, _invalidpts):

                self.roomcount += 1
                self.roomgraph.add_node(self.roomcount)
                self.roomgraph.add_edge(self.roomcount, 
                                        self.connections[(self.connections[:,:2] == pt).all(1)][0,-1])

                self.floorgraph.add_nodes((room.spaces + pt).tolist())

                self.floor[room.shifted(pt)] = self.roomcount 

                self.place_door(pt)

                _newwalls = None
                for key in room.boundary:
                    _address = room.boundary[key] + pt
                    self.walls[_address[:,0], _address[:,1]] = key

                    if _newwalls is not None:
                        _newwalls = np.vstack((_newwalls, _address))
                    else:
                        _newwalls = _address
                    
                _newwalls = np.c_[_newwalls, [self.roomcount]*_newwalls.shape[0]]

                self.connections = np.vstack((self.connections, 
                                              np.unique(_newwalls, axis = 0)))
                    
                return True
            
        return False

    #generate map
    def dig_floor(self, maxrooms):

        # make initial room
        initroom = RoomWrapper(RoomRect(size = 'medium', hallwaychance = 0))
        
        # place somewhere random on map
        shift = np.random.randint(1, min(self.width, self.height) - 9, size = 2)

        # stamp onto temporary list of spots to dig out
        self.floor[initroom.shifted(shift)] = self.roomcount
        self.floorgraph.set_nodes_fromlist = np.argwhere(self.floor != 1).tolist()
        
        for key in initroom.boundary:
            _address = initroom.boundary[key] + shift
            self.walls[_address[:,0], _address[:,1]] = key

        _walls = np.argwhere(self.walls != 'no')
        self.connections = np.c_[_walls, [self.roomcount]*_walls.shape[0]]

        self.roomgraph.add_node(self.roomcount)

        for _ in range(maxrooms):
            # make a new room
            newroom = self.roomgen.get_room(hallwaychance = 0.5)
            
            newroom.transform()
            
            # np.random.shuffle(self.walls)
            # find place for newroom
            for _ in range(2):
                if self.attach_room(newroom, np.argwhere(self.walls == newroom.facing)):
                    break
                else:
                    newroom.transform()

            
            if np.count_nonzero(self.floor) / (self.height*self.width) > 0.75:
                break

        # poke new doors here
        self.dig_extradoors()

if __name__ == '__main__':
    a = Digger(50,30)
    a.dig_floor(10)
    print(a)
