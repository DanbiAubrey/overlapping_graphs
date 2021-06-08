import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import scipy as sp
import argparse

class Graph:
    def __init__(self, p, g):
        self.G = nx.from_numpy_matrix(sp.sparse.load_npz('graphs/'+ g).todense())
        self.n_num = len(self.G)
        self.e_num = self.G.number_of_edges()
        self.nodes = self.G.nodes()
        self.edges = self.G.edges()
        self.ovl_p = p
        self.ovl_num, self.non_ovl_num = self.define_node_num()
        self.sub_g_num = self.ovl_num + self.non_ovl_num
        self.ovl_g = self.generate_ovl_graph()
        self.G1 = self.generate_subgraph(args.t)
        self.G2 = self.generate_subgraph(args.t)
    
    ## calculate the number of overlapping and non-overlapping nodes
    def define_node_num(self):
        non_ovl_p = 1 - self.ovl_p

        ovl_num = int(self.n_num * self.ovl_p)
        non_ovl_num = int((self.n_num - ovl_num)/2)
   
        return ovl_num, non_ovl_num
    
    def generate_ovl_graph(self):
    
        G = self.G
        ovl_g = nx.Graph()
        curr = np.random.choice(self.nodes)
        visited_nodes = [curr]
        ovl_g.add_node(curr)

        while len(ovl_g) < self.ovl_num:
            neighborhood = list(G.neighbors(curr))
            if len(neighborhood) != 0:#if neighbors exist
                for j in neighborhood:
                    if j not in ovl_g.nodes() and (curr,j) not in ovl_g.edges():
                        visited_nodes.append(j)
                        ovl_g.add_edge(curr,j)
                        break
                    elif (curr,j) not in ovl_g.edges() and j in ovl_g.nodes():
                        ovl_g.add_edge(curr,j)
                        break
                    else:
                        continue         
                        
                if curr == visited_nodes[-1]:#if nothing added to node list
                    curr = visited_nodes[visited_nodes.index(curr) - 1]
                else:
                    curr = visited_nodes[-1]
                    
        ''' graph_visualization''' 
        node_color_map = []
        for node in G:
            if node in ovl_g:
                node_color_map.append('red')
            else:
                node_color_map.append('black')
                
        plt.figure(figsize=(12,12))
        pos = nx.circular_layout(G)
        nx.draw_networkx(G, pos, node_color = node_color_map)
        plt.savefig('figures/ovl_G')

        return ovl_g
    
    def generate_sub_graphs(self):
         #tries t
        for i in range(0,t):
            G = self.G
            sub_g = nx.Graph()
            curr = np.random.choice(self.nodes)
            visited_nodes = [curr]
            sub_g.add_node(curr)

            while len(sub_g) < self.sub_g_num:
                neighborhood = list(G.neighbors(curr))
                if len(neighborhood) != 0:#if neighbors exist
                    for j in neighborhood:
                        if j not in sub_g.nodes() and (curr,j) not in sub_g.edges():
                            visited_nodes.append(j)
                            sub_g.add_edge(curr,j)
                            break
                        elif (curr,j) not in sub_g.edges() and j in sub_g.nodes():
                            sub_g.add_edge(curr,j)
                            break
                        else:
                            continue         

                    if curr == visited_nodes[-1]:#if nothing added to node list
                        curr = visited_nodes[visited_nodes.index(curr) - 1]
                    else:
                        curr = visited_nodes[-1]

        return sub_g
        
    
    
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', required=True, default=1, type=float, help="overlapping proportion")
    parser.add_argument('--g', required=True, default='small_world_graph.npz', type=str, help="input graph")
    parser.add_argument('--t', requried=True, default=20, type=int, help="number of attempts to generate subgraphs")
    args = parser.parse_args()
    
    G = Graph(args.p, args.g)
    


if __name__ == "__main__":  
    main()
       

