import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout


def novel_model(
    p,
    q,
    r,
    Zc,
    Zt,
    k,
):
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
            # first generate children
            generate_new = np.random.randint(101) / 100
            if generate_new <= q:
                node = active_nodes[i]
                child = ("Node" + str(id), t)
                id += 1
                G.add_node(child)
                G.add_edge(node, child)
                active_nodes.append(child)

        if t >= k:  # start contact tracing
            # print(frontier_nodes)
            paths = nx.shortest_path_length(G, initial_node)
            for node in frontier_nodes:
                does_test = np.random.randint(101) / 100 <= r
                if does_test:
                    depth = paths[node]
                    probability = p**depth
                    is_infected = np.random.randint(101) / 100 <= probability
                    if is_infected:
                        active_nodes.remove(node)
                        frontier_nodes.remove(node)
                        stable_nodes.append(node)
                        for neighbor in G.neighbors(node):
                            frontier_nodes.append(neighbor)
                        # frontier_nodes.sort(key=lambda x: x[1])
                    else:
                        frontier_nodes.remove(node)
                        uninfected_nodes.append(node)

        num_infected = len(stable_nodes)

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

    return (
        G,
        color_map,
    )


#    return G, color_map, returncode


if __name__ == "__main__":
    p = 0.7
    q = 1
    r = 0.67
    Zt = 1000
    Zc = 10
    k = 2  # time at which contact tracing begins

    G, color_map = novel_model(p, q, r, Zc, Zt, k)
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=False, node_color=color_map)
    plt.show()

    # result = np.zeros((101, 101))

    # # ascending time
    # for p in range(0, 101):
    #     for q in range(0, 101):
    #         num_contained = 0
    #         for i in range(100):
    #             return_code = reproduction_pq(p / 100.0, q / 100.0, Zc, Zt, k, 0)
    #             if return_code == 2:
    #                 num_contained += 1
    #         result[p, q] = num_contained / 100.0

    # fig, ax = plt.subplots()
    # # im, cbar = heatmap(result, ax=ax, cmap="YlGn", cbarlabel="result")
    # ax.set(xlim=(0, 100), ylim=(0, 100))
    # ax.set_xticklabels([x / 100 for x in range(0, 101, 20)])
    # ax.set_yticklabels([y / 100 for y in range(0, 101, 20)])
    # im = ax.imshow(result, cmap="YlOrRd", interpolation="nearest")
    # cbar = ax.figure.colorbar(im, ax=ax)
    # plt.savefig("ascending_time.png")

    # # DESCENDING TIME
    # result2 = np.zeros((101, 101))
    # for p in range(0, 101):
    #     for q in range(0, 101):
    #         num_contained = 0
    #         for i in range(100):
    #             return_code = reproduction_pq(p / 100.0, q / 100.0, Zc, Zt, k, -1)
    #             if return_code == 2:
    #                 num_contained += 1
    #         result2[p, q] = num_contained / 100.0

    # fig, ax = plt.subplots()
    # # im, cbar = heatmap(result, ax=ax, cmap="YlGn", cbarlabel="result")
    # ax.set(xlim=(0, 100), ylim=(0, 100))
    # ax.set_xticklabels([x / 100 for x in range(0, 101, 20)])
    # ax.set_yticklabels([y / 100 for y in range(0, 101, 20)])
    # im = ax.imshow(result2, cmap="YlOrRd", interpolation="nearest")
    # cbar = ax.figure.colorbar(im, ax=ax)

    # plt.savefig("descending_time.png")

    # Difference
    # result2 = np.zeros((101, 101))
    # for p in range(0, 101):
    #     for q in range(0, 101):
    #         num_contained = 0
    #         num_contained_d = 0
    #         for i in range(100):
    #             ascending_code = novel_model(p / 100.0, q / 100.0, r, Zc, Zt, k, 0)
    #             if ascending_code == 2:
    #                 num_contained += 1
    #             descending_code = novel_model(p / 100.0, q / 100.0, r, Zc, Zt, k, -1)
    #             if descending_code == 2:
    #                 num_contained_d += 1
    #         result2[p, q] = num_contained / 100.0 - num_contained_d / 100.0

    # fig, ax = plt.subplots()
    # # im, cbar = heatmap(result, ax=ax, cmap="YlGn", cbarlabel="result")
    # ax.set(xlim=(0, 100), ylim=(0, 100))
    # ax.set_xticklabels([x / 100 for x in range(0, 101, 20)])
    # ax.set_yticklabels([y / 100 for y in range(0, 101, 20)])
    # im = ax.imshow(result2, cmap="YlOrRd", interpolation="nearest")
    # cbar = ax.figure.colorbar(im, ax=ax)

    # plt.savefig("difference_asc_desc.png")

    # fig.tight_layout()
    # plt.show()
