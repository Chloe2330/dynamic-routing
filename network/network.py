import json

class NetworkGraph:
    def __init__(self):
        self.routers = set()
        self.links = {}

    def add_router(self, value):
        self.routers.add(value)
        self.links[value] = []

    def add_link(self, from_router, to_router, cost):
        self.links[from_router].append((to_router, cost))
        self.links[to_router].append((from_router, cost))

    def __str__(self):
        return str(self.links) # network graph adj list

    def update_from_config(self, json_file):
        with open(json_file, 'r') as file: 
            data = json.load(file)
        
        # Add routers 
        for router in data.get("routers", []):
            self.add_router(router)
        
        # Add links
        for link in data.get("links", []):
            self.add_link(link["from"], link["to"], link["cost"])
