"""Malayalam script support package."""

from grapheme_kit.scripts.malayalam.profile import MalayalamProfile
from grapheme_kit.scripts.malayalam.processor import (
    MalayalamNormalizer,
    MalayalamSegmenter,
    MalayalamComposer,
    MalayalamDecomposer,
    MalayalamProcessor,
)

__all__ = [
    "MalayalamProfile",
    "MalayalamNormalizer",
    "MalayalamSegmenter",
    "MalayalamComposer",
    "MalayalamDecomposer",
    "MalayalamProcessor",
]
