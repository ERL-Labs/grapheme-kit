"""Tests for Metrics OOP hierarchy (Section 10 in PDF specification)."""

import pytest
from grapheme_kit import (
    BaseMetric,
    CER,
    CharBLEU,
    DamerauLevenshtein,
    GraphemeCHRF,
    Hamming,
    Jaro,
    JaroWinkler,
    LCS,
    Levenshtein,
    charbleu,
    damerau_levenshtein,
    hamming,
    jaro,
    jaro_winkler,
    levenshtein,
    longest_common_subsequence,
)


class TestMetricsOOPHierarchy:
    def test_concrete_metrics_inherit_directly_from_base_metric(self):
        metric_classes = (
            Levenshtein,
            Hamming,
            DamerauLevenshtein,
            Jaro,
            JaroWinkler,
            LCS,
            CER,
            GraphemeCHRF,
            CharBLEU,
        )

        for metric_class in metric_classes:
            assert issubclass(metric_class, BaseMetric)


class TestMetricsComputationParity:
    def test_levenshtein_class_and_function(self):
        metric = Levenshtein()
        assert metric.compute("ஸ்ரீ", "ஸ்ரி") == levenshtein("ஸ்ரீ", "ஸ்ரி")
        # Test callable instance
        assert metric("ஸ்ரீ", "ஸ்ரி") == 2

    def test_hamming_class_and_function(self):
        metric = Hamming()
        assert metric.compute("ක්‍රමය", "ක්මය") == hamming("ක්‍රමය", "ක්මය")
        assert metric("ක්‍රමය", "ක්මය") == 1

    def test_damerau_levenshtein_class_and_function(self):
        metric = DamerauLevenshtein()
        assert metric.compute("ab", "ba") == damerau_levenshtein("ab", "ba")
        assert metric("ab", "ba") == 1

    def test_jaro_class_and_function(self):
        metric = Jaro()
        assert metric.compute("martha", "marhta") == jaro("martha", "marhta")
        assert metric("martha", "marhta") == pytest.approx(0.9444, rel=1e-3)

    def test_jaro_winkler_class_and_function(self):
        metric = JaroWinkler()
        assert metric.compute("martha", "marhta") == jaro_winkler("martha", "marhta")
        assert metric("martha", "marhta") == pytest.approx(0.9611, rel=1e-3)

    def test_lcs_class_and_function(self):
        metric = LCS()
        assert metric.compute("ABCD", "ACD") == longest_common_subsequence("ABCD", "ACD")
        assert metric("ABCD", "ACD") == 3

    def test_cer_class_and_function(self):
        cer = CER()
        # Direct function call
        score_fn = CER("நல்ல", "நல்ல மாணவன்")
        # Instance method call
        score_inst = cer.compute("நல்ல", "நல்ல மாணவன்")
        assert score_fn == score_inst

    def test_chrf_class_computation(self):
        metric = GraphemeCHRF()
        score = metric.compute("வணக்கம்", "வணக்கம்")
        assert score == 100.0

    def test_charbleu_class_and_function(self):
        metric = CharBLEU()
        score_cls = metric.compute("the quick brown fox", "the quick red fox")
        score_fn = charbleu("the quick brown fox", "the quick red fox")
        assert score_cls == pytest.approx(score_fn, rel=1e-4)
