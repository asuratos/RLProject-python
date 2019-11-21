import numpy as np

# make hallway class maybe

class Room:
    def __init__(self, hallwaychance = 0.75):
        self.entryway = np.array([[0,0]], dtype = float)
        self.boundary = np.array([[0,0]])
        self.w = 0
        self.h = 0

        self.hallwaychance = hallwaychance
        self.halllength = 0

        self.transforms = [self.rotate_left,
                           self.rotate_right,
                           self.mirror_horizontal,        
                           self.mirror_vertical]

    def mirror_horizontal(self):
        self.spaces = self.spaces[:,::-1]

        self.entryway -= [self.w/2, self.h/2]
        self.entryway *= [-1,1]
        self.entryway += [self.w/2, self.h/2]

    def mirror_vertical(self):
        self.spaces = self.spaces[::-1,:]

        self.entryway -= [self.w/2, self.h/2]
        self.entryway *= [1,-1]
        self.entryway += [self.w/2, self.h/2]

    def rotate_right(self):
        self.spaces = self.spaces.T[:,::-1]

        self.entryway -= [self.w/2, self.h/2]
        self.entryway = self.entryway.dot([[0,-1],[1,0]])
        self.entryway += [self.w/2, self.h/2]

    def rotate_left(self):
        self.spaces = self.spaces.T[::-1,:]

        self.entryway -= [self.w/2, self.h/2]
        self.entryway = self.entryway.dot([[0,1],[-1,0]])
        self.entryway += [self.w/2, self.h/2]
    

class RoomRect(Room):
    def __init__(self, w, h, hallwaychance = 0.5, shift = True):
        super().__init__(hallwaychance)
        self.w = w
        self.h = h
        self.shift = shift
        
        # make a rectangle
        self.generate_body(self.w, self.h)

        if np.random.rand() < self.hallwaychance:
            self.add_hallway()

    def add_hallway(self, maxlen = 3):
        hall_pt = np.random.randint(1, self.h - 1)
        hall_len = np.random.randint(1, maxlen + 1)

        self.entryway[:,1] += hall_pt
        self.h += hall_len
        
        hall = np.zeros((self.w, hall_len))
        hall[:,hall_pt] += 1 
        self.spaces = np.hstack((hall, self.spaces))

    def generate_body(self, w, h):
        self.spaces = np.ones((h,w))
        
        
print('finish')