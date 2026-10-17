from src.economy import PoliticalSystem
from src.screens.gamescreens import ShortRange
from src.universe import GOVERNMENTS, Planet


def _planet_at(x: int, y: int) -> Planet:
    return Planet("Test", x, y, 0, GOVERNMENTS[PoliticalSystem.ANARCHY], 0, 0, 0)


def test_short_range_chart_includes_its_square_boundary() -> None:
    center = _planet_at(50, 50)

    assert ShortRange._is_in_chart(_planet_at(70, 30), center)
    assert not ShortRange._is_in_chart(_planet_at(71, 50), center)
    assert not ShortRange._is_in_chart(_planet_at(50, 71), center)


def test_short_range_click_requires_proximity_to_system_marker() -> None:
    assert ShortRange._is_click_near_system(100, 100, 124, 100)
    assert not ShortRange._is_click_near_system(100, 100, 125, 100)
    assert not ShortRange._is_click_near_system(100, 100, 117, 117)