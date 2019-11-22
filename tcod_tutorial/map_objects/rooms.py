import numpy as np

# make hallway class maybe

class Room:
    def __init__(self):
        self.entryway = np.array([[0,0]], dtype = float)
        self.boundary = np.array([[0,0]])
        self.w = 0
        self.h = 0

        self.transforms = [self.rotate_left,
                           self.rotate_right,
                           self.mirror_horizontal,        
                           self.mirror_vertical]
    
    @property
    def centroid(self):
        return np.array([self.w/2, self.h/2])
        
    def mirror_horizontal(self):
        self.spaces = self.spaces[:,::-1]

        self.entryway -= self.centroid
        self.entryway *= [-1,1]
        self.entryway += self.centroid

    def mirror_vertical(self):
        self.spaces = self.spaces[::-1,:]

        self.entryway -= self.centroid
        self.entryway *= [1,-1]
        self.entryway += self.centroid

    def rotate_right(self):
        self.spaces = self.spaces.T[:,::-1]

        self.entryway -= self.centroid
        self.entryway = self.entryway[::-1] * [1,-1]
        self.entryway += self.centroid

    def rotate_left(self):
        self.spaces = self.spaces.T[::-1,:]

        self.entryway -= self.centroid
        self.entryway = self.entryway[::-1] * [-1,1]
        self.entryway += self.centroid
    

class RoomRect(Room):
    def __init__(self, w, h):
        super().__init__()
        self.w = w
        self.h = h
        
        # make a rectangle
        self.generate_body(self.w, self.h)

        self.add_hallway()

    def add_hallway(self, maxlen = 3):
        hall_pt = np.random.randint(1, self.h - 1)
        hall_len = np.random.randint(1, maxlen + 1)

        self.entryway[:,1] += hall_pt
        self.w += hall_len
        
        hall = np.zeros((hall_len, self.h))
        hall[:,hall_pt] += 1 
        self.spaces = np.vstack((hall, self.spaces))

    def generate_body(self, w, h):
        self.spaces = np.ones((w,h))
        
        
print('finish')
