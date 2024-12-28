from network.network import NetworkGraph
from network.router import Router

def main():
    network = NetworkGraph()
    network.update_from_config('config.json')

    num_routers = len(network.routers)

    routers = {}
    for id in network.routers:
        router = Router(id, num_routers)
        neighbors = network.links.get(id, [])
        router.initialize_distance_vector(neighbors)
        routers[id] = router
    
    return network, routers

if __name__ == "__main__":
    network, routers = main()
    print("Network and routers initialized in main.py")
