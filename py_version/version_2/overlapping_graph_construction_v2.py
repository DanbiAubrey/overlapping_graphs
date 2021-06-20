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
        self.G1 = self.ovl_g.copy()
        self.G2 = self.ovl_g.copy()
        self.g1_visited_nodes = []
        self.g2_visited_nodes = []
        
        
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
                    if j not in ovl_g.nodes():
                        visited_nodes.append(j)
                        ovl_g.add_edge(curr,j)
                        break
                    elif (curr,j) not in ovl_g.edges():
                        ovl_g.add_edge(curr,j)
                        break
                    else:
                        continue         
                        
                if curr == visited_nodes[-1]:#if nothing added to node list
                    curr = visited_nodes[visited_nodes.index(curr) - 1]
                else:
                    curr = visited_nodes[-1]
                    
        plt.figure(figsize=(12,12))
        nx.draw_networkx(ovl_g)
        plt.savefig('figures/ovl_G')

        return ovl_g
    
    def extend_graph(self, curr_g, cp_g, curr, visited_nodes):
        
        neighborhood = list(self.G.neighbors(curr))
        if len(neighborhood) != 0:#if neighbors exist
            for j in neighborhood:
                if j not in curr_g.nodes() and j not in cp_g.nodes():
                    visited_nodes.append(j)
                    curr_g.add_edge(curr,j)
                    break
                elif j in curr_g.nodes() and (curr,j) not in curr_g.edges():
                    curr_g.add_edge(curr,j)
                    break
                else:
                    continue         

            if curr == visited_nodes[-1]:#if nothing added to node list
                curr = visited_nodes[visited_nodes.index(curr) - 1]
            else:
                curr = visited_nodes[-1]
                
        print("G1_nodes:{}".format(sorted(self.G1.nodes())))
        print("G2_nodes:{}".format(sorted(self.G2.nodes())))
            
        return curr
    
    def generate_sub_graphs(self, t):
        #tries t times
#          for i in range(0,t):
        G1 = self.G1
        G2 = self.G2
        ovl_nodes = self.ovl_g.nodes()
        g1_curr_node = np.random.choice(ovl_nodes)
        g2_curr_node = np.random.choice(ovl_nodes)
        self.g1_visited_nodes.append(g1_curr_node)
        self.g2_visited_nodes.append(g2_curr_node)
        turn = 1

        while len(G1) < self.sub_g_num and len(G2) < self.sub_g_num:
            if turn == 1:
                print("g1_curr_node:{}".format(g1_curr_node))
                g1_curr_node = self.extend_graph(G1, G2, g1_curr_node, self.g1_visited_nodes)
                turn = 2
            elif turn == 2:
                print("g2_curr_node:{}".format(g2_curr_node))
                g2_curr_node = self.extend_graph(G2, G1, g2_curr_node, self.g2_visited_nodes)
                turn = 1
        
#         print("G1_nodes:{}".format(sorted(G1.nodes())))
#         print("G2_nodes:{}".format(sorted(G2.nodes())))
#         print(sorted(self.g1_visited_nodes))
#         print(sorted(self.g2_visited_nodes))
        
    def subgraph_visualization(self, file_name):
        G1 = self.G1
        G2 = self.G2
        G1_G2 = nx.compose(G1,G2)
        node_color_map = []

        for node in G1_G2:
            if node in G1 and node in G2:
                node_color_map.append('red')
            elif node in G1:
                node_color_map.append('blue')
            elif node in G2:
                node_color_map.append('green')
            else:
                node_color_map.append('black')

        pos = nx.circular_layout(G1_G2)
        plt.figure(figsize=(20,10))
        nx.draw_networkx(G1_G2, pos, node_color=node_color_map)
        plt.savefig("figures/" + file_name)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', required=True, default=1, type=float, help="overlapping proportion")
    parser.add_argument('--g', required=True, default='small_world_graph.npz', type=str, help="input graph")
    parser.add_argument('--t', required=False, default=20, type=int, help="number of attempts to generate subgraphs")
    args = parser.parse_args()
    
    G = Graph(args.p, args.g)
    G.generate_sub_graphs(args.t)
    G.subgraph_visualization('subgraphs')


if __name__ == "__main__":  
    main()
       

