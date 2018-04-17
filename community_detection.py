import matplotlib.pyplot as plt

import networkx as nx
from math import sqrt
import community

from constants import * 

class community_detection:
    def __init__(self, matrix):
        self.G = nx.Graph()
        self.matrix = matrix
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] += 1
        for i in range(len(self.matrix[0])):
            for j in range(i + 1, len(self.matrix[0])):
                edge_weight = self.cosine_similarity(i, j)
                if edge_weight > THRESHOLD_CLIPPED_SIMILARITY: 
                    self.G.add_edge(i, j, weight=self.cosine_similarity(i, j))
    
    def cosine_similarity(self, i, j):
        val = 0.0
        vali = 0.0
        valj = 0.0
        for x in range(len(self.matrix)):
            vali += self.matrix[x][i] * self.matrix[x][i]
            valj += self.matrix[x][j] * self.matrix[x][j]
            val += self.matrix[x][i] * self.matrix[x][j] 
        return val / sqrt(vali * valj)

    def detect_community(self):
        partition = community.best_partition(self.G)
        print("Got partition")
        print(partition.keys())
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
