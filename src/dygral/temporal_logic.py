"""Tiny helpers for temporal assertions / checks."""

from typing import Callable

class TemporalLogic:
    @staticmethod
    def always(predicate: Callable[[int], bool], times):
        """Return True if predicate(t) holds for every t in times."""
        for t in times:
            if not predicate(t):
                return False
        return True

    @staticmethod
    def eventually(predicate: Callable[[int], bool], times):
        """Return True if predicate(t) holds for at least one t in times."""
        for t in times:
            if predicate(t):
                return True
        return False
