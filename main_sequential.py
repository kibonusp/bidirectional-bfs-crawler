import networkx as nx
import time

# Retorna a maior componente do grafo
def get_largest_component(graph):
  Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
  return graph.subgraph(Gcc[0])

def create_adjlist(origin, destination, adj_matrix):
    queue = [origin]
    visited = {origin}
    adj_list = dict()
    
    while len(queue) > 0 and destination not in visited:
        cur_node = queue.pop(0)
        adj_list[cur_node] = set()
        for i, neighbor in enumerate(adj_matrix[cur_node]):
            if neighbor == 1 and i not in visited:
                visited.add(i)
                queue.append(i)
                adj_list[cur_node].add(i)
                if i not in adj_list:
                    adj_list[i] = {cur_node}
                
    return adj_list
           
def dfs(origin, destination, adj_list):
    path = dfs_rec(origin, destination, adj_list, set())
    return path
         
def dfs_rec(cur, destination, adj_list, visited):
    if cur == destination:
        return [cur]
    
    real_path = None
    for neighbor in adj_list[cur]:
        if neighbor not in visited:
            visited.add(neighbor)
            path = dfs_rec(neighbor, destination, adj_list, visited)
            if path is not None:
                real_path = [cur] + path
                
    if real_path:
        return real_path
    
    return None

N = 10000
GWS = get_largest_component(nx.watts_strogatz_graph(N, 10, 0.05))

origin = 0
destination = 3720

start = time.time()
adj_matrix = nx.adjacency_matrix(GWS).todense()
adj_list = create_adjlist(origin, destination, adj_matrix)
path = dfs(origin, destination, adj_list)
end = time.time()
print(path)
print("Time elapsed:", end-start)