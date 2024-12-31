from math import inf
from network.network import NetworkGraph
from network.router import Router

def main():
    network = NetworkGraph()
    network.update_from_config('config.json')

    num_routers = len(network.router_ids)
    routers = {}

    for id in network.router_ids:
        neighbors = network.links[id]
        router = Router(id, num_routers, neighbors)
        router.initialize_distance_vector()
        routers[id] = router
    
    return network, routers

async def update_network_continuously(network, routers):
    updated = False
    old_network = network

    new_network = NetworkGraph()
    new_network.update_from_config('config.json')
    num_routers = len(new_network.router_ids)

    # Change in network config 
    if old_network != new_network:
        updated = True 

        for id in new_network.router_ids:
            neighbors = new_network.links[id]
            neighbors_set = set()

            # Update neighbors in the network
            for neighbor_id, cost in neighbors.items():
                neighbors_set.add(neighbor_id)
                routers[neighbor_id].neighbors = new_network.links[neighbor_id]

            # New router added 
            if id not in routers.keys():
                router = Router(id, num_routers, neighbors)
                router.initialize_distance_vector()
                routers[id] = router

                for neighbor_id in neighbors_set: 
                    routers[neighbor_id].vector.insert(int(id), (cost, id))
                
                # Update non-neighbor in the network
                for router in routers.values():
                    if router.id not in neighbors_set: 
                        router.vector.insert(int(id), (inf, ''))
        
        for id in old_network.router_ids:
            # Old router removed
            if id not in new_network.router_ids:

                # Update other routers in the network
                for router in routers.values():
                    router.vector.pop(int(id))
                    for i in range(len(router.vector)):
                        cost, next_hop = router.vector[i]
                        if next_hop == id:
                            router.vector[i] = (inf, '')
                            
                del routers[id]

    return updated, new_network

if __name__ == "__main__":
    network, routers = main()
    print("Network and routers initialized in main.py")
