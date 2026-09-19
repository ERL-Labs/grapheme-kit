"""Sinhala script processor combining normalizer, segmenter, composer, and decomposer."""

from __future__ import annotations

from grapheme_kit.core.processor import BaseScriptProcessor
from grapheme_kit.scripts.sinhala.composer import SinhalaComposer
from grapheme_kit.scripts.sinhala.decomposer import SinhalaDecomposer
from grapheme_kit.scripts.sinhala.normalizer import SinhalaNormalizer
from grapheme_kit.scripts.sinhala.profile import SinhalaProfile
from grapheme_kit.scripts.sinhala.segmenter import SinhalaSegmenter


class SinhalaProcessor(BaseScriptProcessor):
    """Complete Sinhala script processor."""

    def __init__(self) -> None:
        profile = SinhalaProfile()
        super().__init__(
            profile=profile,
            normalizer=SinhalaNormalizer(),
            segmenter=SinhalaSegmenter(),
            composer=SinhalaComposer(profile=profile),
            decomposer=SinhalaDecomposer(profile=profile),
        )
