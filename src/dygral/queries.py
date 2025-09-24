"""Convenience wrappers for common temporal queries."""

from .core import TemporalGraph

class TemporalQueries:
    def __init__(self, graph: TemporalGraph):
        self.g = graph

    def reachable_at(self, a, b, t):
        return self.g.reachable(a, b, at=t)

    def reachable_in_window(self, a, b, start, end):
        return self.g.reachable(a, b, window=(start, end))

    def shortest_path_at(self, a, b, t):
        return self.g.shortest_path(a, b, at=t)

    def degree_at(self, node, t):
        return self.g.degree(node, at=t)

    def chain_motifs(self, length=3, within=None, window=None):
        return self.g.find_chain_motifs(length=length, within=within, window=window)
