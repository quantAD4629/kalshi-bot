"""Runtime entrypoint for the Kalshi BTC 15-minute market bot."""

import time

from kalshi_manager import KalshiManager, MarketSnapshot

POLL_INTERVAL_SECONDS = 15


def format_snapshot(snap: MarketSnapshot) -> str:
    yes = f"{snap.yes_ask:.0f}¢" if snap.yes_ask is not None else "N/A"
    no = f"{snap.no_ask:.0f}¢" if snap.no_ask is not None else "N/A"
    return (
        f"[{snap.ticker}] {snap.title} | "
        f"Yes: {yes}  No: {no} | "
        f"Vol: {snap.volume}  OI: {snap.open_interest} | "
        f"Status: {snap.status}"
    )


def run_loop(manager: KalshiManager) -> None:
    print("Kalshi BTC 15-min bot started. Press Ctrl+C to stop.\n")
    while True:
        try:
            markets = manager.get_active_btc_15m_markets()
            if not markets:
                print("No active 15-min BTC markets found.")
            for snap in markets:
                print(format_snapshot(snap))
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001
            # Keep the loop alive through transient API/network errors.
            print(f"[ERROR] {exc}")
        time.sleep(POLL_INTERVAL_SECONDS)


def main() -> None:
    manager = KalshiManager()
    run_loop(manager)


if __name__ == "__main__":
    main()
