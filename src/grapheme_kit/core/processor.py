"""Script processor architecture aggregating normalizer, segmenter, composer, and decomposer."""

from __future__ import annotations

from dataclasses import dataclass
from grapheme_kit.core.composer import BaseComposer
from grapheme_kit.core.decomposer import BaseDecomposer
from grapheme_kit.core.normalizer import BaseNormalizer
from grapheme_kit.core.profile import BaseScriptProfile
from grapheme_kit.core.segmenter import BaseSegmenter


class BaseScriptProcessor:
    """Base class for a script processor combining all pipeline stages.

    Combines:
    - BaseNormalizer
    - BaseSegmenter
    - BaseComposer
    - BaseDecomposer
    - BaseScriptProfile
    """

    def __init__(
        self,
        profile: BaseScriptProfile,
        normalizer: BaseNormalizer,
        segmenter: BaseSegmenter,
        composer: BaseComposer,
        decomposer: BaseDecomposer,
    ) -> None:
        self.profile = profile
        self.normalizer = normalizer
        self.segmenter = segmenter
        self.composer = composer
        self.decomposer = decomposer

    @property
    def name(self) -> str:
        """Name of the script handled by this processor."""
        return self.profile.name

    def normalize(self, text: str) -> str:
        """Normalize text using the script's normalizer."""
        return self.normalizer.normalize(text)

    def segment(self, text: str) -> list[str]:
        """Segment text into graphemes using the script's segmenter."""
        return self.segmenter.segment(text)

    def compose(self, text: str) -> str:
        """Compose decomposed text using the script's composer."""
        return self.composer.compose(text)

    def decompose(self, text: str) -> str:
        """Decompose text using the script's decomposer."""
        return self.decomposer.decompose(text)

    def is_in_script(self, text: str) -> bool:
        """Check if text belongs to this processor's script."""
        return self.profile.is_in_script(text)
