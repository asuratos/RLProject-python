import numpy as np

class Room:
    def __init__(self):
        self.spaces = np.array([[0,0]])
        self.boundary = np.array([]) 

        self.halllength = 0
        self.hallwaychance = 0.5

    def add_hallway(self, maxlen = 5):
        for _ in range(maxlen):
            if np.random.rand() > 0.5:
                self.halllength += 1
                np.append(self.spaces, [[0,self.halllength]], axis = 0)
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
            if pt in other.spaces:
                return True
        return False
    

class RoomRect(Room):
    def __init__(self, w, h):
        super().__init__()
        self.w = w
        self.h = h

        if np.random.rand() > self.hallwaychance:
            self.add_hallway()
        
        # make a rectangle
        self.generate_body(self.w, self.h)

    def generate_body(self, w, h):
        body = np.array([[x,y] for x in range(w) for y in range(h)])

        body += [0,self.halllength + 1] 
        body -= [np.random.randint(self.w),0]
        self.spaces = np.append(self.spaces, body, axis = 0)
