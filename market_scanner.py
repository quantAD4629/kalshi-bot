"""One-shot utility scanner for Kalshi BTC 15-minute markets."""

from kalshi_manager import KalshiManager


def scan() -> None:
    manager = KalshiManager()
    markets = manager.get_active_btc_15m_markets()
    if not markets:
        print("No active 15-min BTC markets found.")
        return
    print(f"Found {len(markets)} active 15-min BTC market(s):\n")
    for snap in markets:
        print(f"  Ticker   : {snap.ticker}")
        print(f"  Title    : {snap.title}")
        print(f"  Yes ask  : {snap.yes_ask}")
        print(f"  No ask   : {snap.no_ask}")
        print(f"  Volume   : {snap.volume}")
        print(f"  OI       : {snap.open_interest}")
        print(f"  Status   : {snap.status}")
        print(f"  Closes   : {snap.close_time}")
        print()


if __name__ == "__main__":
    scan()
