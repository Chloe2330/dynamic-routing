import json

class NetworkGraph:
    def __init__(self):
        self.router_ids = set() 
        self.links = {}

    def add_router(self, id):
        self.router_ids.add(id)
        self.links[id] = {}

    def add_link(self, from_router, to_router, cost):
        self.links[from_router][to_router] = cost
        self.links[to_router][from_router] = cost

    def __str__(self):
        return str(self.links)

    def update_from_config(self, json_file):
        with open(json_file, 'r') as file: 
            data = json.load(file)
        
        # Add router_ids 
        for router in data.get("routers", []):
            self.add_router(router)
        
        # Add links
        for link in data.get("links", []):
            self.add_link(link["from"], link["to"], link["cost"])
    
    def __eq__(self, other):
        if isinstance(other, NetworkGraph):
            return self.router_ids == other.router_ids and self.links == other.links
        return False 
