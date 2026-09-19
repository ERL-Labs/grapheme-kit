"""Core abstract contract for grapheme-level metrics."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseMetric(ABC):
    """Abstract base class for all grapheme-aware metrics."""

    @abstractmethod
    def compute(self, *args: Any, **kwargs: Any) -> Any:
        """Compute the metric score."""
        raise NotImplementedError

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Allow metric instance to be called directly like a function."""
        return self.compute(*args, **kwargs)
