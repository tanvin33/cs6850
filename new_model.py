import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout


def self_testing_model(Zc, Zt, k):
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
    root = 0
    p = np.random.randint(101) / 100
    q = np.random.randint(101) / 100
    r = np.random.randint(101) / 100
    # G.add_node(root, p=p, q=q, r=r, num_tests=0)
    G.add_node(root, p=p, q=q, r=r, time_since_last=0)
    active_nodes.append(0)
    frontier_nodes.append(0)
    root_infected = np.random.randint(101) / 100 <= G.nodes[root]["p"]
    if root_infected:
        active_infected_nodes.append(0)
        # max_infected = 1

    # contagion process
    while len(frontier_nodes) > 0 and G.number_of_nodes() <= Zt and num_infected < Zc:
        t += 1

        # in each round, any active nodes will generate new contacts, or "children" with probability q
        for i in range(len(active_nodes)):
            generate_new = np.random.randint(101) / 100
            if generate_new <= G.nodes[i]["q"]:
                parent = active_nodes[i]
                child = id
                id += 1
                p = np.random.randint(101) / 100
                q = np.random.randint(101) / 100
                r = np.random.randint(101) / 100
                # G.add_node(child, p=p, q=q, r=r, num_tests=0)
                G.add_node(child, p=p, q=q, r=r, time_since_last=0)
                G.add_edge(parent, child)
                active_nodes.append(child)

                # determine if each node created will be infected in advance.
                # this is not how we think of the contagion process working, but
                # it allows us to easily code using principle of deferred decisions
                is_infected = np.random.randint(101) / 100 <= G.nodes[child]["p"]
                # a node is only infected if its parent is infected
                if parent in active_infected_nodes and is_infected:
                    active_infected_nodes.append(child)
                    # max_infected += 1

        # if we are past time k, do one step of the contact tracing process
        if t >= k:
            for node in frontier_nodes:
                if G.nodes[node]['time_since_last'] <= 3:
                    does_test = False
                    G.nodes[node]['time_since_last'] += 1
                does_test = np.random.randint(101) / 100 <= G.nodes[node]["r"]
                # nothing happens if the node does not choose to test itself
                if does_test:
                    # G.nodes[node]['num_tests] += 1
                    G.nodes[node]['time_since_last'] = 0
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
                        # marked as uninfected,
                        # and no longer active (technically still generates new contacts, but we are not interested in them)
                        frontier_nodes.remove(node)
                        uninfected_nodes.append(node)
                        active_nodes.remove(node)
                # if G.nodes[node]['num_tests'] == 5:
                #     frontier_nodes.remove(node)
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

    # return (G, color_map, max_infected)
    return (G, color_map, return_code)


def self_testing_model_constant(
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

    # keep track of max number of infected nodes
    # max_infected = 0

    # initialize root, and determine its infection status
    root = ("Root", t)
    G.add_node(root)
    active_nodes.append(root)
    frontier_nodes.append(root)
    root_infected = np.random.randint(101) / 100 <= p
    if root_infected:
        active_infected_nodes.append(root)
        # max_infected = 1

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
                # it allows us to easily code using principle of deferred decisions
                paths = nx.shortest_path_length(G, root)
                depth = paths[parent]
                probability = p**depth
                is_infected = np.random.randint(101) / 100 <= probability
                # a node is only infected if its parent is infected
                if parent in active_infected_nodes and is_infected:
                    active_infected_nodes.append(child)
                    # max_infected += 1

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
                        # marked as uninfected,
                        # and no longer active (technically still generates new contacts, but we are not interested in them)
                        frontier_nodes.remove(node)
                        uninfected_nodes.append(node)
                        active_nodes.remove(node)
                        active_nodes.remove(node)

        # after a round, calculate num_infected, to check contagion stopping condition
        num_infected = len(active_infected_nodes)

    # print the contagion result
    return_code = -1
    if len(frontier_nodes) == 0:
        # print("Infection Contained " + str(num_infected))
        return_code = 2
    elif num_infected >= Zc:
        # print("Infection Not Contained " + str(num_infected))
        return_code = 0
    elif G.number_of_nodes() > Zt:
        # print("NOT converged")
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

    # return (G, color_map, max_infected)
    return (G, color_map, return_code)


if __name__ == "__main__":
    p = np.random.randint(101) / 100.0
    q = 1
    r = 0.8
    Zt = 1500
    Zc = 30
    k = 2  # time at which contact tracing begins

    G, color_map, return_code = self_testing_model(Zc, Zt, k)
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=False, node_color=color_map)
    plt.show()

    # creating observed probability of containment graph
    # result = np.zeros((101, 101))

    # for p1 in range(0, 101):
    #     for r1 in range(0, 101):
    #         num_contained = 0
    #         for i in range(10):
    #             G, color_map, return_code = self_testing_model_constant(p1 / 100.0, q, r1 / 100.0, Zc, Zt, k)
    #             if return_code == 2:
    #                 num_contained += 1
    #         result[p1, r1] = num_contained / 100.0

    # fig, ax = plt.subplots()
    # ax.set(xlim=(0, 100), ylim=(0, 100))
    # im = ax.imshow(result, cmap="YlGn", interpolation="nearest")
    # cbar = ax.figure.colorbar(im, ax=ax)
    # plt.show()

    # sum_max_infected = 0
    # for i in range(0, 1001):
    #     G, color_map, max_infected = self_testing_model(p, q, r, Zc, Zt, k)
    #     sum_max_infected += max_infected
    # print(sum_max_infected / 1000.0)
