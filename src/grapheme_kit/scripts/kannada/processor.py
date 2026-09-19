"""Kannada normalizer, segmenter, composer, decomposer, and processor."""

from __future__ import annotations

import grapheme
from grapheme_kit.core.composer import IndicComposer
from grapheme_kit.core.decomposer import IndicDecomposer
from grapheme_kit.core.normalizer import UnicodeNormalizer
from grapheme_kit.core.processor import BaseScriptProcessor
from grapheme_kit.core.segmenter import RuleBasedSegmenter
from grapheme_kit.scripts.kannada.profile import KannadaProfile


class KannadaNormalizer(UnicodeNormalizer):
    """Handles Kannada Unicode NFC normalization."""
    pass


class KannadaSegmenter(RuleBasedSegmenter):
    """Kannada grapheme segmenter."""
    pass


class KannadaComposer(IndicComposer):
    """Kannada grapheme composer combining halant consonants and vowels."""

    def __init__(self, profile: KannadaProfile | None = None) -> None:
        super().__init__(profile=profile or KannadaProfile())


class KannadaDecomposer(IndicDecomposer):
    """Kannada phonetic decomposer splitting syllables into consonant + virama + vowel."""

    def __init__(self, profile: KannadaProfile | None = None) -> None:
        super().__init__(profile=profile or KannadaProfile())


class KannadaProcessor(BaseScriptProcessor):
    """Complete Kannada script processor."""

    def __init__(self) -> None:
        profile = KannadaProfile()
        super().__init__(
            profile=profile,
            normalizer=KannadaNormalizer(),
            segmenter=KannadaSegmenter(),
            composer=KannadaComposer(profile=profile),
            decomposer=KannadaDecomposer(profile=profile),
        )
