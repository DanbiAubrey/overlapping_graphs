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
        self.expected_ovl_num, self.expected_non_ovl_num = self.define_node_num()
        self.expected_sub_g_num = self.expected_ovl_num + self.expected_non_ovl_num
        self.G1 = self.generate_subgraph()
        self.G2 = self.generate_subgraph()
        self.ovl_num, self.ovl_nodes = self.ovl_num()
        self.G1_n_num = len(self.G1)
        self.G2_n_num = len(self.G2)
        self.G1_non_ovl_nodes = list(self.G1.nodes() - self.ovl_nodes)
        self.G2_non_ovl_nodes = list(self.G2.nodes() - self.ovl_nodes)
        self.remaining_nodes = list(self.nodes - self.G1.nodes() - self.G2.nodes()) + self.ovl_nodes
   
    def define_node_num(self):
        non_ovl_p = 1 - self.ovl_p

        ovl_num = int(self.n_num * self.ovl_p)
        non_ovl_num = int((self.n_num - ovl_num)/2)
   
        return ovl_num, non_ovl_num
    
    def generate_subgraph(self):
    
        G = self.G
        sub_g = nx.Graph()
        sub_g_nodes = []
        sub_g_edges = []
        start = np.random.choice(G.nodes())
        sub_g_nodes = [start]

        curr = start
        while len(sub_g_nodes) < self.expected_sub_g_num:
            sub_g_size = len(sub_g_nodes)
            neighborhood = list(G.neighbors(curr))
            if len(neighborhood) != 0:#if neighbors exist
                for j in neighborhood:
                    e = (curr, j)
                    if e not in sub_g_edges and j not in sub_g_nodes:
                            sub_g_nodes.append(j)
                            sub_g_edges.append(e)
                            break
                    elif e not in sub_g_edges and j in sub_g_nodes:
                            sub_g_edges.append(e)                            
                            break
                    else:
                        continue

                if len(sub_g_nodes) == sub_g_size:#if nothing added to node list
                    idx = sub_g_nodes.index(curr) - 1
                    curr = sub_g_nodes[idx]
                else:
                    curr = sub_g_nodes[-1]

        sub_g.add_nodes_from(sub_g_nodes)
        sub_g.add_edges_from(sub_g_edges)

        return sub_g
    
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
        
    def ovl_num(self):
        common = 0
        common_list = []
        for node in self.G1:
            if node in self.G2:
                common += 1
                common_list.append(node)
        if(not common):
            return ("No overlapping nodes exist")
        else:
            return common, common_list
        
        
    def prune_overlapping_nodes(self, curr_g):
        
        ''' alternatively adjust the number of overlapping nodes from G1 and G2'''
        rand_node = np.random.choice(self.ovl_nodes)
        curr_g.remove_node(rand_node)
        self.ovl_nodes.remove(rand_node)
        self.G1_non_ovl_nodes = list(self.G1.nodes() - self.ovl_nodes)
        self.G2_non_ovl_nodes = list(self.G2.nodes() - self.ovl_nodes)
        added = 0
        while added != 1:
            add_rand_node = np.random.choice(self.remaining_nodes)
            edge_list = list(self.edges(add_rand_node))
            for i in range(0, len(edge_list)):
                if edge_list[i][1] in list(curr_g.nodes()):
                    curr_g.add_edge(list(edge_list[i])[0], list(edge_list[i])[1])
                    added = 1
                else:
                    continue
            
        
    def adjust_overlapping_nodes(self):
        
        turn = 1#start w/ G1
        
        while self.ovl_num > self.expected_ovl_num:
            if turn == 1:
                self.prune_overlapping_nodes(self.G1)
                self.ovl_num -= 1
                turn = 2
            else:
                self.prune_overlapping_nodes(self.G2)
                self.ovl_num -= 1
                turn = 1
        
        '''remove any isolated nodes'''
        self.G1.remove_nodes_from(list(nx.isolates(self.G1)))
        self.G2.remove_nodes_from(list(nx.isolates(self.G2)))
                
        return self.G1, self.G2
            
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', required=True, default=1, type=float, help="overlapping proportion")
    parser.add_argument('--g', required=True, default='small_world_graph.npz', type=str, help="input graph")
    parser.add_argument('--t', required=True, default=30, type=int, help="number of attempts to generate subgraphs")
    args = parser.parse_args()
    
    G = Graph(args.p, args.g)
    G.subgraph_visualization('initial_subgraphs')
    for i in range(0,args.t):
        print("iter:{}".format(i))
        G1, G2 = G.adjust_overlapping_nodes()
        if nx.is_connected(G1) and nx.is_connected(G2):
            break
            
    if not(nx.is_connected(G1) and nx.is_connected(G2)):
        print("try more attempts!")
        
    G.subgraph_visualization('adjusted_subgraphs')
    print("ovl_num: {}, G1_node_num : {}, G2_node_num : {}".format(G.ovl_num, G.G1_n_num, G.G2_n_num))
    


if __name__ == "__main__":  
    main()
       

