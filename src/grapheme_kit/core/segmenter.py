"""Core grapheme segmentation contracts and rule-based segmenter implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Sequence
import grapheme


class BaseSegmenter(ABC):
    """Abstract base class for grapheme cluster segmenters."""

    @abstractmethod
    def segment(self, text: str) -> list[str]:
        """Split input text into a list of grapheme clusters.

        Args:
            text: Input text string.

        Returns:
            List of grapheme clusters.
        """
        raise NotImplementedError


class UnicodeSegmenter(BaseSegmenter):
    """Segmenter implementing standard Unicode UAX #29 grapheme cluster boundaries."""

    def segment(self, text: str) -> list[str]:
        """Segment text using standard Unicode grapheme cluster boundaries.

        Args:
            text: Input string.

        Returns:
            List of standard Unicode grapheme clusters.
        """
        if text is None or not text:
            return []
        return list(grapheme.graphemes(text))


class SegmentationRule(ABC):
    """Abstract base class for declarative script-specific segmentation rules."""

    @abstractmethod
    def apply(self, clusters: list[str]) -> list[str]:
        """Apply the rule to a list of grapheme clusters.

        Args:
            clusters: Current list of grapheme clusters.

        Returns:
            Transformed list of grapheme clusters.
        """
        raise NotImplementedError


class ClusterMergeRule(SegmentationRule):
    """Declarative rule to merge adjacent clusters matching a condition."""

    def __init__(
        self,
        name: str,
        condition: Callable[[str, str], bool],
        merge_fn: Callable[[str, str], str] | None = None,
    ) -> None:
        self.name = name
        self.condition = condition
        self.merge_fn = merge_fn or (lambda a, b: a + b)

    def apply(self, clusters: list[str]) -> list[str]:
        if len(clusters) < 2:
            return list(clusters)

        result: list[str] = []
        i = 0
        n = len(clusters)

        while i < n:
            current = clusters[i]
            if i < n - 1 and self.condition(current, clusters[i + 1]):
                result.append(self.merge_fn(current, clusters[i + 1]))
                i += 2
            else:
                result.append(current)
                i += 1

        return result


class CustomRule(SegmentationRule):
    """Adapter for function-based segmentation rules."""

    def __init__(self, name: str, fn: Callable[[list[str]], list[str]]) -> None:
        self.name = name
        self.fn = fn

    def apply(self, clusters: list[str]) -> list[str]:
        return self.fn(clusters)


class RuleBasedSegmenter(UnicodeSegmenter):
    """Segmenter that extends Unicode grapheme boundaries with script-specific rules."""

    def __init__(self, rules: Sequence[SegmentationRule] | None = None) -> None:
        self.rules: list[SegmentationRule] = list(rules) if rules else []

    def add_rule(self, rule: SegmentationRule) -> RuleBasedSegmenter:
        """Add a rule to the segmentation pipeline."""
        self.rules.append(rule)
        return self

    def segment(self, text: str) -> list[str]:
        """Segment text via Unicode boundaries then apply script correction rules."""
        if text is None or not text:
            return []

        clusters = super().segment(text)
        for rule in self.rules:
            clusters = rule.apply(clusters)
        return clusters
