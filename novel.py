import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout


def self_testing_model(
    p,
    q,
    r,
    Zc,
    Zt,
    k,
):
    # assert pre-conditions
    assert 0 <= p <= 1
    assert 0 <= q <= 1
    assert 0 <= r <= 1

    # initialize graph
    G = nx.DiGraph()

    # initialize key variables
    num_infected = 0
    t = 0  # time / infection round
    id = 1  # nodeID counter

    # initialize key lists
    active_nodes = []  # list of nodes still generating new contacts
    frontier_nodes = []  # list of nodes who know they are possibly infected
    stable_nodes = []  # nodes that were infected, tested positive, "quarantined"
    uninfected_nodes = []  # nodes that tested negative, any children are not relevant
    active_infected_nodes = []  # nodes still generating contacts, but are infected

    # initialize root, and determine its infection status
    root = ("Root", t)
    G.add_node(root)
    active_nodes.append(root)
    frontier_nodes.append(root)
    root_infected = np.random.randint(101) / 100 <= p
    if root_infected:
        active_infected_nodes.append(root)

    # contagion process
    while len(frontier_nodes) > 0 and G.number_of_nodes() <= Zt and num_infected < Zc:
        t += 1

        # in each round, any active nodes will generate new contacts, or "children" with probability q
        for i in range(len(active_nodes)):
            generate_new = np.random.randint(101) / 100
            if generate_new <= q:
                parent = active_nodes[i]
                child = ("Node" + str(id), t)
                id += 1
                G.add_node(child)
                G.add_edge(parent, child)
                active_nodes.append(child)

                # determine if each node created will be infected in advance.
                # this is not how we think of the contagion process working, but
                # it allows us to easily code using principle of deffered decisions
                paths = nx.shortest_path_length(G, root)
                depth = paths[parent]
                probability = p**depth
                is_infected = np.random.randint(101) / 100 <= probability
                # a node is only infected if its parent is infected
                if parent in active_infected_nodes and is_infected:
                    active_infected_nodes.append(child)

        # if we are past time k, do one step of the contact tracing process
        if t >= k:
            for node in frontier_nodes:
                does_test = np.random.randint(101) / 100 <= r
                # nothing happens if the node does not choose to test itself
                if does_test:
                    if node in active_infected_nodes:  # if infected (pre-determined)
                        # first, the node is stabilized
                        active_nodes.remove(node)
                        active_infected_nodes.remove(node)
                        stable_nodes.append(node)

                        # it is removed from the frontier
                        frontier_nodes.remove(node)

                        # and all of its children get added to the frontier
                        for neighbor in G.neighbors(node):
                            frontier_nodes.append(neighbor)

                    else:  # if not infected
                        # otherwise, it is removed from the frontier,
                        # marked as unifected,
                        # and no longer active (technically still generates new contacts, but we are not interested in taht)
                        frontier_nodes.remove(node)
                        uninfected_nodes.append(node)
                        active_infected_nodes.remove(node)

        # after a round, calculate num_infected, to check contagion stopping condition
        num_infected = len(active_infected_nodes)

    # print the contagion result
    return_code = -1
    if len(frontier_nodes) == 0:
        print("Infection Contained " + str(num_infected))
        return_code = 2
    elif num_infected >= Zc:
        print("Infection Not Contained " + str(num_infected))
        return_code = 0
    elif G.number_of_nodes() > Zt:
        print("NOT converged")
        return_code = 1

    # create color map for plotting this graph
    color_map = []
    for node in G.nodes():
        if node in stable_nodes:
            color_map.append("orange")
        elif node in uninfected_nodes:
            color_map.append("green")
        elif node in active_infected_nodes:
            color_map.append("red")
        else:
            color_map.append("blue")

    return (G, color_map)


if __name__ == "__main__":
    p = 0.9
    q = 1
    r = 0.8
    Zt = 1000
    Zc = 10
    k = 2  # time at which contact tracing begins

    G, color_map = self_testing_model(p, q, r, Zc, Zt, k)
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=False, node_color=color_map)
    plt.show()
