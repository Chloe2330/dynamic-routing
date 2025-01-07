# Asynchronous Dynamic Routing Simulations

Uses `asyncio` to simulate all routers concurrently exchanging messages and executing algorithms in:
1. **Distance Vector Routing**: Routers with decentralized information about their neighbors update their vectors using the Bellman-Ford algorithm to find optimal routing paths.
2. **Link State Routing**: Routers with a global network view use Dijkstra's algorithm to create a shortest path tree for optimal routing paths.

## Dependencies
- Python 3.x, git

1. Clone the repository:
```sh
git clone https://github.com/Chloe2330/dynamic-routing.git
```
2. Set the `PYTHONPATH`
```sh
cd dynamic-routing
export PYTHONPATH="$(pwd):$PYTHONPATH"
```

## Distance-vector routing (Bellman-Ford)
3. Run DVR Simulation
```sh
python -u "distance_vector/dvr.py"
```

## Link-state routing (Dijkstra)
3. Run LSR Simulation 
```sh
python -u "link_state/lsr.py"
```
### Notes 
- **Scope**: Only supports simple, undirected network graph topologies.
- **Live Update**: 
    - Disable auto-save in VS Code to avoid premature JSON processing
    - Manually save `config.json` after finalizing changes 
- **Restrictions**: Invalid or complex graphs (e.g., non-existent nodes, multiple edges between nodes) will cause errors or invalid results
