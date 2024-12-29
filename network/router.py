import asyncio
from math import inf

class Router:
    def __init__(self, id, num_routers, neighbors):
        self.id = id
        self.vector = [(inf, "") for _ in range(num_routers)]
        self.vector[int(self.id)] = (0, self.id)
        self.neighbors = neighbors
        self.queue = asyncio.Queue()

    def initialize_distance_vector(self):
        for neighbor_id, cost in self.neighbors.items():
            index = int(neighbor_id)
            self.vector[index] = (cost, neighbor_id)
    
    async def send_distance_vector(self, routers):
        for neighbor_id in self.neighbors:
            await routers[neighbor_id].queue.put((self.id, self.vector))
    
    async def receive_distance_vector(self, routers):
        while True: 
            try:
                sender_id, distance_vector = await asyncio.wait_for(self.queue.get(), timeout=2)
                cost = self.neighbors[sender_id]

                # Bellman-Ford
                for i in range(len(self.vector)):
                    new_cost = cost + distance_vector[i][0]
                    if new_cost < self.vector[i][0]:
                        self.vector[i] = (new_cost, sender_id)

                        print(f"Router {self.id} vector is updated using Router {sender_id} vector.")
                        for router in routers.values():
                            print(f"{router.id}: {router.vector}")
                        await self.send_distance_vector(routers)
    
            except asyncio.TimeoutError:
                break

    async def run_dvr(self, routers):
        await asyncio.gather(
            self.send_distance_vector(routers),
            self.receive_distance_vector(routers)
        )
    