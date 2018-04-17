import matplotlib.pyplot as plt

import networkx as nx

import community
class community_detection:
    def __init__(self, true_pairs, weights):
        self.true_pairs = true_pairs
        self.G = nx.Graph()
        for i in range(len(true_pairs)):
            self.G.add_edge(true_pairs[i][0], true_pairs[i][1], weight=weights[i])
    def detect_community(self):
        partition = community.best_partition(self.G)
        print("Got partition")
        size = float(len(set(partition.values())))
        print("size=", size)
        count = 0
        pos = nx.spectral_layout(self.G)
        for com in set(partition.values()) :
            count = count + 1.
            list_nodes = [nodes for nodes in partition.keys()
                                        if partition[nodes] == com]
            nx.draw_networkx_nodes(self.G, pos, list_nodes, node_size = 20,
                                        cmap='Spectral')

        nx.draw_networkx_edges(self.G, pos, alpha=0.5)
        plt.show()
