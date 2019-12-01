import numpy as np

def _count_neighbors_VN(space):
    _neighbors = np.sum(np.stack((np.roll(space, 1, axis = 0),
                                  np.roll(space, -1, axis = 0),
                                  np.roll(space, 1, axis = 1),
                                  np.roll(space, -1, axis = 1))), 
                                axis = 0)

    return _neighbors

def RuleCave(space):
    _neighbors = _count_neighbors_VN(space)

    # on points where space = 1, apply death rules
    space[space == 1] = _neighbors[space == 1] 

    #on points where space = 0, apply birth rules

    pass
