"""Grapheme-aware string distance and similarity functions and classes."""

from __future__ import annotations

from grapheme_kit.metrics.distance import DamerauLevenshtein, Hamming, Levenshtein
from grapheme_kit.metrics.similarity import LCS, Jaro, JaroWinkler

# Singleton instances for functional API
_levenshtein = Levenshtein()
_hamming = Hamming()
_damerau_levenshtein = DamerauLevenshtein()
_jaro = Jaro()
_jaro_winkler = JaroWinkler()
_lcs = LCS()


def levenshtein(s1: str, s2: str) -> int:
    """Grapheme-aware Levenshtein distance between two strings."""
    return _levenshtein.compute(s1, s2)


def hamming(s1: str, s2: str) -> int:
    """Grapheme-aware Hamming distance between two strings.
    Strings must have equal number of graphemes.
    """
    return _hamming.compute(s1, s2)


def damerau_levenshtein(s1: str, s2: str) -> int:
    """Grapheme-aware Damerau-Levenshtein distance between two strings.
    
    This metric accounts for insertions, deletions, substitutions, and 
    transpositions (swapping adjacent graphemes) as single edit operations.
    """
    return _damerau_levenshtein.compute(s1, s2)


def jaro(s1: str, s2: str) -> float:
    """Grapheme-aware Jaro similarity between two strings.
    
    Returns a similarity score between 0 and 1, where 1 indicates identical strings.
    """
    return _jaro.compute(s1, s2)


def jaro_winkler(s1: str, s2: str) -> float:
    """Grapheme-aware Jaro-Winkler similarity between two strings.
    
    Returns a similarity score between 0 and 1, where 1 indicates identical strings.
    """
    return _jaro_winkler.compute(s1, s2)


def longest_common_subsequence(s1: str, s2: str) -> int:
    """Grapheme-aware Longest Common Subsequence (LCS) length between two strings."""
    return _lcs.compute(s1, s2)


__all__ = [
    "levenshtein",
    "hamming",
    "damerau_levenshtein",
    "jaro",
    "jaro_winkler",
    "longest_common_subsequence",
    "Levenshtein",
    "Hamming",
    "DamerauLevenshtein",
    "Jaro",
    "JaroWinkler",
    "LCS",
]
