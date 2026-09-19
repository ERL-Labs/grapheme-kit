"""Core object-oriented abstractions and pipeline engine for grapheme-kit."""

from grapheme_kit.core.normalizer import BaseNormalizer, UnicodeNormalizer
from grapheme_kit.core.segmenter import (
    BaseSegmenter,
    UnicodeSegmenter,
    SegmentationRule,
    ClusterMergeRule,
    CustomRule,
    RuleBasedSegmenter,
)
from grapheme_kit.core.composer import BaseComposer, IndicComposer
from grapheme_kit.core.decomposer import BaseDecomposer, IndicDecomposer
from grapheme_kit.core.profile import BaseScriptProfile
from grapheme_kit.core.processor import BaseScriptProcessor
from grapheme_kit.core.registry import ScriptRegistry, registry
from grapheme_kit.metrics.base import BaseMetric

__all__ = [
    "BaseNormalizer",
    "UnicodeNormalizer",
    "BaseSegmenter",
    "UnicodeSegmenter",
    "SegmentationRule",
    "ClusterMergeRule",
    "CustomRule",
    "RuleBasedSegmenter",
    "BaseComposer",
    "IndicComposer",
    "BaseDecomposer",
    "IndicDecomposer",
    "BaseScriptProfile",
    "BaseScriptProcessor",
    "ScriptRegistry",
    "registry",
    "BaseMetric",
]
