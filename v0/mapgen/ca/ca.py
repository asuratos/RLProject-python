import numpy as np

class CAMap:
    def __init__(self, w, h):
        self.rule = None

        # can change this to distribution so it's not just a coin flip
        self.spaces = np.random.randint(0,2,size = (w, h))
        self.count_neighbors_VN()

    def count_neighbors_VN(self):
        _neighbors = np.sum(np.stack((np.roll(self.spaces, 1, axis = 0),
                                      np.roll(self.spaces, -1, axis = 0),
                                      np.roll(self.spaces, 1, axis = 1),
                                      np.roll(self.spaces, -1, axis = 1))), 
                                      axis = 0)

        self.neighbors = _neighbors
        


    def find_blobs(self):
        pass

    def set_rule(self, rule):

        pass

    def step(self):
        _nxt = self.rule(self.spaces)
        self.space = _nxt
