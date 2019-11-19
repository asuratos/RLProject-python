import numpy as np

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

    def add_hallway(self, maxlen = 5):

        for _ in range(maxlen):
            if np.random.rand() < self.hallwaychance:
                self.halllength += 1
                self.spaces = np.append(self.spaces, [[0,self.halllength]], axis = 0)
                if self.halllength > 1:
                    self.boundary = np.append(self.boundary, [[-1, self.halllength],
                                                            [1, self.halllength]], axis = 0) 
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
        body = np.array([[x,y] for x in range(w) for y in range(h)])
        bounds = np.array([[x,y] for x in range(-1, w) for y in range(-1, h)])

        shift = [-np.random.randint(self.w), self.halllength]
        body += shift
        self.spaces = np.append(self.spaces, body, axis = 0)

        self.boundary += shift
        self.boundary = bounds[~((bounds[:, None, :] == body).all(1)).any(1)]
        
