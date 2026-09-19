"""Generic fallback script processor with standard Unicode rules."""

from __future__ import annotations

from grapheme_kit.core.composer import BaseComposer
from grapheme_kit.core.decomposer import BaseDecomposer
from grapheme_kit.core.normalizer import UnicodeNormalizer
from grapheme_kit.core.processor import BaseScriptProcessor
from grapheme_kit.core.segmenter import UnicodeSegmenter
from grapheme_kit.scripts.generic.profile import GenericProfile


class GenericComposer(BaseComposer):
    """Pass-through composer for generic text."""

    def compose(self, text: str) -> str:
        return text if text else ""


class GenericDecomposer(BaseDecomposer):
    """Pass-through decomposer for generic text."""

    def decompose(self, text: str) -> str:
        return text if text else ""


class GenericProcessor(BaseScriptProcessor):
    """Universal fallback processor."""

    def __init__(self) -> None:
        super().__init__(
            profile=GenericProfile(),
            normalizer=UnicodeNormalizer(),
            segmenter=UnicodeSegmenter(),
            composer=GenericComposer(),
            decomposer=GenericDecomposer(),
        )
