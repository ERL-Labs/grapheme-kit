"""Sinhala script support package."""

from grapheme_kit.scripts.sinhala.profile import SinhalaProfile
from grapheme_kit.scripts.sinhala.normalizer import SinhalaNormalizer
from grapheme_kit.scripts.sinhala.segmenter import SinhalaSegmenter
from grapheme_kit.scripts.sinhala.composer import SinhalaComposer
from grapheme_kit.scripts.sinhala.decomposer import SinhalaDecomposer
from grapheme_kit.scripts.sinhala.processor import SinhalaProcessor

__all__ = [
    "SinhalaProfile",
    "SinhalaNormalizer",
    "SinhalaSegmenter",
    "SinhalaComposer",
    "SinhalaDecomposer",
    "SinhalaProcessor",
]
