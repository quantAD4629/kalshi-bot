"""Binance websocket feed for live BTC price updates."""

import json
import threading
from typing import Callable, Optional

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"


class PriceEngine:
    """Subscribe to Binance trade stream and push BTC price updates to a callback."""

    def __init__(self, on_price: Callable[[float], None]) -> None:
        self._on_price = on_price
        self._thread: Optional[threading.Thread] = None
        self._running = False

    def start(self) -> None:
        """Start the websocket listener in a background thread."""
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Signal the listener to stop."""
        self._running = False

    def _run(self) -> None:
        try:
            import websocket  # type: ignore[import]
        except ImportError as exc:
            raise ImportError(
                "websocket-client is required. Run: pip install -r requirements.txt"
            ) from exc

        def on_message(ws, message: str) -> None:
            if not self._running:
                ws.close()
                return
            try:
                data = json.loads(message)
                price = float(data["p"])
                self._on_price(price)
            except (KeyError, ValueError):
                pass

        def on_error(ws, error) -> None:
            print(f"[PriceEngine] WebSocket error: {error}")

        def on_close(ws, close_status_code, close_msg) -> None:
            pass

        ws_app = websocket.WebSocketApp(
            BINANCE_WS_URL,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )
        ws_app.run_forever()
