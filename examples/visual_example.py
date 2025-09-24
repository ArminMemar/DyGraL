import matplotlib.pyplot as plt
import networkx as nx
from dygral import TemporalGraph, TemporalQueries

def run_visual_example():
    # Create the temporal graph
    G = TemporalGraph(directed=True)
    edges = [
        ("Alice", "Bob", 1),
        ("Bob", "Carol", 5),
        ("Alice", "Carol", 10),
        ("Carol", "Dave", 12),
        ("Eve", "Alice", 15),
        ("Dave", "Eve", 16),
        ("Eve", "Frank", 18)
    ]
    for u, v, t in edges:
        G.add_edge(u, v, t=t)

    queries = TemporalQueries(G)

    # Draw a snapshot at t=20
    snapshot = G.snapshot(end_time=20)
    pos = nx.spring_layout(snapshot)
    nx.draw(snapshot, pos, with_labels=True, node_color='lightblue', node_size=2000, arrowsize=20)
    
    # Draw edges with timestamps
    edge_labels = {(u, v): f"t={d['time']}" for u, v, d in snapshot.edges(data=True)}
    nx.draw_networkx_edge_labels(snapshot, pos, edge_labels=edge_labels, font_color='red', font_size=12)

    plt.title("DyGraL Temporal Graph (Snapshot t=20)")
    plt.show()

    # Highlight chain motifs length=3 within 6 time units
    motifs = G.find_chain_motifs(length=3, within=6)
    print("Chain motifs length=3 within 6 time units:")
    for nodes, times in motifs:
        print(nodes, times)

if __name__ == "__main__":
    run_visual_example()
