"""Evaluation metrics module for grapheme-kit."""

from __future__ import annotations

from typing import Optional, Sequence
from grapheme_kit.metrics.evaluation import (
    CER,
    CharBLEU,
    GraphemeCHRF,
    extract_all_grapheme_ngrams,
)

_charbleu = CharBLEU()


def charbleu(
    reference: str,
    hypothesis: str,
    max_n: int = 4,
    weights: Optional[Sequence[float]] = None,
) -> float:
    """Grapheme-aware CharBLEU metric (character-level BLEU).

    Args:
        reference: The reference string to compare against.
        hypothesis: The candidate string to evaluate.
        max_n: Maximum n-gram order (default: 4).
        weights: Weights for each n-gram level.

    Returns:
        Score between 0.0 and 1.0.
    """
    return _charbleu.compute(reference, hypothesis, max_n=max_n, weights=weights)


__all__ = [
    "extract_all_grapheme_ngrams",
    "GraphemeCHRF",
    "CER",
    "CharBLEU",
    "charbleu",
]
