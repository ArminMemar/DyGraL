import matplotlib.pyplot as plt
import networkx as nx
from dygral import TemporalGraph

G = TemporalGraph()
G.add_edge("Alice", "Bob", t=1)
G.add_edge("Bob", "Carol", t=5)
G.add_edge("Alice", "Carol", t=10)
G.add_edge("Carol", "Dave", t=12)

snapshot = G.snapshot(end_time=12)
pos = nx.spring_layout(snapshot)
labels = { (u, v): f"t={d['time']}" for u,v,d in snapshot.edges(data=True) }

plt.figure(figsize=(6,4))
nx.draw(snapshot, pos, with_labels=True, node_color="lightblue", node_size=2000, edgecolors="black")
nx.draw_networkx_edge_labels(snapshot, pos, edge_labels=labels)
plt.title("DyGraL Snapshot at t=12")
plt.show()
