from math import inf
from network.network import NetworkGraph
from network.router import Router
from distance_vector.poison_reverse import state_manager

def main():
    network = NetworkGraph()
    network.update_from_config('config.json')
    routers = {}

    for id in network.router_ids:
        neighbors = network.links[id]
        router = Router(id, neighbors)
        router.initialize_distance_vector(network.router_ids)
        routers[id] = router
    
    return network, routers

async def update_network_continuously(network, routers, dvr):
    updated = False
    old_network = network

    new_network = NetworkGraph()
    new_network.update_from_config('config.json')

    # Change in network config 
    if old_network != new_network:
        updated = True 

        for id in new_network.router_ids:

            # Add new router
            if id not in routers.keys():
                add_router(routers, id, new_network)

            neighbors = new_network.links[id]

            # Update neighbors in the network
            for neighbor_id, _ in neighbors.items():

                # Add new router 
                if neighbor_id not in routers:
                    add_router(routers, neighbor_id, new_network)
                routers[neighbor_id].neighbors = new_network.links[neighbor_id]
            
            # Compare (pre-existing) links between old and new networks
            if id in old_network.links and id in new_network.links:
                compare_links(routers, old_network, new_network, id, dvr)
                
        for id in old_network.router_ids:
            # Remove old router
            if id not in new_network.router_ids:
                remove_router(routers, id)
     
    return updated, new_network

def add_router(routers, id, new_network):
    neighbors = new_network.links[id]
    neighbors_set = set()

    # Update neighbors in the network
    for neighbor_id, cost in neighbors.items():
        neighbors_set.add(neighbor_id)
        routers[neighbor_id].vector[id] = (cost, id) 

    # Update non-neighbor in the network
    for router in routers.values():
        if router.id not in neighbors_set: 
            router.vector[id] = (inf, '')

    router = Router(id, neighbors)
    router.initialize_distance_vector(new_network.router_ids)
    routers[id] = router

def remove_router(routers, id):
    del routers[id]

    # Update other routers in the network
    for router in routers.values():
        del router.vector[id]
        for dest_id, (_, next_hop) in router.vector.items():
            # Link is down
            if next_hop == id:
                router.vector[dest_id] = (inf, '')

def reset_routers(routers, new_network):
    for router in routers.values():
        router.initialize_distance_vector(new_network.router_ids)

def compare_links(routers, old_network, new_network, id, dvr):
    neighbors = new_network.links[id]
    old_neighbors = old_network.links[id]

    for neighbor_id, cost in neighbors.items():
        if neighbor_id in old_neighbors:
            # Link cost increases!
            if cost > old_neighbors[neighbor_id]:
                # Poison reverse 
                if dvr:
                    poison_reverse(routers, id, neighbor_id)
                # Link-state recalculation 
                else:
                    reset_routers(routers, new_network)

def poison_reverse(routers, id, neighbor_id):
    for key in routers:
        if key == id:
            for dest_id, (_, next_hop) in routers[id].vector.items():
                if next_hop == neighbor_id:
                    routers[id].vector[dest_id] = (inf, "")
        elif key == neighbor_id:
            for dest_id, (_, next_hop) in routers[neighbor_id].vector.items():
                if next_hop == id:
                    routers[neighbor_id].vector[dest_id] = (inf, "")
    state_manager.set_poison_reverse(True)

if __name__ == "__main__":
    network, routers = main()
    print("Network and routers initialized in main.py")
