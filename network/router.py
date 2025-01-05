import asyncio
from math import inf
from distance_vector.poison_reverse import get_poison_reverse

class Router:
    def __init__(self, id, neighbors):
        self.id = id
        self.vector = {}
        self.neighbors = neighbors
        self.queue = asyncio.Queue()

    def initialize_distance_vector(self, router_ids):
        for id in router_ids:
            if id == self.id:
                self.vector[id] = (0, self.id)
            else:
                self.vector[id] = (inf, "")
        for neighbor_id, cost in self.neighbors.items():
            self.vector[neighbor_id] = (cost, neighbor_id)
    
    async def send_distance_vector(self, routers):
        for neighbor_id in self.neighbors:
            await routers[neighbor_id].queue.put((self.id, self.vector))
    
    async def receive_distance_vector(self, routers):
        while True: 
            try:
                sender_id, distance_vector = await asyncio.wait_for(self.queue.get(), timeout=2)
                cost = self.neighbors[sender_id]

                if not get_poison_reverse():
                    # Bellman-Ford
                    for dest_id in self.vector:
                        new_cost = cost + distance_vector[dest_id][0]
                        if new_cost < self.vector[dest_id][0]: 
                            self.vector[dest_id] = (new_cost, sender_id)

                            print(f"Router {self.id} vector is updated using Router {sender_id} vector.")
                            for router in routers.values():
                                print(f"{router.id}: {router.vector}")
                            await self.send_distance_vector(routers)
                else:
                    # Poison reverse
                    for dest_id in self.vector:
                        if distance_vector[dest_id] == (inf, "") and self.vector[dest_id][1] == sender_id:
                            self.vector[dest_id] = (inf, "")

                            print(f"Router {self.id} vector is poisoned by Router {sender_id} vector.")
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
    