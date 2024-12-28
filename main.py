from network.network import NetworkGraph
from network.router import Router

def main():
    network = NetworkGraph()
    network.update_from_config('config.json')

    num_routers = len(network.routers)
    routers = {}

    for id in network.routers:
        neighbors = network.links[id]
        router = Router(id, num_routers, neighbors)
        router.initialize_distance_vector()
        routers[id] = router
    
    return routers

if __name__ == "__main__":
    routers = main()
    print("Network and routers initialized in main.py")
