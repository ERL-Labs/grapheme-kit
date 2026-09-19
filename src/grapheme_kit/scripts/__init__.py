"""Script implementations and built-in registration for grapheme-kit."""

from grapheme_kit.core.registry import registry
from grapheme_kit.scripts.generic import GenericProcessor
from grapheme_kit.scripts.tamil import TamilProcessor
from grapheme_kit.scripts.sinhala import SinhalaProcessor
from grapheme_kit.scripts.devanagari import DevanagariProcessor
from grapheme_kit.scripts.malayalam import MalayalamProcessor
from grapheme_kit.scripts.kannada import KannadaProcessor


def register_builtin_scripts() -> None:
    """Register all built-in scripts and aliases into the global ScriptRegistry."""
    # Generic fallback
    registry.register(
        GenericProcessor(),
        aliases=["default", "latin", "english", "en"],
        is_fallback=True,
    )

    # Tamil
    registry.register(TamilProcessor(), aliases=["ta"])

    # Sinhala
    registry.register(SinhalaProcessor(), aliases=["si"])

    # Devanagari (Hindi, Sanskrit, Marathi, Nepali)
    registry.register(
        DevanagariProcessor(),
        aliases=["hindi", "hi", "sanskrit", "sa", "marathi", "mr", "nepali", "ne"],
    )

    # Malayalam
    registry.register(MalayalamProcessor(), aliases=["malayalam", "ml"])

    # Kannada
    registry.register(KannadaProcessor(), aliases=["kannada", "kn"])


# Auto-register upon import
register_builtin_scripts()

__all__ = [
    "TamilProcessor",
    "SinhalaProcessor",
    "DevanagariProcessor",
    "MalayalamProcessor",
    "KannadaProcessor",
    "GenericProcessor",
    "register_builtin_scripts",
]
