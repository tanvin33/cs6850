import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout


def reproduction_pq(p, q, Zc, Zt, k):
    assert 0 <= p <= 1
    assert 0 <= q <= 1
    G = nx.DiGraph()
    num_infected = 0
    t = 0
    initial_node = ("Root", t)
    G.add_node(initial_node)
    active_nodes = []
    active_nodes.append(initial_node)
    frontier_nodes = []
    frontier_nodes.append(initial_node)
    stable_nodes = []
    uninfected_nodes = []
    id = 1
    while len(frontier_nodes) > 0 and G.number_of_nodes() <= Zt and num_infected < Zc:
        t += 1
        for i in range(len(active_nodes)):
            generate_new = np.random.randint(101) / 100
            if generate_new <= q:
                node = active_nodes[i]
                child = ("Node" + str(id), t)
                id += 1
                G.add_node(child)
                G.add_edge(node, child)
                active_nodes.append(child)

        if t >= k:  # start contact tracing
            print(frontier_nodes)
            queried_node = frontier_nodes.pop(0)
            paths = nx.shortest_path_length(G, initial_node)
            depth = paths[queried_node]
            probability = p**depth
            is_infected = np.random.randint(101) / 100 <= probability
            if is_infected:
                active_nodes.remove(queried_node)
                stable_nodes.append(queried_node)
                for neighbor in G.neighbors(queried_node):
                    frontier_nodes.append(neighbor)
                frontier_nodes.sort()
            else:
                uninfected_nodes.append(queried_node)

        num_infected = len(stable_nodes)

    if num_infected >= Zc:
        print("Infection Not Contained " + str(num_infected))
    elif G.number_of_nodes() > Zt:
        print("NOT converged")
    else:
        print("Infection Contained " + str(num_infected))

    color_map = []
    for node in G.nodes():
        if node in stable_nodes:
            color_map.append("red")
        elif node in uninfected_nodes:
            color_map.append("green")
        else:
            color_map.append("blue")

    return G, color_map


if __name__ == "__main__":
    p = 0.7
    q = 1
    Zt = 1000
    Zc = 10
    k = 2  # time at which contact tracing begins

    G, color_map = reproduction_pq(p, q, Zc, Zt, k)
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=False, node_color=color_map)
    plt.show()
