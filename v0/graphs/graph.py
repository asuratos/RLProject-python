from graphs.pathfinding import bfs_dist, bfs_greedy

class Graph:
    '''
    General graph class for pathfinding, etc
    '''
    def __init__(self):
        self.nodes = []
        self.edges = {}

    def __str__(self):
        rep = [f'{key}:{value}' for (key,value) in self.edges.items()]
        return '\n'.join(rep) 

    def add_node(self, id):
        self.nodes.append(id)
    
    def add_edge_oneway(self, id1, id2):
        if id1 not in self.edges.keys():
            self.edges[id1] = []

        self.edges[id1].append(id2)
    
    def add_edge(self, id1, id2):
        self.add_edge_oneway(id1, id2)
        self.add_edge_oneway(id2, id1)
    
    def get_neighbors(self, id):
        if id in self.edges.keys():
            return self.edges[id]
        return None
    
    def get_dist(self, id1, id2):
        dists = bfs_dist(self, id1, id2)
        return dists[id2]

class GridGraph:
    '''
    Graph-like class that handles the special case of the
    square grid (e.g floor tiles)
    Initialized with load_nodes_fromlist, which takes a Nx2
    list of positions of walkable tiles.
    get_neighbors returns a list of tuples, as the pathfinding algotithms
    need immutable types to use as dict keys
    '''
    def __init__(self):
        self.nodes = []
        
    def __contains__(self, id):
        return list(id) in self.nodes
        
    def add_node(self, id: list):
        self.nodes.append(id)

    def add_nodes(self, ids: list):
        self.nodes.extend(ids)
    
    def set_nodes_fromlist(self, vec: list):
        self.nodes = vec
    
    def get_neighbors(self, id):
        x, y = id
        neighbors = [[x + 1, y],
                     [x - 1, y],
                     [x, y + 1],
                     [x, y - 1]]
        return [tuple(pt) for pt in neighbors if pt in self.nodes]

    def get_dists(self, pt):
        _dists = bfs_dist(self, pt)
        return _dists

    def get_path(self, pt1, pt2):
        _path = bfs_greedy(self, pt1, pt2)
        return _path
