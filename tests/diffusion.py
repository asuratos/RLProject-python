import numpy as np

class ElementMap():
    def __init__(self, h = 10, w = 10):
        self.values = np.zeros((h,w))
        self.coeff = np.ones((h,w))*0.25
    
    def set_value(self, x, y, val):
        self.values[y,x] = val 

    def map(self):
        return self.values

    def diffuse(self):
        newvalues = (self.values[:-2, 1:-1]* np.sqrt(self.coeff[1:-1,1:-1] * self.values[:-2,1:-1]) +
                     self.values[2:, 1:-1] * np.sqrt(self.coeff[1:-1,1:-1] * self.values[2:,1:-1]) +
                     self.values[1:-1,:-2] * np.sqrt(self.coeff[1:-1,1:-1] * self.values[1:-1,:-2]) +
                     self.values[1:-1,2:]  * np.sqrt(self.coeff[1:-1,1:-1] * self.values[1:-1,2:]))/ 4
        
        return newvalues

    def update(self):
        self.values[1:-1, 1:-1] = self.diffuse()

if __name__ == '__main__':
    test = ElementMap()
    test.set_value(1,1,10)
    test.update()