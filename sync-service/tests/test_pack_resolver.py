"""Tests for PackResolver service ensuring safe product packaging rules and guards."""

from pathlib import Path
import pytest
from app.services.pack_resolver import PackResolver


@pytest.fixture
def resolver():
    """Create standard resolver using repo catalog_pack_rules.json."""
    return PackResolver()


def test_override_precedence(resolver):
    """Explicit overrides from catalog_pack_rules.json must always take precedence."""
    # Matchbox bundles
    mult, src, reason = resolver.resolve_pack("03088", "114- R & G MATCH BOX SHANTHI(600DABBA)")
    assert mult == 1
    assert src == "override"
    assert "Matchbox bundle" in reason

    mult, src, _ = resolver.resolve_pack("04192", "115- R & G MATCH BOX RAYAL(600 DABBA)")
    assert mult == 1
    assert src == "override"

    # 10 Chorsa bundle
    mult, src, _ = resolver.resolve_pack("00186", "290- 10 CHORASA MUNNA DURGESH(100P=1BUND")
    assert mult == 1
    assert src == "override"

    # 16 Chorsa bundle
    mult, src, _ = resolver.resolve_pack("00223", "293- 16 CHORSA B GROUP (50P= 1 BUNDEL)")
    assert mult == 50
    assert src == "override"

    # Sparklers
    mult, src, _ = resolver.resolve_pack("00178", "148- RED BIJALI ROSE (100 PCS) 10 BAGS")
    assert mult == 10
    assert src == "override"

    # Lar garland overrides
    mult, src, _ = resolver.resolve_pack("02905", "W 1000 LAR (600 COUNTING) S.K.M")
    assert mult == 1
    assert src == "override"


def test_shots_exclusion_guard(resolver):
    """Multi-shot aerial repeaters describe tube counts and must default to 1."""
    # Pure shot counts
    mult, src, reason = resolver.resolve_pack("99001", "30 SHOTS MULTI COLOUR U V BOX AYYANAR")
    assert mult == 1
    assert src == "heuristic"
    assert "repeater" in reason.lower()

    mult, src, _ = resolver.resolve_pack("99002", "240 SHOTS CELEBRATION CAKE")
    assert mult == 1
    assert src == "heuristic"

    mult, src, _ = resolver.resolve_pack("99003", "120 SHOTS SKY SHOW")
    assert mult == 1
    assert src == "heuristic"


def test_garland_lar_exclusion_guard(resolver):
    """Garland cracker chains (1000 LAR, 600 COUNTING) must default to 1."""
    mult, src, reason = resolver.resolve_pack("99010", "1000 WALA LAR JAYEM ( 400) AUGUST")
    assert mult == 1
    assert src == "heuristic"
    assert "garland" in reason.lower()

    mult, src, _ = resolver.resolve_pack("99011", "5000 LAR (600) COUNTING SANTHANMARI")
    assert mult == 1
    assert src == "heuristic"


def test_paper_ply_exclusion_guard(resolver):
    """Paper ply thickness (12 PLY) must not be confused with pack multiples."""
    mult, src, reason = resolver.resolve_pack("99020", "RED FORT CRACKER ( 12 PLY )")
    assert mult == 1
    assert src == "heuristic"
    assert "ply" in reason.lower()


def test_dimensions_exclusion_guard(resolver):
    """Physical dimensions (10 CM, 15 CM, 4 INCH) must not be extracted as pack multiples."""
    mult, src, _ = resolver.resolve_pack("99030", "10 CM PLAIN SPARKLERS LEO")
    assert mult == 1
    assert src == "fallback"

    mult, src, _ = resolver.resolve_pack("99031", "15 CM GREEN SPARKLERS BHAWAN")
    assert mult == 1
    assert src == "fallback"


def test_dual_parenthetical_single_unit_guard(resolver):
    """Dual parentheticals ending in (1P) or (1 PCS) represent single unit packing."""
    mult, src, reason = resolver.resolve_pack("99040", "GIANT WHEEL AYYAN (5 PCS) (1P) BIG")
    assert mult == 1
    assert src == "heuristic"
    assert "single unit" in reason.lower()

    mult, src, _ = resolver.resolve_pack("99041", "CORONATION CANDLE B.F.W ( 10P) 1P")
    assert mult == 1
    assert src == "heuristic"


def test_positive_parenthetical_extraction(resolver):
    """Valid parenthetical pack tags must be accurately extracted."""
    # 5 P
    mult, src, _ = resolver.resolve_pack("99050", "10 CM COL CLASSIC (5 P)")
    assert mult == 5
    assert src == "heuristic"

    # 10 P
    mult, src, _ = resolver.resolve_pack("99051", "KIT-KAT (10 P) RAJHARISH")
    assert mult == 10
    assert src == "heuristic"

    # 25 PCS
    mult, src, _ = resolver.resolve_pack("99052", "NAAGARA FALLS ( 25 PCS) P.G")
    assert mult == 25
    assert src == "heuristic"


def test_truncated_parenthetical_handling(resolver):
    """Parentheticals truncated at 40 FoxPro characters must still be extracted."""
    # Truncated without closing parenthesis
    mult, src, _ = resolver.resolve_pack("99060", "28 CHORSA TAJ T/MEENA (50P= 1 BUND")
    assert mult == 50
    assert src == "heuristic"

    mult, src, _ = resolver.resolve_pack("99061", "GROUND CHAKKAR DELUXE AYYAN (10 P")
    assert mult == 10
    assert src == "heuristic"


def test_legacy_typo_handling(resolver):
    """Legacy typos like '1OOPKT' (capital O) must resolve to 100."""
    mult, src, _ = resolver.resolve_pack("99070", "10 CHORSA MUNNA (1OOPKT= 1 BOX)")
    assert mult == 100
    assert src == "heuristic"


def test_box_of_pattern(resolver):
    """Phrases like 'BOX OF 12' or 'PACK OF 5' must be extracted."""
    mult, src, _ = resolver.resolve_pack("99080", "SPECIAL SPARKLETS BOX OF 12")
    assert mult == 12
    assert src == "heuristic"


def test_safe_fallback_to_one(resolver):
    """Products with no packaging metadata must safely fallback to 1."""
    mult, src, reason = resolver.resolve_pack("99090", "STANDARD FLOWER POT DELUXE")
    assert mult == 1
    assert src == "fallback"
    assert "safe default" in reason.lower()


def test_custom_overlay_file_missing_graceful(tmp_path):
    """Missing overlay file must gracefully log and fallback without throwing."""
    non_existent = tmp_path / "non_existent.json"
    res = PackResolver(overlay_path=non_existent)
    assert res.rules == {}
    mult, src, _ = res.resolve_pack("00001", "TEST PRODUCT (5 P)")
    assert mult == 5
    assert src == "heuristic"
