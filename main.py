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

    for id in new_network.router_ids:
        neighbors = new_network.links[id]

        # New router added 
        if id not in routers.keys():
            router = Router(id, num_routers, neighbors)
            router.initialize_distance_vector()
            routers[id] = router
            
            # Update neighbors in the network
            for neighbor_id, cost in neighbors.items():
                routers[neighbor_id].neighbors = new_network.links[neighbor_id]
                routers[neighbor_id].vector.insert(int(id), (cost, id))

            # Update non-neighbor in the network
            for router in routers.values():
                if len(router.vector) != num_routers:
                    router.vector.insert(int(id), (inf, ''))

    if old_network != new_network:
        updated = True

    return updated, new_network

if __name__ == "__main__":
    network, routers = main()
    print("Network and routers initialized in main.py")
