"""grapheme-kit: A grapheme-aware toolkit for segmenting, comparing, and evaluating text across scripts."""

from __future__ import annotations

# Core contracts and pipeline
from grapheme_kit.core import (
    BaseComposer,
    BaseDecomposer,
    BaseMetric,
    BaseNormalizer,
    BaseScriptProcessor,
    BaseScriptProfile,
    BaseSegmenter,
    ClusterMergeRule,
    CustomRule,
    IndicComposer,
    IndicDecomposer,
    RuleBasedSegmenter,
    ScriptRegistry,
    SegmentationRule,
    UnicodeNormalizer,
    UnicodeSegmenter,
    registry,
)

# Built-in processors
from grapheme_kit.scripts import (
    DevanagariProcessor,
    GenericProcessor,
    KannadaProcessor,
    MalayalamProcessor,
    SinhalaProcessor,
    TamilProcessor,
)

# High-level pipeline and utilities
from grapheme_kit.composer import Composer, compose
from grapheme_kit.decomposer import Decomposer, decompose
from grapheme_kit.graphemizer import Graphemizer

# Distance & similarity metrics
from grapheme_kit.distance import (
    DamerauLevenshtein,
    Hamming,
    Jaro,
    JaroWinkler,
    LCS,
    Levenshtein,
    damerau_levenshtein,
    hamming,
    jaro,
    jaro_winkler,
    levenshtein,
    longest_common_subsequence,
)

# Evaluation metrics
from grapheme_kit.metric import (
    CER,
    CharBLEU,
    GraphemeCHRF,
    charbleu,
    extract_all_grapheme_ngrams,
)

__all__ = [
    # Core contracts
    "BaseNormalizer",
    "UnicodeNormalizer",
    "BaseSegmenter",
    "UnicodeSegmenter",
    "RuleBasedSegmenter",
    "SegmentationRule",
    "ClusterMergeRule",
    "CustomRule",
    "BaseComposer",
    "IndicComposer",
    "BaseDecomposer",
    "IndicDecomposer",
    "BaseScriptProfile",
    "BaseScriptProcessor",
    "BaseMetric",
    "ScriptRegistry",
    "registry",
    # Built-in script processors
    "TamilProcessor",
    "SinhalaProcessor",
    "DevanagariProcessor",
    "MalayalamProcessor",
    "KannadaProcessor",
    "GenericProcessor",
    # Main tools
    "Graphemizer",
    "Composer",
    "compose",
    "Decomposer",
    "decompose",
    # Functional metrics
    "levenshtein",
    "hamming",
    "damerau_levenshtein",
    "jaro",
    "jaro_winkler",
    "longest_common_subsequence",
    "CER",
    "GraphemeCHRF",
    "charbleu",
    "extract_all_grapheme_ngrams",
    # OOP metric classes
    "Levenshtein",
    "Hamming",
    "DamerauLevenshtein",
    "Jaro",
    "JaroWinkler",
    "LCS",
    "CharBLEU",
]
