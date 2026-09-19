"""Tests for Kannada script processing."""

import pytest
from grapheme_kit import Graphemizer, compose, decompose
from grapheme_kit.scripts.kannada import (
    KannadaComposer,
    KannadaDecomposer,
    KannadaNormalizer,
    KannadaProcessor,
    KannadaProfile,
    KannadaSegmenter,
)


class TestKannada:
    def test_profile_properties(self):
        profile = KannadaProfile()
        assert profile.name == "kannada"
        assert profile.virama == "್"
        assert profile.inherent_vowel == "ಅ"
        assert profile.is_consonant("ಕ") is True
        assert profile.is_vowel("ಅ") is True
        assert profile.is_dependent_vowel_sign("ಾ") is True

    def test_decompose_consonant(self):
        assert decompose("ಕ") == "ಕ್ಅ"
        assert decompose("ಕಾ") == "ಕ್ಆ"
        assert decompose("ಕಿ") == "ಕ್ಇ"

    def test_compose_consonant(self):
        assert compose("ಕ್ಅ") == "ಕ"
        assert compose("ಕ್ಆ") == "ಕಾ"
        assert compose("ಕ್ಇ") == "ಕಿ"

    @pytest.mark.parametrize(
        "text",
        ["ಕ", "ಕಾ", "ಕಿ", "ಕೀ", "ಕು", "ಕೂ", "ಕೆ", "ಕೈ", "ಕೊ", "ಕೋ", "ನಮಸ್ಕಾರ"],
    )
    def test_kannada_round_trip(self, text):
        assert compose(decompose(text)) == text
