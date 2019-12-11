from collections import deque

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    @property
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()

def floodfill(graph, start):
    '''
    From a graph and a point in the graph, 
    finds the locations on the graph that are accessible from 
    the starting point, and gives the distance in steps from the
    start
    '''
    
    frontier = Queue()
    frontier.put(start)
    
    distance = {}
    distance[start] = 0
    
    while not frontier.empty:
        current = frontier.get()
        for next in graph.get_neighbors(current):
            if next not in distance:
                frontier.put(next)
                distance[next] = 1 + distace[current]
                
    return visited
