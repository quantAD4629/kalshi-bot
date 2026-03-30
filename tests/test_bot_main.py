"""Unit tests for bot_main formatting helpers."""

from bot_main import format_snapshot
from kalshi_manager import MarketSnapshot


def _make_snap(**kwargs) -> MarketSnapshot:
    defaults = dict(
        ticker="KXBTC-15M",
        title="BTC 15-min",
        yes_ask=55.0,
        no_ask=45.0,
        volume=200,
        open_interest=80,
        status="open",
        close_time=None,
    )
    defaults.update(kwargs)
    return MarketSnapshot(**defaults)


def test_format_snapshot_basic():
    snap = _make_snap()
    result = format_snapshot(snap)
    assert "KXBTC-15M" in result
    assert "55¢" in result
    assert "45¢" in result
    assert "Vol: 200" in result


def test_format_snapshot_none_prices():
    snap = _make_snap(yes_ask=None, no_ask=None)
    result = format_snapshot(snap)
    assert "N/A" in result
