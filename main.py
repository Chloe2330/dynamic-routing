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

            # Add new router
            if id not in routers.keys():
                add_router(routers, id, num_routers, new_network)

            neighbors = new_network.links[id]

            # Update neighbors in the network
            for neighbor_id, _ in neighbors.items():

                # Add new router 
                if neighbor_id not in routers:
                    add_router(routers, neighbor_id, num_routers, new_network)
                routers[neighbor_id].neighbors = new_network.links[neighbor_id]
            
            # Compare (pre-existing) links between old and new network
            if id in old_network.links and id in new_network.links: 
                compare_links(routers, old_network, new_network, id)
                
        for id in old_network.router_ids:
            # Remove old router
            if id not in new_network.router_ids:
                remove_router(routers, id)
     
    return updated, new_network

def add_router(routers, id, num_routers, new_network):
    neighbors = new_network.links[id]
    neighbors_set = set()

    # Update neighbors in the network
    for neighbor_id, cost in neighbors.items():
        neighbors_set.add(neighbor_id)
        routers[neighbor_id].vector.insert(int(id), (cost, id)) 

    # Update non-neighbor in the network
    for router in routers.values():
        if router.id not in neighbors_set: 
            router.vector.insert(int(id), (inf, ''))

    router = Router(id, num_routers, neighbors)
    router.initialize_distance_vector()
    routers[id] = router

def remove_router(routers, id):
    del routers[id]

    # Update other routers in the network
    for router in routers.values():
        router.vector.pop(int(id))
        for i in range(len(router.vector)):
            _, next_hop = router.vector[i]
            # Link is down 
            if next_hop == id:
                router.vector[i] = (inf, '')

def compare_links(routers, old_network, new_network, id):
    neighbors = new_network.links[id]
    old_neighbors = old_network.links[id]

    for neighbor_id, cost in neighbors.items():
        if neighbor_id in old_neighbors:
            # Edge case where link cost increases (Bellman Ford won't autocorrect)
            if cost > old_neighbors[neighbor_id]:
                for i in range(len(routers[id].vector)):
                    _, next_hop = routers[id].vector[i]
                    if next_hop == neighbor_id:
                        # Manually update distance vector with new cost
                        routers[id].vector[i] = (cost, neighbor_id)

if __name__ == "__main__":
    network, routers = main()
    print("Network and routers initialized in main.py")
