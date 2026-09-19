"""Graphemizer pipeline orchestrating normalization and script-aware grapheme splitting."""

from __future__ import annotations

from typing import Iterator
from grapheme_kit.core.registry import registry
from grapheme_kit.scripts import register_builtin_scripts
from grapheme_kit.utils.graphemes import GraphemeSplitter
from grapheme_kit.utils.normalizer import Normalizer

# Ensure built-ins are registered
register_builtin_scripts()


class Graphemizer:
    """Orchestrates script-aware text normalization and grapheme clustering.

    Provides iteration, length query, and grapheme cluster extraction.
    """

    def __init__(self, string: str, script: str | None = None) -> None:
        self.script = script
        self.normalizer = Normalizer()
        self.splitter = GraphemeSplitter()
        self.raw_string = string
        self._graphemes = self._process_text(string)

    @property
    def graphemes(self) -> list[str]:
        """List of extracted grapheme clusters."""
        return self._graphemes

    def __iter__(self) -> Iterator[str]:
        return iter(self._graphemes)

    def __len__(self) -> int:
        return len(self._graphemes)

    def __repr__(self) -> str:
        return f"Graphemizer({self.raw_string!r}, count={len(self._graphemes)})"

    def _process_text(self, raw_text: str) -> list[str]:
        """Takes raw string -> Normalize -> Split into Graphemes.

        Returns:
            List of Graphemes.
        """
        if raw_text is None or not raw_text:
            return []

        # If a specific script was requested, route through that processor
        if self.script:
            proc = registry.get(self.script)
            if proc:
                normalized = proc.normalize(raw_text)
                return proc.segment(normalized)

        # 1. Normalize
        normalized_text = self.normalizer.normalize(raw_text)

        # 2. Split
        graphemes = self.splitter.split(normalized_text)
        return graphemes
