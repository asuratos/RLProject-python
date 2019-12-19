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
        
        if size not in _dims:
            size = 'medium'
       
        _roomw = np.random.randint(*_dims[size])
        _roomh = np.random.randint(*_dims[size])
               
        body = np.array([[x,y] for x in range(_roomw) for y in range(_roomh)], 
                        dtype = int)

        if self.halllength > 0:
            shift = np.array([-np.random.randint(1, _roomw-1), 
                              self.halllength+1])
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
            'medium' : (4,6),
            'large' : (5,7)
        }
        
        if size not in _dims:
            size = 'medium'
        
        _r1w = np.random.randint(*_dims[size])
        _r1h = _r1w + np.random.randint(*_dims[size])
        
        r1 = np.array([[x,y] for x in range(_r1w) for y in range(_r1h)], 
                      dtype = int)

        shift = np.array([-np.random.randint(1, _r1w-1), self.halllength+1])
        r1 += shift
        
        _r2w = _r1w + np.random.randint(*_dims[size])
        _r2h = _r1h - np.random.randint(1, _r1h - 1)
        
        r2 = np.array([[x,y] for x in range(_r2w) for y in range(_r2h)], 
                      dtype = int)

        shift += np.array([-np.random.randint(0, _r2w-_r1w), 
                           np.random.randint(0,_r1h-_r2h)])
        r2 += shift

        body = np.unique(np.vstack((r1,r2)), axis = 0)

        if self.halllength == 0:
            self.spaces = body
        else:
            self.spaces = np.vstack((self.spaces, body))

class RoomCircle(Room):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transforms = [None,
                           self.rotate_left,
                           self.rotate_right]

        if np.random.rand() < self.hallwaychance:
            self.add_hallway()
        
        self.generate_body(self.size)
        self.boundary = self.get_bounds()
    
    def _incircle(self, x, y, r):
        return x*x + y*y < r*r
        

    def generate_body(self,size):
        _dims = {
            'template' : ('minradius', 'maxradius'),
            'small' : (2,4),
            'medium' : (4,6),
            'large' : (6,8)
        }
        
        if size not in _dims:
            size = 'medium'
        
        _r = np.random.randint(*_dims[size])
        
        _body = []
        for _y in range(-_r,_r + 1):
            for _x in range(-_r,_r + 1):
                if self._incircle(_x, _y, _r + 0.5):
                    _body.append([_x,_y])

        _body = np.array(_body) + [0, self.halllength + int(_r) + 1]
        
        if self.halllength == 0:
            self.spaces = _body
        else:
            self.spaces = np.vstack((self.spaces, _body))