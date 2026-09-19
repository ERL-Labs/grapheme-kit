"""Grapheme-aware similarity metrics implementations."""

from __future__ import annotations

import textdistance
from grapheme_kit.graphemizer import Graphemizer
from grapheme_kit.metrics.base import BaseMetric


class Jaro(BaseMetric):
    """Grapheme-aware Jaro similarity metric."""

    def compute(self, s1: str, s2: str) -> float:
        return float(textdistance.jaro.similarity(list(Graphemizer(s1)), list(Graphemizer(s2))))


class JaroWinkler(BaseMetric):
    """Grapheme-aware Jaro-Winkler similarity metric."""

    def compute(self, s1: str, s2: str) -> float:
        return float(textdistance.jaro_winkler.similarity(list(Graphemizer(s1)), list(Graphemizer(s2))))


class LCS(BaseMetric):
    """Grapheme-aware Longest Common Subsequence (LCS) metric."""

    def compute(self, s1: str, s2: str) -> int:
        g1 = list(Graphemizer(s1))
        g2 = list(Graphemizer(s2))

        m, n = len(g1), len(g2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if g1[i - 1] == g2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]
