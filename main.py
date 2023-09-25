from multiprocessing import Process, Manager
import networkx as nx
import time

# Retorna a maior componente do grafo
def get_largest_component(graph):
  Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
  return graph.subgraph(Gcc[0])

N = 10000
GWS = get_largest_component(nx.watts_strogatz_graph(N, 10, 0.05))
'''
adj_matrix = [
    [0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0]
]
'''

# visitados específico da dfs
def dfs_recursive(node, visitados, adj_list, conn_node):
    visitados.add(node)
    if node == conn_node:
        return [node]
    
    if node not in adj_list:
        return None
    
    for neighbor in adj_list[node]:
        if neighbor not in visitados:
            result = dfs_recursive(neighbor, visitados, adj_list, conn_node)
            if result is not None:
                return [node] + result
            
    return None


def search(visitados_a, visitados_b, who, start_node, adj_matrix, stop, adj_list_a, adj_list_b, route_a, route_b):
    if who == 'a':
        visitados = visitados_a
        opposite_visitados = visitados_b
        adj_list = adj_list_a
        route = route_a
    else:
        visitados = visitados_b
        opposite_visitados = visitados_a
        adj_list = adj_list_b
        route = route_b
        
    visitados[start_node] = 0
    
    queue = [start_node]
    while len(visitados) < 5000 and len(queue) > 0 and not stop.value:
        cur_node = queue.pop(0)
        adj_list[cur_node] = []
        
        for i, neighbor in enumerate(adj_matrix[cur_node]):
            if neighbor == 1:
                adj_list[cur_node] += [i]
                queue.append(i)
            if neighbor != 0 and i not in visitados:
                visitados[i] = 0
                if i in opposite_visitados:
                    stop.value = True
        # time.sleep(1)
    print(who, adj_list)
    
    commons = sorted(list({x:visitados[x] for x in visitados.keys() if x in opposite_visitados}.keys()))
    path_to_conn = dfs_recursive(start_node, set(), adj_list, commons[0])
    
    route += path_to_conn


if __name__ == '__main__':
    start = time.time()
    
    manager = Manager()
    visitados_a = manager.dict()
    visitados_b = manager.dict()
    adj_list_a = manager.dict()
    adj_list_b = manager.dict()
    route_a = manager.list()
    route_b = manager.list()
    
    # usado para parar a bfs em ambos os processos
    # quando o nó estiver no visitados do processo oposto
    stop = manager.Value('stop', False)
    
    process_a = Process(target=search, 
                        args=(visitados_a, 
                              visitados_b, 
                              'a', 
                              list(GWS.nodes)[0], 
                              nx.adjacency_matrix(GWS).todense(), 
                              stop,
                              adj_list_a,
                              adj_list_b,
                              route_a,
                              route_b))
    
    process_b = Process(target=search, 
                        args=(visitados_a, 
                              visitados_b, 
                              'b', 
                              list(GWS.nodes)[3720], 
                              nx.adjacency_matrix(GWS).todense(), 
                              stop,
                              adj_list_a,
                              adj_list_b,
                              route_a,
                              route_b))
    
    process_a.start()
    process_b.start()
    
    process_a.join()
    process_b.join()
    
    route_a_list = list(route_a)
    route_b_list = list(route_b)
    route_b_list.reverse()
    
    route = route_a_list + route_b_list[1:]
    
    end = time.time()
    print("Route:", route)
    print("Time elapsed: {:.2f}s".format(end-start))