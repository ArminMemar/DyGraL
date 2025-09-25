from dygral import TemporalGraph, TemporalQueries, GraphStream

def run_example():
    G = TemporalGraph(directed=True)

    # Add edges
    G.add_edge("Alice", "Bob", t=1)
    G.add_edge("Bob", "Carol", t=5)
    G.add_edge("Alice", "Carol", t=10)
    G.add_edge("Carol", "Dave", t=12)
    G.add_edge("Eve", "Alice", t=15)

    queries = TemporalQueries(G)

    print("Edges (time, u, v):")
    for e in G.list_edges():
        print(e)

    print('\nReachable Alice -> Carol at t=7?')
    print(queries.reachable_at("Alice", "Carol", 7))

    print('\nShortest path Alice -> Dave at t=12')
    path, times = queries.shortest_path_at("Alice", "Dave", 12)
    print("Path:", path)
    print("Edge times:", times)

    print('\nDegree of Bob at t=6:')
    print(queries.degree_at("Bob", 6))

    print('\nFind chain motifs length=3 within 6 time units:')
    motifs = queries.chain_motifs(length=3, within=6)
    for nodes, times in motifs:
        print(nodes, times)

    # Streaming ingestion
    print('\nStreaming new edges...')
    def on_update(u,v,t,**attrs):
        print(f"Stream added {u}->{v} at t={t}")
    with GraphStream(G, on_update=on_update) as s:
        s.ingest("Dave", "Eve", t=16)
        s.ingest("Eve", "Frank", t=18)

    print('\nReachable Alice -> Frank at t=20?')
    print(queries.reachable_at("Alice", "Frank", 20))

if __name__ == '__main__':
    run_example()
