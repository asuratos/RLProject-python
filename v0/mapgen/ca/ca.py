import numpy as np

from mapgen.ca.carules import ruleCave

def _manhattandistance(pt, vectors):
    '''
    calculates manhattan distance between a point and an array of vectors
    '''
    _diffs = vectors - pt
    return np.sum(_diffs, axis = -1)


def labelrooms(map):
    '''
    Takes 2d array of 0s and 1s, returns labelled 2darray
    and count of number of rooms
    '''
    
    _spaces = np.argwhere(map == 1) #Nx2 np array of positions of 1s
    _labelled = np.zeros_like(map)
    
    _rooms = []
    _unvisited = _spaces.tolist()
    _visited = set()
    _frontier = []

    # initialize starting point
    _current = np.random.choice(_unvisited)
    # just use a queue object dammit
    while len(_unvisited) > 0:
        # get valid neighbors of current point
        
        # for each neighbor
            # if neighbor in _unvisited, add to _frontier, remove from _unvisited
            # if neighbor in _visited, discard

        pass


class CAMap:
    def __init__(self, w, h, alive = 0.5):
        self.rule = None
        self.spaces = np.random.choice([0,1],size = (w, h), p = [1-alive,alive])

    def find_blobs(self):
        pass

    def set_rule(self, rule):
        self.rule = rule

    def step(self):
        _nxt = self.rule(self.spaces)
        self.spaces = _nxt

class Cave:
    pass
