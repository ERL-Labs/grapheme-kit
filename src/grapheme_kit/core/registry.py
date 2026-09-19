"""Central Script Registry for dynamic registration and script dispatch."""

from __future__ import annotations

from collections import Counter
from typing import Sequence
from grapheme_kit.core.processor import BaseScriptProcessor


class ScriptRegistry:
    """Registry managing script processors and script-aware dispatching."""

    def __init__(self) -> None:
        self._processors: dict[str, BaseScriptProcessor] = {}
        self._aliases: dict[str, str] = {}
        self._fallback_processor: BaseScriptProcessor | None = None

    def register(
        self,
        processor: BaseScriptProcessor,
        aliases: Sequence[str] | None = None,
        is_fallback: bool = False,
    ) -> None:
        """Register a script processor with optional aliases.

        Args:
            processor: Processor instance implementing BaseScriptProcessor.
            aliases: Optional list of alternative script names (e.g. 'hindi' for devanagari).
            is_fallback: Whether to use this processor for unregistered/generic text.
        """
        key = processor.name.lower()
        self._processors[key] = processor

        if aliases:
            for alias in aliases:
                self._aliases[alias.lower()] = key

        if is_fallback or self._fallback_processor is None:
            self._fallback_processor = processor

    def get(self, script_name: str) -> BaseScriptProcessor | None:
        """Get registered processor by script name or alias."""
        key = script_name.lower()
        resolved = self._aliases.get(key, key)
        return self._processors.get(resolved)

    def list_scripts(self) -> list[str]:
        """List all canonically registered script names."""
        return list(self._processors.keys())

    def detect_script(self, text: str) -> str:
        """Detect the dominant script of a text string from Unicode code points."""
        if not text:
            return "generic"

        counts: Counter[str] = Counter()
        for char in text:
            if char.isspace() or char in ("\u200c", "\u200d"):
                continue
            cp = ord(char)
            matched = False
            for name, proc in self._processors.items():
                if name == "generic":
                    continue
                for start, end in proc.profile.unicode_ranges:
                    if start <= cp <= end:
                        counts[name] += 1
                        matched = True
                        break
                if matched:
                    break

        if not counts:
            return "generic"

        dominant, _ = counts.most_common(1)[0]
        return dominant

    def get_processor_for_text(self, text: str) -> BaseScriptProcessor:
        """Return the best matching processor for the provided text."""
        script = self.detect_script(text)
        proc = self.get(script)
        if proc is not None:
            return proc
        if self._fallback_processor is not None:
            return self._fallback_processor
        raise RuntimeError("No script processor or fallback processor registered.")

    def get_processor_for_char(self, char: str) -> BaseScriptProcessor | None:
        """Return the processor whose profile matches the given character, if any."""
        if not char:
            return None
        cp = ord(char[0])
        for proc in self._processors.values():
            if proc.name.lower() == "generic":
                continue
            for start, end in proc.profile.unicode_ranges:
                if start <= cp <= end:
                    return proc
        return None

    def compose(self, text: str) -> str:
        """Compose decomposed text by routing script clusters to their respective processors."""
        if not text:
            return ""

        # Group contiguous characters of the same script or process via segmenter
        import grapheme
        clusters = list(grapheme.graphemes(text))
        result: list[str] = []
        i = 0
        n = len(clusters)

        while i < n:
            curr = clusters[i]
            proc = self.get_processor_for_char(curr)
            if proc is not None:
                # Collect all contiguous clusters belonging to the same script
                chunk = [curr]
                i += 1
                while i < n and (self.get_processor_for_char(clusters[i]) == proc or clusters[i].isspace()):
                    chunk.append(clusters[i])
                    i += 1
                result.append(proc.compose("".join(chunk)))
            else:
                result.append(curr)
                i += 1

        return "".join(result)

    def decompose(self, text: str) -> str:
        """Decompose text by routing script clusters to their respective processors."""
        if not text:
            return ""

        import grapheme
        clusters = list(grapheme.graphemes(text))
        result: list[str] = []

        for curr in clusters:
            proc = self.get_processor_for_char(curr)
            if proc is not None:
                result.append(proc.decompose(curr))
            else:
                result.append(curr)

        return "".join(result)


# Global default registry instance
registry = ScriptRegistry()
