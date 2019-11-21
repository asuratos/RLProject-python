import numpy as np

# make hallway class maybe

class Room:
    def __init__(self, hallwaychance = 0.75):
        self.spaces = np.array([[0,0]])
        self.boundary = np.array([[0,0]])

        self.hallwaychance = hallwaychance
        self.halllength = 0

        self.transforms = [self.rotate_left,
                           self.rotate_right,
                           self.mirror_horizontal,        
                           self.mirror_vertical]

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
    
    def update_boundary(self):
        pass
        
    def add_hallway(self, maxlen = 3):
        for _ in range(maxlen):
            if np.random.rand() < self.hallwaychance:
                self.halllength += 1
                self.spaces = np.vstack((self.spaces, [[0,self.halllength]]))
            else:
                break

    def mirror_horizontal(self):
        self.spaces = self.spaces * [-1, 1]
        self.boundary = self.boundary * [-1, 1]

    def mirror_vertical(self):
        self.spaces = self.spaces * [1, -1]
        self.boundary = self.boundary * [1, -1]

    def rotate_right(self):
        self.spaces = self.spaces.dot([[0,-1],[1,0]])
        self.boundary = self.boundary.dot([[0,-1],[1,0]])

    def rotate_left(self):
        self.spaces = self.spaces.dot([[0,1],[-1,0]])
        self.boundary = self.boundary.dot([[0,1],[-1,0]])

    def collission_check(self,other):
        for pt in self.spaces:
            if (other.spaces[:] == pt).all(1).any():
                return True
        return False
    

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
        self.boundary = self.get_bounds(self.spaces)

    def generate_body(self, w, h):
        body = [[x,y] for x in range(w) for y in range(h)]

        if self.shift:
            shift = np.array([-np.random.randint(1, self.w-1), self.halllength+1])
            body += shift
        
        #self.spaces = np.append(self.spaces, body, axis = 0)
        self.spaces = np.vstack((self.spaces, body))
        
        
