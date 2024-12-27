from math import inf
from network.network import NetworkGraph

class Router:
    def __init__(self, name, num_routers):
        self.name = name
        self.vector = [inf for _ in range(num_routers)]
        self.set_self_index(num_routers)
    
    def set_self_index(self, num_routers):
        index = self.name_to_index(self.name)
        if index < num_routers:
            self.vector[index] = 0
        self.set_neighbor_index()

    def set_neighbor_index(self):
        network = NetworkGraph()
        network.update_from_config('config.json')
        for neighbor, cost in network.links[self.name]:
            index = self.name_to_index(neighbor)
            self.vector[index] = cost

    def name_to_index(self, name):
        return ord(name) - ord('A')
