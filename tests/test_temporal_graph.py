import pytest
from dygral import TemporalGraph, TemporalQueries, GraphStream

def test_basic_reachability():
    G = TemporalGraph()
    G.add_edge('A','B', t=1)
    G.add_edge('B','C', t=2)
    assert G.reachable('A','C', at=2)
    assert not G.reachable('C','A', at=2)

def test_shortest_path_and_degree():
    G = TemporalGraph()
    G.add_edge('X','Y', t=1)
    G.add_edge('Y','Z', t=5)
    path, times = G.shortest_path('X','Z', at=6)
    assert path == ['X','Y','Z']
    assert len(times) == 2
    assert G.degree('Y', at=6) >= 1

def test_chain_motifs():
    G = TemporalGraph()
    G.add_edge('A','B', t=1)
    G.add_edge('B','C', t=2)
    G.add_edge('C','D', t=3)
    motifs = G.find_chain_motifs(length=3, within=2)
    found = any(m[0] == ['A','B','C'] for m in motifs)
    assert found

def test_graphstream_ingest():
    G = TemporalGraph()
    events = []

    def on_update(u,v,t,**attrs):
        events.append((u,v,t))

    with GraphStream(G, on_update=on_update) as stream:
        stream.ingest("X", "Y", t=10)
        stream.ingest("Y", "Z", t=12)

    assert len(events) == 2
    assert G.reachable("X", "Z", at=12)
