# overlapping_graphs

This is the code that contructs two subgraphs G1 and G2 from input graph G given overlapping proportion p.

1. graph construction
  - small_world graph
  <pre>
  <code>
  python graph_construction.py --g small_world --n 100 --p 0.5 --k 4 --t 20
  </code>
  </pre>
  
  - erdos_renyi graph
  <pre>
  <code>
  python graph_construction.py --g erdos_renyi --n 100 --p 0.3 
  </code>
  </pre>
  
2. extract overlapping graphs (G1 and G2)
  - version_1 
    - p == overlapping proportion over input G
  <pre>
  <code>
  python overlapping_graph_construction_v1.py --p 0.1 --g small_world_graph.npz
  </code>
  </pre>
  
