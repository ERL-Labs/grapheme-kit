"""Grapheme-aware distance metrics implementations."""

from __future__ import annotations

import textdistance
from grapheme_kit.graphemizer import Graphemizer
from grapheme_kit.metrics.base import BaseMetric


class Levenshtein(BaseMetric):
    """Grapheme-aware Levenshtein distance metric.
    
    Computes minimum edit distance (insertions, deletions, substitutions)
    treating multi-codepoint grapheme clusters as atomic single units.
    """

    def compute(self, s1: str, s2: str) -> int:
        return textdistance.levenshtein.distance(list(Graphemizer(s1)), list(Graphemizer(s2)))


class Hamming(BaseMetric):
    """Grapheme-aware Hamming distance metric.
    
    Computes number of positions with differing graphemes.
    """

    def compute(self, s1: str, s2: str) -> int:
        return textdistance.hamming.distance(list(Graphemizer(s1)), list(Graphemizer(s2)))


class DamerauLevenshtein(BaseMetric):
    """Grapheme-aware Damerau-Levenshtein distance metric.
    
    Accounts for insertions, deletions, substitutions, and transpositions of adjacent graphemes.
    """

    def compute(self, s1: str, s2: str) -> int:
        return textdistance.damerau_levenshtein.distance(list(Graphemizer(s1)), list(Graphemizer(s2)))
