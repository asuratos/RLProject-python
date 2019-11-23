import numpy as np

# make hallway class maybe

class Room:
    def __init__(self, hallwaychance = 0.75):
        self.spaces = np.array([[]])
        self.boundary = {
            '+y' : [] ,
            '+x' : [] ,
            '-y' : [] ,
            '-x' : [] 
        }

        self.facing_index = 0
        self.directions = ['+y', '+x', '-y', '-x']

        self.hallwaychance = hallwaychance
        self.halllength = 0

        self.transforms = [self.rotate_left,
                           self.rotate_right,
                           self.mirror_horizontal,        
                           self.mirror_vertical]

    @property
    def facing(self):
        return self.directions[self.facing_index]

    def get_neighbors(self, point):
        return point + np.array([[1,0],
                                 [-1,0],
                                 [0,1],
                                 [0,-1]])

    def get_bounds(self):
        
        dirs = {
            '+x' : [[1,0]],
            '+y' : [[0,1]],
            '-x' : [[-1,0]],
            '-y' : [[0,-1]]
        }

        _bounds = {}
        for key in self.directions:
            _bound = self.spaces + dirs[key]
            _bounds[key] = np.array([pt for pt in _bound 
                        if (self.spaces[:]!=pt).all(1).any()])

        return _bounds

    def add_hallway(self, maxlen = 3):
        for _ in range(maxlen):
            if np.random.rand() < self.hallwaychance:
                self.halllength += 1
                if self.halllength == 1:
                    self.spaces = np.array([[0,1]])
                else:
                    self.spaces = np.vstack((self.spaces, [[0,self.halllength]]))
            else:
                break

    def mirror_horizontal(self):
        self.spaces = self.spaces * [-1, 1]

        self.boundary = self.get_bounds()
        
        self.facing_index = (self.facing_index + 2) % 4

    def mirror_vertical(self):
        self.spaces = self.spaces * [1, -1]

        self.boundary = self.get_bounds()

        self.facing_index = (self.facing_index + 2) % 4

    def rotate_right(self):
        self.spaces = self.spaces.dot([[0,-1],[1,0]])

        self.boundary = self.get_bounds()

        self.facing_index = (self.facing_index + 1) % 4

    def rotate_left(self):
        self.spaces = self.spaces.dot([[0,1],[-1,0]])

        self.boundary = self.get_bounds()

        self.facing_index = (self.facing_index - 1) % 4
    

class RoomRect(Room):
    def __init__(self, w, h, hallwaychance = 0.5, shift = True):
        super().__init__(hallwaychance)
        self.w = w
        self.h = h
        self.shift = shift

        if np.random.rand() < self.hallwaychance:
            self.add_hallway()
        
        # make a rectangle
        self.generate_body(self.w, self.h)
        self.boundary = self.get_bounds()

    def generate_body(self, w, h):
        body = np.array([[x,y] for x in range(w) for y in range(h)])

        if self.shift:
            shift = np.array([-np.random.randint(1, self.w-1), self.halllength+1])
            body += shift
        
        if self.halllength == 0:
            self.spaces = body
        else:
            self.spaces = np.vstack((self.spaces, body))
        
        
