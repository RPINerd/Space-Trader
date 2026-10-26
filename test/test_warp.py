from types import SimpleNamespace
from unittest.mock import Mock

import src.constants as c
from src.actions import warp
from src.commander import Commander


def _make_game(credits: int = 1000, wormholes: list[int] | None = None) -> tuple[dict, Mock]:
    current_planet = SimpleNamespace(get_distance=lambda target: 7)
    target_planet = SimpleNamespace()
    commander = Mock()
    commander.currentSystem = 0
    commander.credits = credits
    commander.debt = 0
    commander.insurance = False
    commander.noClaimDays = 0
    commander.timePlayed = 0
    commander.get_insurance_payment.return_value = 0
    commander.ship = SimpleNamespace(
        fuel=12,
        tank_capacity=20,
        fuel_cost=2,
    )
    game = {
        "commander": commander,
        "universe": SimpleNamespace(
            planets={0: current_planet, 1: target_planet},
            wormholes=wormholes or [],
        ),
        "target_system": target_planet,
    }
    return game, commander


def test_prep_for_warp_updates_normal_travel_state(monkeypatch) -> None:
    game, commander = _make_game()
    travel = Mock()
    monkeypatch.setattr(c, "GAME", game)
    monkeypatch.setattr(warp, "travel", travel)

    warp.prep_for_warp()

    assert commander.credits == 1000
    assert commander.ship.fuel == 5
    assert commander.timePlayed == 1
    assert game["arrived_via_wormhole"] is False
    assert game["clicks"] == 21
    commander.pay_interest.assert_called_once_with()
    travel.assert_called_once_with()


def test_prep_for_warp_rejects_unaffordable_wormhole_without_mutation(monkeypatch) -> None:
    game, commander = _make_game(credits=49, wormholes=[0, 1])
    travel = Mock()
    monkeypatch.setattr(c, "GAME", game)
    monkeypatch.setattr(warp, "travel", travel)

    warp.prep_for_warp()

    assert commander.credits == 49
    assert commander.ship.fuel == 12
    assert commander.timePlayed == 0
    assert "arrived_via_wormhole" not in game
    commander.pay_interest.assert_not_called()
    travel.assert_not_called()


def test_insurance_payment_query_does_not_mutate_commander() -> None:
    commander = Commander("Test", 1, 1, 1, 1)
    commander.insurance = True

    payment = commander.get_insurance_payment()

    assert payment > 0
    assert commander.credits == 1000
    assert commander.debt == 0
    assert commander.noClaimDays == 0

    commander.pay_insurance()

    assert commander.credits == 1000 - payment
    assert commander.noClaimDays == 1
