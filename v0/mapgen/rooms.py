import numpy as np

# make hallway class maybe

class Room:
    def __init__(self, size = 'medium', hallwaychance = 0.75):
        self.spaces = np.array([[]], dtype = int)
        self.boundary = {
            '+y' : [] ,
            '+x' : [] ,
            '-y' : [] ,
            '-x' : [] 
        }
        self.size = size

        self.facing_index = 0
        self.directions = ['+y', '+x', '-y', '-x']

        self.hallwaychance = hallwaychance
        self.halllength = 0

        self.transforms = [None,
                           self.rotate_left,
                           self.rotate_right,
                           self.mirror_horizontal,        
                           self.mirror_vertical]

    @property
    def facing(self):
        return self.directions[self.facing_index]

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
        self.halllength = np.random.randint(1, maxlen+1)

        self.spaces = np.hstack((np.zeros((self.halllength,1), dtype = int), 
                          np.arange(1, self.halllength+1, dtype = int)[:,None]))

    def transform(self):
        _choice = np.random.choice(self.transforms)
        if _choice:
            _choice()
        
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if np.random.rand() < self.hallwaychance:
            self.add_hallway()
        
        # make a rectangle
        self.generate_body(self.size)
        self.boundary = self.get_bounds()

    def generate_body(self, size):
        _dims = {
            'template' : ('min','max'),
            'small' : (3,5),
            'medium' : (5,10),
            'large' : (10,15)
        }
       
        _roomw = np.random.randint(*_dims[size])
        _roomh = np.random.randint(*_dims[size])
               
        body = np.array([[x,y] for x in range(_roomw) for y in range(_roomh)], dtype = int)

        shift = np.array([-np.random.randint(1, _roomw-1), self.halllength+1])
        body += shift
        
        if self.halllength == 0:
            self.spaces = body
        else:
            self.spaces = np.vstack((self.spaces, body))
        
        
class RoomCross(Room):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if np.random.rand() < self.hallwaychance:
            self.add_hallway()
        
        self.generate_body(self.size)
        self.boundary = self.get_bounds()

    def generate_body(self, size):
        _dims = {
            'template' : ('min','max'),
            'small' : (3,5),
            'medium' : (4,12),
            'large' : (8,15)
        }
        
        _r1w = np.random.randint(*_dims[size])
        _r1h = np.random.randint(*_dims[size]) + np.random.randint(*_dims[size])
        
        r1 = np.array([[x,y] for x in range(_r1w) for y in range(_r1h)], dtype = int)

        shift = np.array([-np.random.randint(1, _rw1-1), self.halllength+1])
        r1 += shift
        
        _r2w = _r1w + np.random.randint(*_dims[size])
        _r2h = _r1h - np.random.randint(1, _r1h - 1)
        
        r2 = np.array([[x,y] for x in range(_r2w) for y in range(_r2h)], dtype = int)

        shift += np.array([-np.random.randint(1, _r2w-_r1w), np.random.randint(1,_r1h-_r2h)])
        r2 += shift

        body = np.unique(np.vstack((r1,r2)), axis = 0)

        if self.halllength == 0:
            self.spaces = body
        else:
            self.spaces = np.vstack((self.spaces, body))
