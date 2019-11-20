import numpy as np

# make hallway class maybe

class Room:
    def __init__(self, hallwaychance = 0.75):
        self.spaces = np.array([[0,1]])
        self.boundary = np.array([[0,-1]]) 

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

    def get_bounds(self, space = self.spaces):
        bounds = []
        for point in space:
            for neighbor in self.get_neighbors(point):
                if not np.any((space[:] == neighbor).all(1)):
                    bounds.append(neighbor)
        return bounds
    
    def update_boundary(self):
        pass
        
    def add_hallway(self, maxlen = 5):
        for _ in range(maxlen):
            if np.random.rand() < self.hallwaychance:
                self.halllength += 1
                self.spaces = np.vstack((self.spaces, [[0,self.halllength]]))
                self.boundary = np.vstack((self.boundary, [[-1, self.halllength],
                                                           [1, self.halllength]])) 
            else:
                break

    def mirror_horizontal(self):
        self.spaces = self.spaces * [-1, 1]
        return self.spaces

    def mirror_vertical(self):
        self.spaces = self.spaces * [1, -1]
        return self.spaces

    def rotate_right(self):
        self.spaces = self.spaces.dot([[0,-1],[1,0]])
        return self.spaces

    def rotate_left(self):
        self.spaces = self.spaces.dot([[0,1],[-1,0]])
        return self.spaces

    def collission_check(self,other):
        for pt in self.spaces:
            if (other.spaces[:] == pt).all(1).any():
                return True
        return False
    

class RoomRect(Room):
    def __init__(self, w, h, hallwaychance = 0.5):
        super().__init__(hallwaychance)
        self.w = w
        self.h = h

        if np.random.rand() < self.hallwaychance:
            self.add_hallway()
        
        # make a rectangle
        self.generate_body(self.w, self.h)

    def generate_body(self, w, h):
        body = [[x,y] for x in range(h) for y in range(w)]
        bounds = [[x,y] for x in range(-1, h+1) for y in range(-1, w+1)]
        walls = [wall for wall in bounds if wall not in body]

        shift = np.array([-np.random.randint(self.w), self.halllength])
        body += shift
        walls += shift
        
        #self.spaces = np.append(self.spaces, body, axis = 0)
        self.spaces = np.vstack((self.spaces, body))
        
        #self.boundary = np.append(self.boundary, walls, axis = 0)
        self.boundary = np.vstack((self.boundary, walls))
        
