import numpy as np

class CAMap:
    def __init__(self, w, h):
        self.w = w

        # can change this to distribution so it's not just a coin flip
        self.spaces = np.random.randint(0,2,shape=(w*h))

    def find_blobs(self):
        pass

    def set_rule(self, rule):
        pass

    def step(self):
        _nxt = self.rule(self.spaces)
        self.space = _nxt
