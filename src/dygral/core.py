"""Core temporal graph implementation (prototype)

Design goals:
- Simple API for adding time-stamped edges
- Snapshot extraction for time-based queries
- Small and easily extensible for research
"""

from collections import defaultdict
import networkx as nx
from bisect import bisect_right

class TemporalGraph:
    """Temporal graph storing edges as time-stamped events.

    Edges are stored internally in a sorted list and a time-index for quick window queries.
    This is a prototype: replacing the naive lists with persistent indexes (e.g. sortedcontainers)
    will be necessary for scale.
    """

    def __init__(self, directed=True):
        self.directed = directed
        # master list of edges as tuples (t, u, v, attrs)
        self._edges = []
        # time -> list of edge indices (for quick lookup)
        self._time_index = defaultdict(list)
        # set of nodes
        self.nodes = set()
        # maintain a sorted list of timestamps
        self._times = []

    def add_edge(self, u, v, t, **attrs):
        """Add a time-stamped edge (u -> v) occurring at time t.

        Args:
            u, v: node identifiers (hashable)
            t: numeric timestamp (int or float)
            attrs: optional attributes stored on the edge
        """
        record = (t, u, v, attrs)
        # append and maintain time index
        self._edges.append(record)
        self._time_index[t].append(len(self._edges) - 1)
        if t not in self._times:
            # insert preserving order
            i = bisect_right(self._times, t)
            self._times.insert(i, t)
        self.nodes.add(u)
        self.nodes.add(v)

    def edges_between(self, start=None, end=None):
        """Yield edges whose timestamp is between start and end (inclusive).

        If start is None, include from -inf. If end is None, include to +inf.
        """
        if start is None and end is None:
            for t, u, v, attrs in self._edges:
                yield (t, u, v, attrs)
            return

        # simple strategy: iterate times between start and end
        lo = 0
        hi = len(self._times)
        if start is not None:
            lo = bisect_right(self._times, start - 1e-9)
        if end is not None:
            hi = bisect_right(self._times, end)
        for t in self._times[lo:hi]:
            for idx in self._time_index[t]:
                yield self._edges[idx]

    def snapshot(self, end_time, start_time=None):
        """Build and return a networkx.Graph snapshot that includes edges with timestamps
        t such that (start_time is None or t >= start_time) and t <= end_time.

        This snapshot is a simple view and can be used for static algorithms.
        """
        if self.directed:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        for t, u, v, attrs in self.edges_between(start=start_time, end=end_time):
            G.add_edge(u, v, time=t, **attrs)
        return G

    # ---------- Query helpers ---------------
    def reachable(self, source, target, at=None, window=None):
        """Return True if target is reachable from source in the snapshot defined by
        either at (all edges <= at) or window=(start,end).
        """
        if window is not None:
            start, end = window
        else:
            start, end = None, at
        G = self.snapshot(end_time=end, start_time=start)
        try:
            return nx.has_path(G, source, target)
        except nx.NetworkXError:
            return False

    def shortest_path(self, source, target, at=None, window=None):
        if window is not None:
            start, end = window
        else:
            start, end = None, at
        G = self.snapshot(end_time=end, start_time=start)
        try:
            path = nx.shortest_path(G, source, target)
            # also return path length and the edge times list
            times = [G[u][v]["time"] for u, v in zip(path[:-1], path[1:])]
            return path, times
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None, None

    def degree(self, node, at=None, window=None):
        if window is not None:
            start, end = window
        else:
            start, end = None, at
        G = self.snapshot(end_time=end, start_time=start)
        if node not in G:
            return 0
        return G.degree(node)

    def find_chain_motifs(self, length=3, within=None, window=None):
        """Find chain motifs of the form v0->v1->...->v_{length-1} where consecutive
        edges occur within `within` time units.

        This is a naive implementation: iterate over sorted edges and look for subsequent
        matching edges. Returns a list of tuples: (nodes_list, times_list)
        """
        # collect edges in time order with filter
        if window is not None:
            start, end = window
        else:
            start, end = None, None
        edges = list(self.edges_between(start=start, end=end))
        edges.sort(key=lambda r: r[0])  # sort by time
        results = []
        n = len(edges)
        # naive DFS of depth length-1 across edges respecting time ordering
        def dfs(path_nodes, path_times, last_index):
            if len(path_nodes) == length:
                results.append((list(path_nodes), list(path_times)))
                return
            last_node = path_nodes[-1]
            last_time = path_times[-1]
            for j in range(last_index + 1, n):
                t, u, v, attrs = edges[j]
                if u == last_node:
                    if within is None or (t - last_time) <= within:
                        path_nodes.append(v)
                        path_times.append(t)
                        dfs(path_nodes, path_times, j)
                        path_nodes.pop()
                        path_times.pop()
        # start
        for i in range(n):
            t, u, v, attrs = edges[i]
            dfs([u, v], [t, t], i)
        return results

    # utility: pretty-print edges
    def list_edges(self):
        return list(self._edges)