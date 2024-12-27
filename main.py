from network.network import NetworkGraph
from network.router import Router

def main():
    network = NetworkGraph()
    network.update_from_config('config.json')

    num_routers = len(network.routers)
    routers = []

    for name in network.routers:
        router = Router(name, num_routers)
        routers.append(router)
    
    return network, routers

if __name__ == "__main__":
    network, routers = main()
    print("Network and routers initialized in main.py")
    