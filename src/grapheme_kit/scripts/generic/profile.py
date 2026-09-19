"""Generic fallback script profile for universal/unregistered languages."""

from __future__ import annotations

from grapheme_kit.core.profile import BaseScriptProfile


class GenericProfile(BaseScriptProfile):
    """Universal fallback profile for scripts without language-specific overrides."""

    def __init__(self) -> None:
        super().__init__(
            name="generic",
            unicode_ranges=[],
        )

    def is_in_script(self, text: str) -> bool:
        return True
