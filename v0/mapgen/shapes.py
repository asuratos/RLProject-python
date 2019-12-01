import numpy as np

def BuildRectangle(w, h):
    return np.array([[x,y] for x in range(w) for y in range(h)])
