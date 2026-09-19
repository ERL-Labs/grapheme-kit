"""Tests for Core Architecture abstract classes, base implementations, and contracts."""

import pytest
from grapheme_kit.core import (
    BaseNormalizer,
    UnicodeNormalizer,
    BaseSegmenter,
    UnicodeSegmenter,
    SegmentationRule,
    ClusterMergeRule,
    CustomRule,
    RuleBasedSegmenter,
    BaseComposer,
    IndicComposer,
    BaseDecomposer,
    IndicDecomposer,
    BaseScriptProfile,
    BaseScriptProcessor,
    BaseMetric,
)


class TestCoreNormalizer:
    def test_base_normalizer_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            BaseNormalizer()

    def test_unicode_normalizer_nfc(self):
        normalizer = UnicodeNormalizer(form="NFC")
        assert normalizer.normalize("e\u0301") == "é"
        assert normalizer.normalize("") == ""
        assert normalizer.normalize(None) == ""

    def test_unicode_normalizer_nfd(self):
        normalizer = UnicodeNormalizer(form="NFD")
        assert normalizer.normalize("é") == "e\u0301"

    def test_unicode_normalizer_invalid_form(self):
        with pytest.raises(ValueError, match="Invalid Unicode normalization form"):
            UnicodeNormalizer(form="INVALID")


class TestCoreSegmenter:
    def test_base_segmenter_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            BaseSegmenter()

    def test_unicode_segmenter(self):
        segmenter = UnicodeSegmenter()
        assert segmenter.segment("hello") == ["h", "e", "l", "l", "o"]
        assert segmenter.segment("") == []
        assert segmenter.segment(None) == []

    def test_rule_based_segmenter_with_cluster_merge_rule(self):
        segmenter = RuleBasedSegmenter()
        # Custom rule: merge 'a' followed by 'b' into 'ab'
        rule = ClusterMergeRule(
            name="merge_ab",
            condition=lambda curr, nxt: curr == "a" and nxt == "b",
        )
        segmenter.add_rule(rule)
        assert segmenter.segment("ab c") == ["ab", " ", "c"]

    def test_rule_based_segmenter_with_custom_rule(self):
        segmenter = RuleBasedSegmenter()
        rule = CustomRule("reverse", lambda clusters: list(reversed(clusters)))
        segmenter.add_rule(rule)
        assert segmenter.segment("abc") == ["c", "b", "a"]


class TestCoreProfile:
    def test_base_script_profile_lookups(self):
        profile = BaseScriptProfile(
            name="test_script",
            unicode_ranges=[(0x1000, 0x1050)],
            consonants=["က", "ခ"],
            vowels=["အ", "အာ"],
            dependent_vowel_signs=["", "ာ"],
            virama="်",
            inherent_vowel="အ",
        )
        assert profile.is_consonant("က") is True
        assert profile.is_vowel("အ") is True
        assert profile.is_dependent_vowel_sign("ာ") is True
        assert profile.vowel_sign_to_vowel("ာ") == "အာ"
        assert profile.vowel_to_vowel_sign("အာ") == "ာ"
        assert profile.is_in_script("က") is True
        assert profile.is_in_script("hello") is False


class TestCoreProcessor:
    def test_script_processor_delegation(self):
        profile = BaseScriptProfile(
            name="dummy",
            unicode_ranges=[(0x0041, 0x005A)],
        )
        normalizer = UnicodeNormalizer()
        segmenter = UnicodeSegmenter()

        class DummyComposer(BaseComposer):
            def compose(self, text: str) -> str:
                return text.upper()

        class DummyDecomposer(BaseDecomposer):
            def decompose(self, text: str) -> str:
                return text.lower()

        proc = BaseScriptProcessor(
            profile=profile,
            normalizer=normalizer,
            segmenter=segmenter,
            composer=DummyComposer(),
            decomposer=DummyDecomposer(),
        )

        assert proc.name == "dummy"
        assert proc.normalize("abc") == "abc"
        assert proc.segment("abc") == ["a", "b", "c"]
        assert proc.compose("abc") == "ABC"
        assert proc.decompose("ABC") == "abc"
        assert proc.is_in_script("HELLO") is True
