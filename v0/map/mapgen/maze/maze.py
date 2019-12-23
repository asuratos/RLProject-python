import numpy as np

class Maze:
    def __init__(self, w, h):
        self.w = w
        self.h = h

        self.floor = np.zeros((w,h), dtype = int)
        self.walls = [] 

    def _get_neighbors(self, x, y):
        return self.floor[[x + 1, x - 1, x, x],
                          [y , y, y - 1, y +1]]

    
    def _count_neighbor_floor(self, x, y):
        return np.sum(self._get_neighbors(x, y))

    def _dig(self, x, y):
        self.floor[x, y] = 1
