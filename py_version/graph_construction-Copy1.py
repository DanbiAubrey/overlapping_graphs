import matplotlib.pyplot as plt
import networkx as nx
import scipy as sp
import argparse

def construct_small_world(args):
        G = nx.connected_watts_strogatz_graph(n = args.n, k = args.k, p = args.p, tries = args.t)
        pos = nx.circular_layout(G)
        
        plt.figure(figsize = (12, 12))
        nx.draw_networkx(G, pos)
        plt.savefig('figures/G.png')
        
        ''' save the G'''
        A = nx.adjacency_matrix(G)
        sp.sparse.save_npz('graphs/small_world_graph.npz', A)
        
def construct_erdos_renyi(args):
        G = nx.erdos_renyi_graph(n = args.n, p = args.p)
        
        plt.figure(figsize = (12, 12))
        nx.draw_networkx(G)
        plt.savefig('figures/G.png')
        
        ''' save the G'''
        A = nx.adjacency_matrix(G)
        sp.sparse.save_npz('graphs/erdos_renyi_graph.npz', A)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--g', required=False, default='small_world', type=str, help="graph_type")
    parser.add_argument('--n', required=False, default=100, type=int, help="number of nodes")
    parser.add_argument('--p', required=False, default=0.5, type=float, help="overlapping proportion")
    parser.add_argument('--k', required=False, default=4, type=int, help="k nearest neighbors")
    parser.add_argument('--t', required=False, default=20, type=int, help="tries")
    args = parser.parse_args()
    
    if args.g == 'small_world':
        construct_small_world(args)
    elif args.g == 'erdos_renyi':
        construct_erdos_renyi(args)
    else:
        print("unavailable graph type has been entered!")
        
    
if __name__ == "__main__":
    main()
    