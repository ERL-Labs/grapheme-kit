"""Grapheme-aware evaluation metrics: CER, GraphemeCHRF, and CharBLEU."""

from __future__ import annotations

import math
from collections import Counter
from typing import Any, Dict, List, Optional, Sequence, Union

import textdistance
from sacrebleu.metrics.chrf import CHRF
from sacrebleu.metrics.helpers import extract_word_ngrams

from grapheme_kit.graphemizer import Graphemizer
from grapheme_kit.metrics.base import BaseMetric


def extract_all_grapheme_ngrams(
    graphemes: List[str], max_order: int, include_whitespace: bool = False
) -> List[Counter]:
    """Extracts all grapheme n-grams at once for convenience."""
    counters: list[Counter] = []
    if not include_whitespace:
        graphemes = [g for g in graphemes if g.strip() != ""]

    for n in range(1, max_order + 1):
        ngrams = Counter([tuple(graphemes[i : i + n]) for i in range(len(graphemes) - n + 1)])
        counters.append(ngrams)

    return counters


import abc


class _CERMeta(abc.ABCMeta):
    """Metaclass allowing CER to be called directly as CER(hyp, ref) or instantiated as CER()."""

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
            instance = super().__call__()
            return instance.compute(*args, **kwargs)
        return super().__call__(*args, **kwargs)


class CER(BaseMetric, metaclass=_CERMeta):
    """Character Error Rate (CER) computed at the grapheme cluster level.
    
    Can be used both as a class:
        cer = CER()
        score = cer.compute(hypothesis, reference)
    or directly as a function:
        score = CER(hypothesis, reference)
    """

    def compute(self, hypothesis: str, reference: str) -> float:
        hyp_graphemes = list(Graphemizer(hypothesis))
        ref_graphemes = list(Graphemizer(reference))
        if len(reference) == 0:
            return 0.0 if len(hypothesis) == 0 else 1.0

        dist = textdistance.levenshtein.distance(hyp_graphemes, ref_graphemes)
        return dist / len(ref_graphemes)


class GraphemeCHRF(CHRF, BaseMetric):
    """Computes the chrF(++) metric at the grapheme cluster level."""

    def compute(self, hypothesis: str, reference: Union[str, Sequence[str]]) -> float:
        """Compute sentence-level chrF score."""
        refs = [reference] if isinstance(reference, str) else list(reference)
        return float(self.sentence_score(hypothesis, refs).score)

    def _graphemize(self, text: str) -> List[str]:
        return list(Graphemizer(text))

    def _preprocess_segment(self, sent: Union[str, List[str]]) -> List[str]:
        if isinstance(sent, str):
            graphemes = self._graphemize(sent)
        else:
            graphemes = sent
        return [g.lower() for g in graphemes] if self.lowercase else graphemes

    def _remove_punctuation_for_words(self, graphemes: List[str]) -> List[str]:
        reconstructed_string = "".join(graphemes)
        return super()._remove_punctuation(reconstructed_string)

    def _extract_reference_info(self, refs: Sequence[str]) -> Dict[str, List[List[Counter]]]:
        ngrams = []
        for ref in refs:
            ref_graphemes = self._preprocess_segment(ref)
            stats = extract_all_grapheme_ngrams(ref_graphemes, self.char_order, self.whitespace)
            if self.word_order > 0:
                ref_words = self._remove_punctuation_for_words(ref_graphemes)
                for n in range(self.word_order):
                    stats.append(extract_word_ngrams(ref_words, n + 1))
            ngrams.append(stats)
        return {"ref_ngrams": ngrams}

    def _compute_segment_statistics(self, hypothesis: str, ref_kwargs: Dict) -> List[int]:
        best_stats: list[int] = []
        best_f_score = -1.0

        hyp_graphemes = self._preprocess_segment(hypothesis)
        all_hyp_ngrams = extract_all_grapheme_ngrams(
            hyp_graphemes, self.char_order, self.whitespace
        )

        if self.word_order > 0:
            hwords = self._remove_punctuation_for_words(hyp_graphemes)
            _range = range(1, self.word_order + 1)
            all_hyp_ngrams.extend([extract_word_ngrams(hwords, n) for n in _range])

        for _ref_ngrams in ref_kwargs["ref_ngrams"]:
            stats: list[int] = []
            for h, r in zip(all_hyp_ngrams, _ref_ngrams):
                stats.extend(self._get_match_statistics(h, r))
            f_score = self._compute_f_score(stats)

            if f_score > best_f_score:
                best_f_score = f_score
                best_stats = stats

        return best_stats


class CharBLEU(BaseMetric):
    """Grapheme-aware CharBLEU metric (character-level BLEU)."""

    def compute(
        self,
        reference: str,
        hypothesis: str,
        max_n: int = 4,
        weights: Optional[Sequence[float]] = None,
    ) -> float:
        if not reference or not hypothesis:
            return 1.0 if reference == hypothesis else 0.0

        ref_graphemes = list(Graphemizer(reference))
        hyp_graphemes = list(Graphemizer(hypothesis))

        if ref_graphemes == hyp_graphemes:
            return 1.0

        if weights is None:
            weights = [1.0 / max_n] * max_n

        precisions: list[float] = []
        valid_n_values: list[int] = []

        for n in range(1, max_n + 1):
            if len(hyp_graphemes) < n:
                continue

            ref_ngrams = [tuple(ref_graphemes[i : i + n]) for i in range(len(ref_graphemes) - n + 1)]
            hyp_ngrams = [tuple(hyp_graphemes[i : i + n]) for i in range(len(hyp_graphemes) - n + 1)]

            ref_ngram_counts: dict[tuple, int] = {}
            for ngram in ref_ngrams:
                ref_ngram_counts[ngram] = ref_ngram_counts.get(ngram, 0) + 1

            matches = 0
            for ngram in hyp_ngrams:
                if ngram in ref_ngram_counts and ref_ngram_counts[ngram] > 0:
                    matches += 1
                    ref_ngram_counts[ngram] -= 1

            precision = matches / len(hyp_ngrams) if hyp_ngrams else 0.0
            if precision > 0:
                precisions.append(precision)
                valid_n_values.append(n)

        if not precisions:
            return 0.0

        if len(hyp_graphemes) < len(ref_graphemes):
            brevity_penalty = (
                max(0, 1 - len(ref_graphemes) / len(hyp_graphemes)) if len(hyp_graphemes) > 0 else 0
            )
            brevity_penalty = max(0, 1 - brevity_penalty)
        else:
            brevity_penalty = 1.0

        normalized_weights: list[float] = []
        weight_sum = sum(weights[n - 1] for n in valid_n_values)
        for n in valid_n_values:
            normalized_weights.append(weights[n - 1] / weight_sum)

        log_precisions = [math.log(p) * w for p, w in zip(precisions, normalized_weights)]
        geo_mean = math.exp(sum(log_precisions))

        return geo_mean * brevity_penalty
