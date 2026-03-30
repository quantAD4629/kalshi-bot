"""Unit tests for kalshi_manager module."""

from kalshi_manager import MarketSnapshot


def test_market_snapshot_fields():
    snap = MarketSnapshot(
        ticker="KXBTC-15M",
        title="BTC 15-min",
        yes_ask=55.0,
        no_ask=45.0,
        volume=100,
        open_interest=50,
        status="open",
        close_time="2024-01-01T00:15:00Z",
    )
    assert snap.ticker == "KXBTC-15M"
    assert snap.yes_ask == 55.0
    assert snap.no_ask == 45.0
    assert snap.volume == 100
    assert snap.status == "open"


def test_market_snapshot_optional_fields():
    snap = MarketSnapshot(
        ticker="KXBTC-15M",
        title="BTC 15-min",
        yes_ask=None,
        no_ask=None,
        volume=0,
        open_interest=0,
        status="closed",
        close_time=None,
    )
    assert snap.yes_ask is None
    assert snap.no_ask is None
    assert snap.close_time is None
