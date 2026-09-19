"""Devanagari script processor combining normalizer, segmenter, composer, and decomposer."""

from __future__ import annotations

from grapheme_kit.core.processor import BaseScriptProcessor
from grapheme_kit.scripts.devanagari.composer import DevanagariComposer
from grapheme_kit.scripts.devanagari.decomposer import DevanagariDecomposer
from grapheme_kit.scripts.devanagari.normalizer import DevanagariNormalizer
from grapheme_kit.scripts.devanagari.profile import DevanagariProfile
from grapheme_kit.scripts.devanagari.segmenter import DevanagariSegmenter


class DevanagariProcessor(BaseScriptProcessor):
    """Complete Devanagari script processor (Hindi, Marathi, Sanskrit, Nepali)."""

    def __init__(self) -> None:
        profile = DevanagariProfile()
        super().__init__(
            profile=profile,
            normalizer=DevanagariNormalizer(),
            segmenter=DevanagariSegmenter(),
            composer=DevanagariComposer(profile=profile),
            decomposer=DevanagariDecomposer(profile=profile),
        )
