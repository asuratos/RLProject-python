class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = {}

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

