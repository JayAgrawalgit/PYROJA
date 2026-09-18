"""Tests for PackResolver service ensuring safe product packaging rules and guards."""

from pathlib import Path
import pytest
from app.services.pack_resolver import PackResolver, PackResolution


@pytest.fixture
def resolver():
    """Create standard resolver using repo catalog_pack_rules.json."""
    return PackResolver()


def test_override_precedence(resolver):
    """Explicit overrides from catalog_pack_rules.json must always take precedence."""
    # Matchbox bundles
    res = resolver.resolve_pack("03088", "114- R & G MATCH BOX SHANTHI(600DABBA)")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "override"
    assert res.approval_status == "APPROVED"
    assert "Matchbox bundle" in res.reason

    res = resolver.resolve_pack("04192", "115- R & G MATCH BOX RAYAL(600 DABBA)")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "override"
    assert res.approval_status == "APPROVED"

    # 10 Chorsa bundle
    res = resolver.resolve_pack("00186", "290- 10 CHORASA MUNNA DURGESH(100P=1BUND")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "override"
    assert res.approval_status == "APPROVED"

    # 16 Chorsa bundle
    res = resolver.resolve_pack("00223", "293- 16 CHORSA B GROUP (50P= 1 BUNDEL)")
    assert res.suggested_pack_multiple == 50
    assert res.enforced_pack_multiple == 50
    assert res.is_enforced is True
    assert res.source == "override"
    assert res.approval_status == "APPROVED"

    # Sparklers
    res = resolver.resolve_pack("00178", "148- RED BIJALI ROSE (100 PCS) 10 BAGS")
    assert res.suggested_pack_multiple == 10
    assert res.enforced_pack_multiple == 10
    assert res.is_enforced is True
    assert res.source == "override"
    assert res.approval_status == "APPROVED"

    # Lar garland overrides
    res = resolver.resolve_pack("02905", "W 1000 LAR (600 COUNTING) S.K.M")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "override"
    assert res.approval_status == "APPROVED"


def test_heuristic_never_enforces_above_one(resolver):
    """Unapproved heuristics may suggest pack sizes, but enforced_pack_multiple must strictly be 1."""
    # Heuristic 10 P
    res = resolver.resolve_pack("99051", "KIT-KAT (10 P) RAJHARISH")
    assert res.suggested_pack_multiple == 10
    assert res.enforced_pack_multiple == 1  # Crucial safety check: NOT ENFORCED!
    assert res.is_enforced is False
    assert res.source == "heuristic"
    assert res.approval_status == "UNVERIFIED_HEURISTIC"

    # Heuristic 25 PCS
    res = resolver.resolve_pack("99052", "NAAGARA FALLS ( 25 PCS) P.G")
    assert res.suggested_pack_multiple == 25
    assert res.enforced_pack_multiple == 1
    assert res.is_enforced is False
    assert res.source == "heuristic"
    assert res.approval_status == "UNVERIFIED_HEURISTIC"

    # Heuristic ratio
    res = resolver.resolve_pack("99060", "28 CHORSA TAJ T/MEENA (50P= 1 BUND")
    assert res.suggested_pack_multiple == 50
    assert res.enforced_pack_multiple == 1
    assert res.is_enforced is False


def test_disabled_or_pending_rule_never_enforced(tmp_path):
    """A rule in catalog_pack_rules.json with enabled=False or status!=APPROVED must not enforce."""
    import json
    rules_file = tmp_path / "test_rules.json"
    rules_file.write_text(json.dumps({
        "_version": "1.0.0",
        "rules": {
            "TEST_DIS": {
                "pack_multiple": 10,
                "enabled": False,
                "status": "APPROVED",
                "reason": "Disabled rule"
            },
            "TEST_PEND": {
                "pack_multiple": 20,
                "enabled": True,
                "status": "PENDING",
                "reason": "Pending business review"
            }
        }
    }))

    res = PackResolver(overlay_path=rules_file)

    res_dis = res.resolve_pack("TEST_DIS", "DISABLED PRODUCT")
    assert res_dis.suggested_pack_multiple == 10
    assert res_dis.enforced_pack_multiple == 1
    assert res_dis.approval_status == "DISABLED"

    res_pend = res.resolve_pack("TEST_PEND", "PENDING PRODUCT")
    assert res_pend.suggested_pack_multiple == 20
    assert res_pend.enforced_pack_multiple == 1
    assert res_pend.approval_status == "PENDING_REVIEW"


def test_shots_exclusion_guard(resolver):
    """Multi-shot aerial repeaters describe tube counts and must default suggested and enforced to 1."""
    # Pure shot counts
    res = resolver.resolve_pack("99001", "30 SHOTS MULTI COLOUR U V BOX AYYANAR")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"
    assert "repeater" in res.reason.lower()

    res = resolver.resolve_pack("99002", "240 SHOTS CELEBRATION CAKE")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"

    res = resolver.resolve_pack("99003", "120 SHOTS SKY SHOW")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"


def test_garland_lar_exclusion_guard(resolver):
    """Garland cracker chains (1000 LAR, 600 COUNTING) must default to 1."""
    res = resolver.resolve_pack("99010", "1000 WALA LAR JAYEM ( 400) AUGUST")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"
    assert "garland" in res.reason.lower()

    res = resolver.resolve_pack("99011", "5000 LAR (600) COUNTING SANTHANMARI")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"


def test_paper_ply_exclusion_guard(resolver):
    """Paper ply thickness (12 PLY) must not be confused with pack multiples."""
    res = resolver.resolve_pack("99020", "RED FORT CRACKER ( 12 PLY )")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"
    assert "ply" in res.reason.lower()


def test_dimensions_exclusion_guard(resolver):
    """Physical dimensions (10 CM, 15 CM, 4 INCH) must not be extracted as pack multiples."""
    res = resolver.resolve_pack("99030", "10 CM PLAIN SPARKLERS LEO")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "fallback"

    res = resolver.resolve_pack("99031", "15 CM GREEN SPARKLERS BHAWAN")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "fallback"


def test_dual_parenthetical_single_unit_guard(resolver):
    """Dual parentheticals ending in (1P) or (1 PCS) represent single unit packing."""
    res = resolver.resolve_pack("99040", "GIANT WHEEL AYYAN (5 PCS) (1P) BIG")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"
    assert "single unit" in res.reason.lower()

    res = resolver.resolve_pack("99041", "CORONATION CANDLE B.F.W ( 10P) 1P")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"


def test_positive_parenthetical_extraction(resolver):
    """Valid parenthetical pack tags must accurately populate suggested multiple while keeping enforced=1."""
    # 5 P
    res = resolver.resolve_pack("99050", "10 CM COL CLASSIC (5 P)")
    assert res.suggested_pack_multiple == 5
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"

    # 10 P
    res = resolver.resolve_pack("99051", "KIT-KAT (10 P) RAJHARISH")
    assert res.suggested_pack_multiple == 10
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"

    # 25 PCS
    res = resolver.resolve_pack("99052", "NAAGARA FALLS ( 25 PCS) P.G")
    assert res.suggested_pack_multiple == 25
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"


def test_truncated_parenthetical_handling(resolver):
    """Parentheticals truncated at 40 FoxPro characters must still extract suggested multiple."""
    # Truncated without closing parenthesis
    res = resolver.resolve_pack("99060", "28 CHORSA TAJ T/MEENA (50P= 1 BUND")
    assert res.suggested_pack_multiple == 50
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"

    res = resolver.resolve_pack("99061", "GROUND CHAKKAR DELUXE AYYAN (10 P")
    assert res.suggested_pack_multiple == 10
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"


def test_legacy_typo_handling(resolver):
    """Legacy typos like '1OOPKT' (capital O) must resolve suggested to 100."""
    res = resolver.resolve_pack("99070", "10 CHORSA MUNNA (1OOPKT= 1 BOX)")
    assert res.suggested_pack_multiple == 100
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"


def test_box_of_pattern(resolver):
    """Phrases like 'BOX OF 12' or 'PACK OF 5' must extract suggested multiple."""
    res = resolver.resolve_pack("99080", "SPECIAL SPARKLETS BOX OF 12")
    assert res.suggested_pack_multiple == 12
    assert res.enforced_pack_multiple == 1
    assert res.source == "heuristic"


def test_safe_fallback_to_one(resolver):
    """Products with no packaging metadata must safely fallback to 1."""
    res = resolver.resolve_pack("99090", "STANDARD FLOWER POT DELUXE")
    assert res.suggested_pack_multiple == 1
    assert res.enforced_pack_multiple == 1
    assert res.source == "fallback"
    assert "safe default" in res.reason.lower()


def test_custom_overlay_file_missing_graceful(tmp_path):
    """Missing overlay file must gracefully log and fallback without throwing."""
    non_existent = tmp_path / "non_existent.json"
    res = PackResolver(overlay_path=non_existent)
    assert res.rules == {}
    resolution = res.resolve_pack("00001", "TEST PRODUCT (5 P)")
    assert resolution.suggested_pack_multiple == 5
    assert resolution.enforced_pack_multiple == 1
    assert resolution.source == "heuristic"


def test_backwards_compatible_tuple_unpacking(resolver):
    """PackResolution must support unpacking as (suggested_multiple, source, reason)."""
    suggested, src, reason = resolver.resolve_pack("99050", "10 CM COL CLASSIC (5 P)")
    assert suggested == 5
    assert src == "heuristic"
    assert "parenthetical" in reason.lower()

    # Indexing test
    res = resolver.resolve_pack("99050", "10 CM COL CLASSIC (5 P)")
    assert res[0] == 5
    assert res[1] == "heuristic"
