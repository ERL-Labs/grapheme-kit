"""Tests for Malayalam script processing."""

import pytest
from grapheme_kit import Graphemizer, compose, decompose
from grapheme_kit.scripts.malayalam import (
    MalayalamComposer,
    MalayalamDecomposer,
    MalayalamNormalizer,
    MalayalamProcessor,
    MalayalamProfile,
    MalayalamSegmenter,
)


class TestMalayalam:
    def test_profile_properties(self):
        profile = MalayalamProfile()
        assert profile.name == "malayalam"
        assert profile.virama == "്"
        assert profile.inherent_vowel == "അ"
        assert profile.is_consonant("ക") is True
        assert profile.is_vowel("അ") is True
        assert profile.is_dependent_vowel_sign("ാ") is True

    def test_decompose_consonant(self):
        assert decompose("ക") == "ക്അ"
        assert decompose("കാ") == "ക്ആ"
        assert decompose("കി") == "ക്ഇ"

    def test_compose_consonant(self):
        assert compose("ക്അ") == "ക"
        assert compose("ക്ആ") == "കാ"
        assert compose("ക്ഇ") == "കി"

    @pytest.mark.parametrize(
        "text",
        ["ക", "കാ", "കി", "കീ", "കു", "കൂ", "കേ", "കൈ", "കൊ", "കോ", "നമസ്കാരം"],
    )
    def test_malayalam_round_trip(self, text):
        assert compose(decompose(text)) == text
