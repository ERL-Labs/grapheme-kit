"""Tests for Devanagari script processing (Hindi, Sanskrit, Marathi, Nepali)."""

import pytest
from grapheme_kit import Graphemizer, compose, decompose
from grapheme_kit.scripts.devanagari import (
    DevanagariComposer,
    DevanagariDecomposer,
    DevanagariNormalizer,
    DevanagariProcessor,
    DevanagariProfile,
    DevanagariSegmenter,
)


class TestDevanagariProfile:
    def test_profile_properties(self):
        profile = DevanagariProfile()
        assert profile.name == "devanagari"
        assert profile.virama == "्"
        assert profile.inherent_vowel == "अ"
        assert profile.is_consonant("क") is True
        assert profile.is_vowel("अ") is True
        assert profile.is_dependent_vowel_sign("ा") is True
        assert profile.vowel_sign_to_vowel("ा") == "आ"
        assert profile.vowel_to_vowel_sign("आ") == "ा"


class TestDevanagariNormalizer:
    def test_devanagari_nfc_and_nukta(self):
        norm = DevanagariNormalizer()
        # Decomposed nukta 'क' + '\u093c' normalized to canonical 'क़'
        assert norm.normalize("क\u093c") == "क़"
        assert norm.normalize("किताब") == "किताब"


class TestDevanagariSegmenter:
    def test_devanagari_segmentation(self):
        seg = DevanagariSegmenter()
        # "किताब" -> ['कि', 'ता', 'ब']
        assert seg.segment("किताब") == ["कि", "ता", "ब"]
        assert len(Graphemizer("किताब")) == 3

    def test_devanagari_conjuncts(self):
        seg = DevanagariSegmenter()
        assert seg.segment("क्षत्रिय") == ["क्ष", "त्रि", "य"]
        assert seg.segment("ज्ञान") == ["ज्ञा", "न"]


class TestDevanagariComposeDecompose:
    def test_decompose_consonant(self):
        assert decompose("क") == "क्अ"

    def test_decompose_vowel_sign(self):
        assert decompose("का") == "क्आ"
        assert decompose("कि") == "क्इ"
        assert decompose("की") == "क्ई"
        assert decompose("कु") == "क्उ"
        assert decompose("कू") == "क्ऊ"
        assert decompose("के") == "क्ए"
        assert decompose("कै") == "क्ऐ"
        assert decompose("को") == "क्ओ"
        assert decompose("कौ") == "क्औ"

    def test_compose_consonant(self):
        assert compose("क्अ") == "क"
        assert compose("क्आ") == "का"
        assert compose("क्इ") == "कि"
        assert compose("क्ई") == "की"
        assert compose("क्उ") == "कु"

    @pytest.mark.parametrize(
        "text",
        [
            "क", "का", "कि", "की", "कु", "कू", "के", "कै", "को", "कौ",
            "किताब", "भारत", "नमस्ते",
        ],
    )
    def test_devanagari_round_trip(self, text):
        """Verify compose(decompose(text)) == text for Devanagari."""
        assert compose(decompose(text)) == text
