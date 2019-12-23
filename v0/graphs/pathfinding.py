from collections import deque

from graphs.heuristics import manhattandist

class Queue:
    def __init__(self):
        self.elements = deque()
    
    @property
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()

class PriorityQueue:
    def __init__(self):
        self.elements = []
          
    @property
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x, prio):
        self.elements.append((x, prio))
    
    def get(self):
        #should return the element with the lowest priority
        best = (None, 300)
        for element in self.elements:
            if element[-1] < best[-1]:
                best = element 

        self.elements.remove(best)
        return best[0]

def bfs_dist(graph, start, goal = None):
    '''
    From a graph and a point in the graph, 
    finds the locations on the graph that are accessible from 
    the starting point, and gives the distance in steps from the
    start.
    
    If a goal is provided, then it will exit as soon as the goal becomes the 
    current node.
    '''
    
    frontier = Queue()
    frontier.put(start)
    
    distance = {}
    distance[start] = 0
    
    while not frontier.empty:
        current = frontier.get()
        
        if goal and current == goal:
            break
        
        for next in graph.get_neighbors(current):
            if next not in distance:
                frontier.put(next)
                distance[next] = 1 + distance[current]
                
    return distance

def astar(graph, start, goal, h = manhattandist):
    '''
    From a graph and a point in the graph, 
    finds the locations on the graph that are accessible from 
    the starting point, and gives the distance in steps from the
    start.
    
    If a goal is provided, then it will exit as soon as the goal becomes the 
    current node.
    '''
    
    frontier = PriorityQueue()
    frontier.put(start,0)
    
    comes_from = {}
    comes_from[start] = 0
        
    dist_so_far = {}
    dist_so_far[start] = 0

    while not frontier.empty:
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.get_neighbors(current):
            _currentdist = dist_so_far[current] + 1
            if (next not in comes_from) and (dist_so_far.get(next, 100) > _currentdist):
                frontier.put(next, _currentdist + h(next, goal))
                comes_from[next] = current
                dist_so_far[next] = _currentdist
                                
    return comes_from, dist_so_far
