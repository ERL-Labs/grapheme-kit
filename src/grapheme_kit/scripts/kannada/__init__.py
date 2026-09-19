"""Kannada script support package."""

from grapheme_kit.scripts.kannada.profile import KannadaProfile
from grapheme_kit.scripts.kannada.processor import (
    KannadaNormalizer,
    KannadaSegmenter,
    KannadaComposer,
    KannadaDecomposer,
    KannadaProcessor,
)

__all__ = [
    "KannadaProfile",
    "KannadaNormalizer",
    "KannadaSegmenter",
    "KannadaComposer",
    "KannadaDecomposer",
    "KannadaProcessor",
]
