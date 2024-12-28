import asyncio
from math import inf

class Router:
    def __init__(self, id, num_routers, neighbors):
        self.id = id
        self.vector = [(inf, "") for _ in range(num_routers)]
        self.set_self_index()
        self.neighbors = neighbors
        self.queue = asyncio.Queue()
    
    def set_self_index(self):
        index = int(self.id)
        self.vector[index] = (0, self.id)

    def initialize_distance_vector(self):
        for neighbor_id, cost in self.neighbors.items():
            index = int(neighbor_id)
            self.vector[index] = (cost, neighbor_id)
    
    async def send_distance_vector(self, routers):
        for neighbor_id in self.neighbors:
            await routers[neighbor_id].queue.put((self.id, self.vector))
    
    async def receive_distance_vector(self):
        sender_id, distance_vector = await self.queue.get()
        await self.update_distance_vector(sender_id, distance_vector)
    
    async def update_distance_vector(self, sender_id, distance_vector):
        updated = False
        cost = self.neighbors[sender_id]

        # Bellman-Ford
        for i in range(len(self.vector)):
            new_cost = cost + distance_vector[i][0]
            if new_cost < self.vector[i][0]:
                self.vector[i] = (new_cost, sender_id)
                updated = True 

        return updated 

    async def dvr(self, routers):
        await asyncio.gather(self.send_distance_vector(routers), self.receive_distance_vector())
        