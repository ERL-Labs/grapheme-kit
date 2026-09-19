"""Tamil script support package."""

from grapheme_kit.scripts.tamil.profile import TamilProfile
from grapheme_kit.scripts.tamil.normalizer import TamilNormalizer
from grapheme_kit.scripts.tamil.segmenter import TamilSegmenter
from grapheme_kit.scripts.tamil.composer import TamilComposer
from grapheme_kit.scripts.tamil.decomposer import TamilDecomposer
from grapheme_kit.scripts.tamil.processor import TamilProcessor

__all__ = [
    "TamilProfile",
    "TamilNormalizer",
    "TamilSegmenter",
    "TamilComposer",
    "TamilDecomposer",
    "TamilProcessor",
]
