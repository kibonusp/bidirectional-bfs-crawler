from multiprocessing import Process, Manager
import networkx as nx
import random
import time

# Retorna a maior componente do grafo
def get_largest_component(graph):
  Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
  return graph.subgraph(Gcc[0])

N = 1000
GWS = get_largest_component(nx.watts_strogatz_graph(N, 10, 0.05))
adj_matrix = nx.adjacency_matrix(GWS).todense()

def dfs_recursive(node, visitados, adj_matrix, conn_nodes):
    visitados.add(node)
    if node in conn_nodes:
        return [node]

    for i, neighbour in enumerate(adj_matrix[node]):
        if neighbour == 1 and i not in visitados:
            result = dfs_recursive(neighbour, visitados)
            if result is not None:
                return [i] + result


def search(visitados_a, visitados_b, who, start_node, adj_matrix, stop, adj_list_a, adj_list_b):
    if who == 'a':
        visitados = visitados_a
        opposite_visitados = visitados_b
        adj_list = adj_list_a
        opposite_adj_list = adj_list_b
    else:
        visitados = visitados_b
        opposite_visitados = visitados_a
        adj_list = adj_list_b
        opposite_adj_list = adj_list_a
    
    queue = [start_node]
    while len(visitados) < 5000 and len(queue) > 0 and not stop.value:
        cur_node = queue.pop(0)
        adj_list[cur_node] = []
        print(f'''
              ===
              FROM: {who}
              ===
              Cur Node: {cur_node}
              visitados: {visitados}
              opposite_visitados: {opposite_visitados}''')
        
        for i, neighbor in enumerate(adj_matrix[cur_node]):
            adj_list[cur_node] += [i]
            queue.append(i)
            if neighbor != 0 and i not in visitados:
                visitados[i] = 0
                if i in opposite_visitados:
                    stop.value = True
        time.sleep(1)
    
    print(who, len(visitados), len(queue), stop.value, adj_list)
    
    #visitados_a = set(visitados_a)
    #visitados_b = set(visitados_b)
    #conn_nodes = visitados_a.intersection(visitados_b)
    conn_nodes = visitados_a.keys() & visitados_b.keys()
    print(conn_nodes)


if __name__ == '__main__':
    manager = Manager()
    visitados_a = manager.dict()
    visitados_b = manager.dict()
    adj_list_a = manager.dict()
    adj_list_b = manager.dict()
    stop = manager.Value('stop', False)
    
    process_b = Process(target=search, 
                        args=(visitados_a, 
                              visitados_b, 
                              'b', 
                              random.choice(list(GWS.nodes)), 
                              adj_matrix, 
                              stop,
                              adj_list_a,
                              adj_list_b))
    
    process_a = Process(target=search, 
                        args=(visitados_a, 
                              visitados_b, 
                              'a', 
                              random.choice(list(GWS.nodes)), 
                              adj_matrix, 
                              stop,
                              adj_list_a,
                              adj_list_b))
    
    
    process_b.start()
    process_a.start()
    
    process_a.join()
    process_b.join()