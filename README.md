# Dynamic Routing Simulations

## Distance-vector routing (Bellman-Ford)
1. Clone the repository:
```sh
git clone https://github.com/Chloe2330/dynamic-routing.git
```
2. Set the `PYTHONPATH`
```sh
cd dynamic-routing
export PYTHONPATH="$(pwd):$PYTHONPATH"
```
3. Run DVR Simulation
```sh
python -u "distance-vector/dvr.py"
```
### In Progress
#### Highest priorities 
- Change distance vector type from array of 2-tuples to dict with char/string key (dest router ID) and a 2-tuple value (cost, next hop)
- Graceful exit with Ctrl + C
#### Lower priorities
- Write a test suite (scripts to automate creation/update of config files)
- Use `watchdog` for smoother file monitoring and event handling

### Notes 
- **Scope**: Only supports simple, undirected network graph topologies.
- **Live Update**: 
    - Disable auto-save in VS Code to avoid premature JSON processing
    - Manually save `config.json` after finalizing changes 
- **Restrictions**: Invalid or complex graphs (e.g., non-existent nodes, multiple edges between nodes) will cause errors or invalid results

## Link-state routing (Dijkstra)