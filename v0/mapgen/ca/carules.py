import numpy as np

def _count_neighbors_VN(space):
    _neighbors = np.sum(np.stack((np.roll(space, 1, axis = 0),
                                  np.roll(space, -1, axis = 0),
                                  np.roll(space, 1, axis = 1),
                                  np.roll(space, -1, axis = 1))), 
                                  axis = 0)

    return _neighbors

def _count_neighbors_M(space):
    _neighbors = np.sum(np.stack((np.roll(space, 1, axis = 0),
                                  np.roll(space, -1, axis = 0),
                                  np.roll(space, 1, axis = 1),
                                  np.roll(space, -1, axis = 1),
                                  np.roll(space, (1,1), axis = (0,1)),
                                  np.roll(space, (-1,1), axis = (0,1)),
                                  np.roll(space, (-1,1), axis = (0,1)),
                                  np.roll(space, (-1,-1), axis = (0,1)))), 
                                  axis = 0)

    return _neighbors

def RuleCave(space):
    _neighbors = _count_neighbors_M(space)
    _new = np.zeros_like(space) 
   

    # on points where space = 1, apply death rules
    _new[(space == 1) & (_neighbors > 4)] = 0

    #on points where space = 0, apply birth rules
    _new[(space == 0) & (_neighbors > 2) & (_neighbors < 5)] = 1
    
    return _new
