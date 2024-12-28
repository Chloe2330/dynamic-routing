from math import inf
from network.network import NetworkGraph

class Router:
    def __init__(self, id, num_routers):
        self.id = id
        self.vector = [inf for _ in range(num_routers)]
        self.set_self_index()
    
    def set_self_index(self):
        index = int(self.id)
        self.vector[index] = (0, self.id)

    def initialize_distance_vector(self, neighbors):
        for neighbor_id, cost in neighbors:
            index = int(neighbor_id)
            self.vector[index] = (cost, neighbor_id)
