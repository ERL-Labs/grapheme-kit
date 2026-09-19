"""Tamil script processor combining normalizer, segmenter, composer, and decomposer."""

from __future__ import annotations

from grapheme_kit.core.processor import BaseScriptProcessor
from grapheme_kit.scripts.tamil.composer import TamilComposer
from grapheme_kit.scripts.tamil.decomposer import TamilDecomposer
from grapheme_kit.scripts.tamil.normalizer import TamilNormalizer
from grapheme_kit.scripts.tamil.profile import TamilProfile
from grapheme_kit.scripts.tamil.segmenter import TamilSegmenter


class TamilProcessor(BaseScriptProcessor):
    """Complete Tamil script processor."""

    def __init__(self) -> None:
        profile = TamilProfile()
        super().__init__(
            profile=profile,
            normalizer=TamilNormalizer(),
            segmenter=TamilSegmenter(),
            composer=TamilComposer(profile=profile),
            decomposer=TamilDecomposer(profile=profile),
        )
