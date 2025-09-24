"""Simple streaming ingestion context manager."""

from .core import TemporalGraph

class GraphStream:
    """Context manager that yields a small stream controller for ingestion."""

    def __init__(self, graph: TemporalGraph = None, on_update=None):
        self.graph = graph if graph is not None else TemporalGraph()
        self.on_update = on_update

    def ingest(self, u, v, t, **attrs):
        self.graph.add_edge(u, v, t, **attrs)
        if self.on_update:
            try:
                self.on_update(u, v, t, **attrs)
            except Exception as e:
                print(f"[GraphStream] Warning: callback failed with {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
