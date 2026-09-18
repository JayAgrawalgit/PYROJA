"""Packaging rules resolver service for PYROJA.

Resolves product pack multiples and wholesale case quantities using a 3-tier precedence:
1. Explicit Overrides (catalog_pack_rules.json)
2. Guarded Heuristic Extraction (regex parsing with strict exclusion filters)
3. Safe Default (fallback to 1)

Enforces business safety constraints:
- Only explicit, enabled rules with status 'APPROVED' in catalog_pack_rules.json can set enforced_pack_multiple > 1.
- Heuristics suggest pack sizes for tablet UI quick increments and reporting, but enforced_pack_multiple is ALWAYS 1.
- Multi-shot repeaters (e.g. '30 SHOTS', '240 SHOTS') describe tube counts, not pack multiples.
- Garland crackers ('1000 LAR', '600 COUNTING') describe cracker counts, sold per garland box.
- Paper ply thickness ('12 PLY') describes paper thickness, not pack multiples.
- Length dimensions ('10 CM', '12 CM', '15 CM') describe physical length, not pack multiples.
- Dual parentheticals ending in (1P) or 1P indicate single sellable units.
- Auto-extracted pack multiples are strictly capped at <= 100 units. Any count > 100 falls back to 1.
"""

from dataclasses import dataclass
import json
import logging
from pathlib import Path
import re
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Regular expressions for guards and patterns
RE_SINGLE_UNIT_TAG = re.compile(
    r"(?:\(\s*1\s*(?:P|PCS?|PKT|BOX|NOS?|DABBI?)\s*\)|\b1\s*P(?:KT)?\s*(?:$|\bBIG|\bSTD|\bAYY|\bT/))",
    re.IGNORECASE,
)
RE_GARLAND_LAR = re.compile(
    r"(?:\b\d+\s*LAR\b|\bWALA\s+LAR\b|\bCOUNTING\b|\bGARLAND\b)",
    re.IGNORECASE,
)
RE_PAPER_PLY = re.compile(r"\b\d+\s*PLY\b", re.IGNORECASE)
RE_SHOTS_COUNT = re.compile(r"\b\d+\s*SHOTS?\b", re.IGNORECASE)
RE_DIMENSIONS = re.compile(r"\b\d+(?:\.\d+)?\s*(?:CM|MM|INCH|INCHES)\b", re.IGNORECASE)

# Positive patterns
RE_TYPO_100PKT = re.compile(r"\b1[oO]{2}\s*(?:PKT|P)\b", re.IGNORECASE)
RE_BUNDLE_RATIO = re.compile(
    r"\(\s*(\d{1,3})\s*(?:P|PCS?|PKT|DABBI?|NOS?)\s*=\s*\d+",
    re.IGNORECASE,
)
RE_DUAL_PACK_OUTER = re.compile(
    r"\(\s*\d+\s*(?:P|PCS?)\s*\)\s*(\d{1,2})\s*P\b",
    re.IGNORECASE,
)
RE_STANDARD_PACK_TAG = re.compile(
    r"\(\s*(\d{1,3})\s*(?:PCS?|P|PKTS?|BOX|DABBI?|NOS?|PIECES?|PRS?|TINS?)\b",
    re.IGNORECASE,
)
RE_BOX_OF = re.compile(
    r"\b(?:BOX|PACK|PKT|CASE)\s+OF\s+(\d{1,3})\b",
    re.IGNORECASE,
)


@dataclass
class PackResolution:
    """Detailed packaging resolution result distinguishing suggested from enforced multiples."""

    suggested_pack_multiple: int
    enforced_pack_multiple: int
    source: str            # 'override', 'heuristic', 'fallback'
    approval_status: str   # 'APPROVED', 'UNVERIFIED_HEURISTIC', 'DEFAULT', 'PENDING_REVIEW', 'DISABLED'
    reason: str

    @property
    def is_enforced(self) -> bool:
        """Whether a wholesale pack multiple > 1 is enforced."""
        return self.enforced_pack_multiple > 1

    def __iter__(self):
        """Backwards compatibility: allows unpacking as (suggested_multiple, source, reason)."""
        return iter((self.suggested_pack_multiple, self.source, self.reason))

    def __getitem__(self, item):
        """Backwards compatibility: indexing like a 3-tuple."""
        return (self.suggested_pack_multiple, self.source, self.reason)[item]


class PackResolver:
    """Service to resolve wholesale pack multiples and validate packaging rules."""

    def __init__(self, overlay_path: Optional[Path] = None):
        if overlay_path is None:
            self.overlay_path = Path(__file__).parent.parent / "data" / "catalog_pack_rules.json"
        else:
            self.overlay_path = Path(overlay_path)

        self.rules: Dict[str, Dict[str, Any]] = {}
        self.load_overlay_rules()

    def load_overlay_rules(self) -> None:
        """Load explicit rules from the overlay JSON file."""
        if not self.overlay_path.exists():
            logger.info(f"Catalog pack rules overlay file not found: {self.overlay_path}. Using empty rules.")
            self.rules = {}
            return

        try:
            with open(self.overlay_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.rules = data.get("rules", {})
                logger.info(f"Loaded {len(self.rules)} pack rule overrides from {self.overlay_path}")
        except Exception as e:
            logger.error(f"Failed to load catalog pack rules from {self.overlay_path}: {e}")
            self.rules = {}

    def resolve_pack(
        self,
        code: str,
        name: str,
        default: int = 1,
    ) -> PackResolution:
        """Resolve pack multiple for a product code and name.

        Returns:
            PackResolution containing suggested_pack_multiple, enforced_pack_multiple,
            source, approval_status, and reason.
        """
        clean_code = str(code).strip()
        clean_name = str(name).strip()
        name_upper = clean_name.upper()

        # Tier 1: Explicit Catalog Overrides
        if clean_code in self.rules:
            rule = self.rules[clean_code]
            is_enabled = rule.get("enabled", True) is True
            status = str(rule.get("status", "APPROVED")).strip().upper()
            is_approved = (status == "APPROVED")
            pack_mult = int(rule.get("pack_multiple", default) or default)
            reason = rule.get("reason", "Explicit catalog overlay rule")

            if is_enabled and is_approved:
                return PackResolution(
                    suggested_pack_multiple=pack_mult,
                    enforced_pack_multiple=pack_mult,
                    source="override",
                    approval_status="APPROVED",
                    reason=reason,
                )
            else:
                # Rule exists but is disabled or pending review: do not enforce above 1
                return PackResolution(
                    suggested_pack_multiple=pack_mult,
                    enforced_pack_multiple=1,
                    source="override",
                    approval_status="PENDING_REVIEW" if not is_approved else "DISABLED",
                    reason=f"{reason} (Rule unapproved or disabled; enforcement inactive)",
                )

        # Tier 2: Guarded Heuristic Extraction
        # Strict policy: Heuristics NEVER set enforced_pack_multiple > 1!
        # Guard 1: Single unit indicators (e.g. (1P), (1 PCS), ending in 1P)
        if RE_SINGLE_UNIT_TAG.search(name_upper):
            return PackResolution(
                suggested_pack_multiple=1,
                enforced_pack_multiple=1,
                source="heuristic",
                approval_status="UNVERIFIED_HEURISTIC",
                reason="Single unit indicator detected ((1P)/(1 PCS))",
            )

        # Guard 2: Garland cracker chains (e.g. 1000 LAR, 600 COUNTING, WALA LAR)
        if RE_GARLAND_LAR.search(name_upper):
            return PackResolution(
                suggested_pack_multiple=1,
                enforced_pack_multiple=1,
                source="heuristic",
                approval_status="UNVERIFIED_HEURISTIC",
                reason="Garland cracker string sold per piece/box",
            )

        # Guard 3: Paper ply thickness (e.g. 12 PLY)
        if RE_PAPER_PLY.search(name_upper):
            return PackResolution(
                suggested_pack_multiple=1,
                enforced_pack_multiple=1,
                source="heuristic",
                approval_status="UNVERIFIED_HEURISTIC",
                reason="Paper ply thickness specification (defaults to 1)",
            )

        # Guard 4: Pure multi-shot aerial repeaters (e.g. 30 SHOTS, 240 SHOTS)
        has_pack_tag = RE_STANDARD_PACK_TAG.search(name_upper)
        if not has_pack_tag and RE_SHOTS_COUNT.search(name_upper):
            return PackResolution(
                suggested_pack_multiple=1,
                enforced_pack_multiple=1,
                source="heuristic",
                approval_status="UNVERIFIED_HEURISTIC",
                reason="Multi-shot aerial repeater sold per unit",
            )

        # Pattern A: Typo '1OOPKT' or '1OOP' (capital O instead of zero)
        if RE_TYPO_100PKT.search(name_upper):
            return PackResolution(
                suggested_pack_multiple=100,
                enforced_pack_multiple=1,
                source="heuristic",
                approval_status="UNVERIFIED_HEURISTIC",
                reason="Extracted 100 from '1OOPKT' legacy typo (unverified heuristic)",
            )

        # Pattern B: Bundle ratio e.g. (10 DABBI=1BOX) or (50P= 1 BUNDEL)
        m_ratio = RE_BUNDLE_RATIO.search(name_upper)
        if m_ratio:
            val = int(m_ratio.group(1))
            if 1 <= val <= 100:
                return PackResolution(
                    suggested_pack_multiple=val,
                    enforced_pack_multiple=1,
                    source="heuristic",
                    approval_status="UNVERIFIED_HEURISTIC",
                    reason=f"Extracted pack multiple {val} from bundle ratio (unverified heuristic)",
                )

        # Pattern C: Outer multiple from dual pack like '(10 P) 2P'
        m_outer = RE_DUAL_PACK_OUTER.search(name_upper)
        if m_outer:
            val = int(m_outer.group(1))
            if 1 <= val <= 100:
                return PackResolution(
                    suggested_pack_multiple=val,
                    enforced_pack_multiple=1,
                    source="heuristic",
                    approval_status="UNVERIFIED_HEURISTIC",
                    reason=f"Extracted outer pack multiple {val} from dual pack tag (unverified heuristic)",
                )

        # Pattern D: Standard parenthetical pack tags (e.g. (10 P), (5 PCS), (25 P)
        if has_pack_tag:
            val = int(has_pack_tag.group(1))
            if 1 <= val <= 100:
                return PackResolution(
                    suggested_pack_multiple=val,
                    enforced_pack_multiple=1,
                    source="heuristic",
                    approval_status="UNVERIFIED_HEURISTIC",
                    reason=f"Extracted pack multiple {val} from parenthetical pack tag (unverified heuristic)",
                )

        # Pattern E: 'BOX OF 10', 'PACK OF 5', etc.
        m_box_of = RE_BOX_OF.search(name_upper)
        if m_box_of:
            val = int(m_box_of.group(1))
            if 1 <= val <= 100:
                return PackResolution(
                    suggested_pack_multiple=val,
                    enforced_pack_multiple=1,
                    source="heuristic",
                    approval_status="UNVERIFIED_HEURISTIC",
                    reason=f"Extracted pack multiple {val} from box-of pattern (unverified heuristic)",
                )

        # Tier 3: Safe Fallback
        return PackResolution(
            suggested_pack_multiple=default,
            enforced_pack_multiple=1,
            source="fallback",
            approval_status="DEFAULT",
            reason="No packaging multiple pattern detected; safe default to 1",
        )
