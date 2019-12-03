import numpy as np

from mapgen.ca.carules import RuleCave

class CAMap:
    def __init__(self, w, h):
        self.rule = None

        self.spaces = np.random.choice([0,1],size = (w, h), p = [0.5,0.5])

    def find_blobs(self):
        pass

    def set_rule(self, rule):
        self.rule = rule

    def step(self):
        _nxt = self.rule(self.spaces)
        self.space = _nxt
