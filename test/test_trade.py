from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from src import constants, universe
from src.actions.trade import buy_good, get_bays, sell_good
from src.economy import Ware
from src.screens import trade as trade_screen


@pytest.fixture
def game(monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    commander = SimpleNamespace(
        cargo=[0] * 10,
        credits=100,
        currentSystem=0,
        ship=SimpleNamespace(cargo=15),
    )
    planet = SimpleNamespace(trade_items=[5] * 10, trade_prices=[10] * 10)
    universe = SimpleNamespace(planets=[planet])
    monkeypatch.setattr(constants, "GAME", {"commander": commander, "universe": universe})
    return SimpleNamespace(commander=commander, planet=planet)


def test_buy_good_limits_purchase_by_stock_credits_and_capacity(
    game: SimpleNamespace,
) -> None:
    game.commander.cargo[Ware.WATER] = 13

    buy_good(Ware.WATER)

    assert game.commander.cargo[Ware.WATER] == 15
    assert game.commander.credits == 80
    assert game.planet.trade_items[Ware.WATER] == 3
    assert get_bays() == "Bays: 15/15"


def test_buy_good_respects_requested_amount(game: SimpleNamespace) -> None:
    buy_good(Ware.WATER, amount=2)

    assert game.commander.cargo[Ware.WATER] == 2
    assert game.commander.credits == 80
    assert game.planet.trade_items[Ware.WATER] == 3


def test_sell_good_limits_sale_to_carried_amount(game: SimpleNamespace) -> None:
    game.commander.cargo[Ware.WATER] = 4

    sell_good(Ware.WATER, amount=2)

    assert game.commander.cargo[Ware.WATER] == 2
    assert game.commander.credits == 120


def test_trade_actions_reject_invalid_ware_ids(game: SimpleNamespace) -> None:
    with pytest.raises(ValueError, match="Invalid ware ID"):
        buy_good(99)


def test_planet_calculates_prices_and_updates_cached_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(universe, "randint", lambda low, _high: low)
    planet = universe.Planet(
        "Test",
        0,
        0,
        0,
        universe.GOVERNMENTS[universe.PoliticalSystem.ANARCHY],
        7,
        0,
        universe.SpecialResource.NOTHING,
    )

    assert planet.trade_prices[Ware.WATER] == 49
    planet.trade_prices[Ware.WATER] = 0

    planet.update_trade_prices()

    assert planet.trade_prices[Ware.WATER] == 49


def test_universe_refreshes_prices_for_every_planet() -> None:
    planets = [Mock(), Mock()]
    generated_universe = universe.Universe.__new__(universe.Universe)
    generated_universe.planets = dict(enumerate(planets))

    generated_universe.update_trade_prices()

    for planet in planets:
        planet.update_trade_prices.assert_called_once_with()


@pytest.mark.parametrize(
    ("screen_type", "prompt_method", "action_method"),
    [
        (trade_screen.BuyCargo, "_prompt_buy_amount", "_buy_good"),
        (trade_screen.SellCargo, "_prompt_sell_amount", "_sell_good"),
    ],
)
def test_quantity_prompt_forwards_entered_amount(
    monkeypatch: pytest.MonkeyPatch,
    screen_type: type,
    prompt_method: str,
    action_method: str,
) -> None:
    prompt = Mock(return_value=3)
    monkeypatch.setattr(trade_screen.simpledialog, "askinteger", prompt)
    screen = SimpleNamespace()
    action = Mock()
    setattr(screen, action_method, action)

    getattr(screen_type, prompt_method)(screen, Ware.WATER)

    prompt.assert_called_once_with(
        "Buy Cargo" if screen_type is trade_screen.BuyCargo else "Sell Cargo",
        "How many Water do you want to buy?"
        if screen_type is trade_screen.BuyCargo
        else "How many Water do you want to sell?",
        parent=screen,
        minvalue=1,
    )
    action.assert_called_once_with(Ware.WATER, 3)


@pytest.mark.parametrize(
    ("screen_type", "prompt_method", "action_method"),
    [
        (trade_screen.BuyCargo, "_prompt_buy_amount", "_buy_good"),
        (trade_screen.SellCargo, "_prompt_sell_amount", "_sell_good"),
    ],
)
def test_cancelled_quantity_prompt_does_not_trade(
    monkeypatch: pytest.MonkeyPatch,
    screen_type: type,
    prompt_method: str,
    action_method: str,
) -> None:
    monkeypatch.setattr(trade_screen.simpledialog, "askinteger", Mock(return_value=None))
    screen = SimpleNamespace()
    action = Mock()
    setattr(screen, action_method, action)

    getattr(screen_type, prompt_method)(screen, Ware.WATER)

    action.assert_not_called()