"""Tamil segmenter with linguistic rules for conjunct clusters (க்ஷ, ஸ்ரீ, ஶ்ரீ)."""

from __future__ import annotations

from grapheme_kit.core.segmenter import ClusterMergeRule, RuleBasedSegmenter


class TamilSegmenter(RuleBasedSegmenter):
    """Tamil grapheme segmenter with script-specific cluster merging rules."""

    def __init__(self) -> None:
        super().__init__()

        # Rule 1: க் + ஷ... -> க்ஷ...
        self.add_rule(
            ClusterMergeRule(
                name="tamil_ksha",
                condition=lambda curr, nxt: curr == "க்" and nxt.startswith("ஷ"),
            )
        )

        # Rule 2: ஸ் + ரீ -> ஸ்ரீ
        self.add_rule(
            ClusterMergeRule(
                name="tamil_sree",
                condition=lambda curr, nxt: curr == "ஸ்" and nxt == "ரீ",
            )
        )

        # Rule 3: ஶ் + ரீ -> ஶ்ரீ
        self.add_rule(
            ClusterMergeRule(
                name="tamil_shree",
                condition=lambda curr, nxt: curr == "ஶ்" and nxt == "ரீ",
            )
        )
