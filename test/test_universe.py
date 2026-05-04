""""""

import src.constants as c
from src.economy import PoliticalSystem
from src.universe import GOVERNMENTS, PLANET_NAMES, Planet, Universe

testverse = Universe()

# Shared minimal government for creating isolated test planets
_GOVT = GOVERNMENTS[PoliticalSystem.ANARCHY]


def _planet_at(x: int, y: int) -> Planet:
    """Create a minimal Planet at (x, y) for distance testing."""
    return Planet("Test", x, y, 0, _GOVT, 0, 0, 0)


def test_planetcounts() -> None:
    """"""
    assert len(testverse.planets) == len(PLANET_NAMES)
    assert len(testverse.wormholes) == c.MAX_WORMHOLES


def test_wormholes() -> None:
    """"""
    assert all(isinstance(x, int) for x in testverse.wormholes)
    assert all(x in testverse.planets for x in testverse.wormholes)


def test_planetproperties() -> None:
    """"""
    assert all(isinstance(x, Planet) for x in testverse.planets.values())

    for i in testverse.planets:
        assert testverse.planets[i].name in PLANET_NAMES.values()
        assert testverse.planets[i].size in range(6)
        assert testverse.planets[i].get_govt_type() in GOVERNMENTS.values()
        assert testverse.planets[i].tech_level in range(
            testverse.planets[i].government.minTech, testverse.planets[i].government.maxTech + 1
        )
        assert testverse.planets[i].soci_pressure in range(8)
        assert testverse.planets[i].special_resource in range(13)
        assert testverse.planets[i].x in range(c.GALAXYWIDTH + 1)
        assert testverse.planets[i].y in range(c.GALAXYHEIGHT + 1)


def test_planetpositions() -> None:
    """
    Verify that the universe generator enforces the minimum distance invariant between planets.

    The C source places wormhole planets on a fixed grid without distance checking, so only non-wormhole vs. any-planet
    pairs are guaranteed to satisfy MIN_DISTANCE.

    The shuffle also swaps coordinates without re-checking, shuffle=False isolates the placement invariant from shuffle side-effects.
    """
    pre_shuffle = Universe(shuffle=False)
    wormhole_ids = set(pre_shuffle.wormholes)
    for i in pre_shuffle.planets:
        for j in pre_shuffle.planets:
            if i != j and not (i in wormhole_ids and j in wormhole_ids):
                assert pre_shuffle.planets[i].get_distance(pre_shuffle.planets[j]) >= c.MIN_DISTANCE


def test_universe() -> None:
    """"""
    pass


# ─── Distance calculation tests ───────────────────────────────────────────────
# The C source (Math.c) defines two functions:
#
#   SqrDistance(a, b) = (a.X-b.X)^2 + (a.Y-b.Y)^2   — integer, no sqrt
#   RealDistance(a, b) = int_sqrt(SqrDistance(a, b))  — nearest-integer rounding
#
# The C custom sqrt rounds to the nearest integer (not floor). The rounding
# condition is: if i^2 - sq > sq - (i-1)^2, return i-1, else return i.
# This is equivalent to Python's round() for all integer inputs that can arise
# from game coordinates (no exact-half cases exist in the integer range).
#
# Planet placement uses SqrDistance directly (no sqrt), so the rejection
# threshold is: sq <= SQR(MINDISTANCE + 1) = 49, not real_dist < 7.


def test_get_distance_pythagorean_3_4_5() -> None:
    """3-4-5 right triangle: exact integer sqrt, floor and round agree."""
    assert _planet_at(0, 0).get_distance(_planet_at(3, 4)) == 5


def test_get_distance_pythagorean_5_12_13() -> None:
    """5-12-13 right triangle: exact integer sqrt, floor and round agree."""
    assert _planet_at(0, 0).get_distance(_planet_at(5, 12)) == 13


def test_get_distance_rounds_not_floors() -> None:
    """
    C's custom integer sqrt rounds to nearest, not floor.

    dx=2, dy=2: sq=8, true sqrt ≈ 2.828 — C gives 3, floor gives 2.
    dx=4, dy=4: sq=32, true sqrt ≈ 5.657 — C gives 6, floor gives 5.
    dx=3, dy=5: sq=34, true sqrt ≈ 5.831 — C gives 6, floor gives 5.
    """
    assert _planet_at(0, 0).get_distance(_planet_at(2, 2)) == 3
    assert _planet_at(0, 0).get_distance(_planet_at(4, 4)) == 6
    assert _planet_at(0, 0).get_distance(_planet_at(3, 5)) == 6


def test_get_distance_is_symmetric() -> None:
    """Distance from A to B must equal distance from B to A."""
    a = _planet_at(30, 50)
    b = _planet_at(33, 54)  # sq = 9+16 = 25, dist = 5
    assert a.get_distance(b) == b.get_distance(a) == 5


def test_get_distance_min_distance_boundary() -> None:
    """
    The C generator rejects pairs with sq <= SQR(MINDISTANCE+1) = 49.

    - sq=49 (dx=0, dy=7): sits exactly on the rejection boundary.
    - sq=50 (dx=1, dy=7): the minimum squared distance a valid universe contains.

    Both round to get_distance == 7, confirming the generator must work in
    squared-distance space rather than relying on get_distance comparisons.
    """
    origin = _planet_at(0, 0)
    at_boundary = _planet_at(0, 7)  # sq = 49 — C rejects (<=49)
    just_inside = _planet_at(1, 7)  # sq = 50 — C accepts  (>49)

    assert (at_boundary.x - origin.x) ** 2 + (at_boundary.y - origin.y) ** 2 == c.MIN_DISTANCE**2
    assert (just_inside.x - origin.x) ** 2 + (just_inside.y - origin.y) ** 2 == c.MIN_DISTANCE**2 + 1
    # Both resolve to the same get_distance — showing why float comparison is insufficient
    assert origin.get_distance(at_boundary) == 7
    assert origin.get_distance(just_inside) == 7


def test_universe_squared_distance_invariant() -> None:
    """
    Non-wormhole planets must have SqrDistance > MIN_DISTANCE^2 (49) from every other planet (wormhole or not).

    Wormhole planets are placed on a fixed grid without distance checking (matching C source behaviour),
    so wormhole-vs-wormhole pairs are exempt.

    Verified in squared-distance space (exact integers) to match the C source invariant precisely,
    without floating-point rounding error at boundary values.

    The shuffle step is skipped (shuffle=False) to isolate the placement invariant.
    """
    universe = Universe(shuffle=False)
    threshold = c.MIN_DISTANCE**2  # 49 — mirrors C's SQR(MINDISTANCE + 1)
    wormhole_ids = set(universe.wormholes)
    for i, pi in universe.planets.items():
        for j, pj in universe.planets.items():
            # Skip wormhole-vs-wormhole: their grid placement gives no distance guarantee
            if i != j and not (i in wormhole_ids and j in wormhole_ids):
                sq = (pi.x - pj.x) ** 2 + (pi.y - pj.y) ** 2
                assert sq > threshold, (
                    f"{pi.name} ({pi.x},{pi.y}) and {pj.name} ({pj.x},{pj.y}): "
                    f"sq_dist={sq} not > threshold={threshold}"
                )
