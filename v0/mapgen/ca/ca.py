import numpy as np

from mapgen.ca.carules import ruleCave

def findrooms(map):
    '''
    Takes 2d array of 0s and 1s, returns list of lists,
    where each element is a list of connected points
    '''
    
    _spaces = np.argwhere(map == 1) #Nx2 np array of positions of 1s
    np.random.shuffle(_spaces)
    
    _rooms = []
    
    #pick point in _spaces
    #find all points directly connected to that
    # repeat until no more neighbors
    # if there are still points in spaces, find next room
    
    # just implement skimage? or scipy.ndimage.label, unless I can figure out how to vectorize


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
