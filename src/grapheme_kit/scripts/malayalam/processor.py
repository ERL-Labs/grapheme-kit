"""Malayalam normalizer, segmenter, composer, decomposer, and processor."""

from __future__ import annotations

import grapheme
from grapheme_kit.core.composer import IndicComposer
from grapheme_kit.core.decomposer import IndicDecomposer
from grapheme_kit.core.normalizer import UnicodeNormalizer
from grapheme_kit.core.processor import BaseScriptProcessor
from grapheme_kit.core.segmenter import RuleBasedSegmenter
from grapheme_kit.scripts.malayalam.profile import MalayalamProfile


class MalayalamNormalizer(UnicodeNormalizer):
    """Handles Malayalam Unicode NFC normalization."""
    pass


class MalayalamSegmenter(RuleBasedSegmenter):
    """Malayalam grapheme segmenter."""
    pass


class MalayalamComposer(IndicComposer):
    """Malayalam grapheme composer combining chandrakkala consonants and vowels."""

    def __init__(self, profile: MalayalamProfile | None = None) -> None:
        super().__init__(profile=profile or MalayalamProfile())


class MalayalamDecomposer(IndicDecomposer):
    """Malayalam phonetic decomposer splitting syllables into consonant + virama + vowel."""

    def __init__(self, profile: MalayalamProfile | None = None) -> None:
        super().__init__(profile=profile or MalayalamProfile())


class MalayalamProcessor(BaseScriptProcessor):
    """Complete Malayalam script processor."""

    def __init__(self) -> None:
        profile = MalayalamProfile()
        super().__init__(
            profile=profile,
            normalizer=MalayalamNormalizer(),
            segmenter=MalayalamSegmenter(),
            composer=MalayalamComposer(profile=profile),
            decomposer=MalayalamDecomposer(profile=profile),
        )
