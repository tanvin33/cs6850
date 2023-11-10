import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout


def reproduction_pq(p, q, r, Zc, Zt, k):
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
    infected_nodes = []
    id = 1

    # while len(frontier_nodes) > 0 and G.number_of_nodes() <= Zt and num_infected < Zc:
    #     t += 1
    #     for i in range(len(active_nodes)):
    #         generate_new = np.random.randint(101) / 100
    #         if generate_new <= q:
    #             node = active_nodes[i]
    #             child = ("Node" + str(id), t)
    #             id += 1
    #             G.add_node(child)
    #             G.add_edge(node, child)
    #             active_nodes.append(child)

    #     if t >= k:  # start contact tracing
    #         queried_node = frontier_nodes.pop(0)
    #         paths = nx.shortest_path_length(G, initial_node)
    #         depth = paths[queried_node]
    #         probability = p**depth
    #         is_infected = np.random.randint(101) / 100 <= probability
    #         if is_infected:
    #             active_nodes.remove(queried_node)
    #             stable_nodes.append(queried_node)
    #             for neighbor in G.neighbors(queried_node):
    #                 frontier_nodes.append(neighbor)
    #             frontier_nodes.sort()
    #         else:
    #             uninfected_nodes.append(queried_node)
    
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
            new_frontier = []
            #print(frontier_nodes)

            for queried_node in frontier_nodes:
                #print(queried_node)
                paths = nx.shortest_path_length(G, initial_node)
                depth = paths[queried_node]
                probability = p**depth
                is_infected = np.random.randint(101) / 100 <= probability
                test_self = np.random.randint(101) / 100 <= r # probability queried_node tests itself, should it vary with time?

                # if is_infected:
                #     if test_self: # if test, contact trace by adding contacts to frontier
                #         # idk if we should add a test self option for if not infected (idt it would change anything tho)
                #         if queried_node in active_nodes:
                #             active_nodes.remove(queried_node) # remove from active nodes
                #         stable_nodes.append(queried_node)
                #         for neighbor in G.neighbors(queried_node):
                #             new_frontier.append(neighbor)
                #     else:
                #         new_frontier.append(queried_node) # hasn't tested, gets another try to test at next time step
                # elif not is_infected:
                #     uninfected_nodes.append(queried_node)


                if test_self:
                    if is_infected:
                        active_nodes.remove(queried_node)
                        stable_nodes.append(queried_node)
                        if queried_node in infected_nodes:
                            infected_nodes.remove(queried_node)
                        for neighbor in G.neighbors(queried_node):
                            new_frontier.append(neighbor)
                    
                    if not is_infected:
                        uninfected_nodes.append(queried_node)
                else:
                    if is_infected:
                        infected_nodes.append(queried_node)
                    new_frontier.append(queried_node)

            frontier_nodes = new_frontier

        num_infected = len(infected_nodes)

    return_code = -1
    if num_infected >= Zc:
        print("Infection Not Contained " + str(num_infected))
        return_code = 0
    elif G.number_of_nodes() > Zt:
        print("NOT converged")
        return_code = 1
    else:
        print("Infection Contained " + str(num_infected))
        return_code = 2

    color_map = []
    for node in G.nodes():
        if node in stable_nodes:
            color_map.append("red")
        elif node in uninfected_nodes:
            color_map.append("green")
        else:
            color_map.append("blue")

    return G, color_map, return_code

    # return return_code


if __name__ == "__main__":
    p = 0.9
    q = 1
    r = 1
    Zt = 1000
    Zc = 10
    k = 4  # time at which contact tracing begins

    G, color_map, return_code = reproduction_pq(p, q, r, Zc, Zt, k)
    print(return_code)
    # pos = graphviz_layout(G, prog="dot")
    # nx.draw(G, pos, with_labels=False, node_color=color_map)
    # plt.show()

    result = np.zeros((101, 101))

    # # ascending time
    # for p in range(0, 101):
    #     for q in range(0, 101):
    #         num_contained = 0
    #         for i in range(100):
    #             return_code = reproduction_pq(p / 100.0, q / 100.0, Zc, Zt, k)
    #             if return_code == 2:
    #                 num_contained += 1
    #         result[p, q] = num_contained / 100.0

    # fig, ax = plt.subplots()
    # # im, cbar = heatmap(result, ax=ax, cmap="YlGn", cbarlabel="result")
    # ax.set(xlim=(0, 100), ylim=(0, 100))

    # im = ax.imshow(result, cmap="YlGn", interpolation="nearest")
    # cbar = ax.figure.colorbar(im, ax=ax)
    # plt.show()

    # fig.tight_layout()
    # plt.show()
