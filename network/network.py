import json

class NetworkGraph:
    def __init__(self):
        self.routers = [] 
        self.links = {}

    def add_router(self, id):
        self.routers.append(id)
        self.links[id] = {}

    def add_link(self, from_router, to_router, cost):
        self.links[from_router][to_router] = cost
        self.links[to_router][from_router] = cost

    def __str__(self):
        return str(self.links)

    def update_from_config(self, json_file):
        with open(json_file, 'r') as file: 
            data = json.load(file)
        
        # Add routers 
        for router in data.get("routers", []):
            self.add_router(router)
        
        # Add links
        for link in data.get("links", []):
            self.add_link(link["from"], link["to"], link["cost"])
