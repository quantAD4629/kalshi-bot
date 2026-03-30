"""Kalshi API integration layer and market parsing."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class MarketSnapshot:
    """Typed model representing a Kalshi market snapshot."""

    ticker: str
    title: str
    yes_ask: Optional[float]
    no_ask: Optional[float]
    volume: int
    open_interest: int
    status: str
    close_time: Optional[str]


class KalshiManager:
    """Single integration layer for the Kalshi REST API."""

    BASE_URL = "https://trading-api.kalshi.com/trade-api/v2"

    def __init__(self) -> None:
        self.key_id = os.environ.get("KALSHI_KEY_ID", "")
        self.private_key_path = os.environ.get(
            "KALSHI_PRIVATE_KEY_PATH", "kalshi_key.pem"
        )
        self._validate_config()
        self._session = self._build_session()

    # ------------------------------------------------------------------
    # Config validation
    # ------------------------------------------------------------------

    def _validate_config(self) -> None:
        errors = []
        if not self.key_id:
            errors.append("KALSHI_KEY_ID is not set")
        if not os.path.exists(self.private_key_path):
            errors.append(
                f"Private key file not found: {self.private_key_path}"
            )
        if errors:
            raise EnvironmentError(
                "Kalshi configuration errors:\n" + "\n".join(f"  - {e}" for e in errors)
            )

    # ------------------------------------------------------------------
    # HTTP session with RSA signature auth
    # ------------------------------------------------------------------

    def _build_session(self):  # type: ignore[return]
        """Build a requests.Session pre-loaded with the RSA signing adapter."""
        try:
            import requests
            from cryptography.hazmat.primitives.serialization import (
                load_pem_private_key,
            )
        except ImportError as exc:
            raise ImportError(
                "Required packages missing. Run: pip install -r requirements.txt"
            ) from exc

        with open(self.private_key_path, "rb") as fh:
            private_key = load_pem_private_key(fh.read(), password=None)

        session = requests.Session()
        session.headers.update({"Content-Type": "application/json"})

        # Attach a custom auth handler that signs each request.
        session.auth = _RsaAuth(self.key_id, private_key)
        return session

    # ------------------------------------------------------------------
    # Market helpers
    # ------------------------------------------------------------------

    def get_active_btc_15m_markets(self) -> list[MarketSnapshot]:
        """Return all active 15-minute BTC markets."""
        params = {
            "status": "open",
            "series_ticker": "KXBTC",
        }
        resp = self._session.get(f"{self.BASE_URL}/markets", params=params)
        resp.raise_for_status()
        data = resp.json()
        markets = data.get("markets", [])
        return [
            self._parse_market(m)
            for m in markets
            if "15" in m.get("ticker", "")
        ]

    def _parse_market(self, raw: dict) -> MarketSnapshot:
        return MarketSnapshot(
            ticker=raw.get("ticker", ""),
            title=raw.get("title", ""),
            yes_ask=raw.get("yes_ask"),
            no_ask=raw.get("no_ask"),
            volume=raw.get("volume", 0),
            open_interest=raw.get("open_interest", 0),
            status=raw.get("status", ""),
            close_time=raw.get("close_time"),
        )


# ---------------------------------------------------------------------------
# Internal RSA auth adapter
# ---------------------------------------------------------------------------

class _RsaAuth:
    """requests-compatible auth callable that signs requests with RSA-PSS."""

    def __init__(self, key_id: str, private_key) -> None:
        self._key_id = key_id
        self._private_key = private_key

    def __call__(self, r):  # type: ignore[override]
        import base64
        import time

        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding

        ts_ms = str(int(time.time() * 1000))
        path = r.path_url
        method = r.method.upper()
        msg = f"{ts_ms}{method}{path}".encode()

        signature = self._private_key.sign(
            msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.DIGEST_SIZE,
            ),
            hashes.SHA256(),
        )
        r.headers.update(
            {
                "KALSHI-ACCESS-KEY": self._key_id,
                "KALSHI-ACCESS-TIMESTAMP": ts_ms,
                "KALSHI-ACCESS-SIGNATURE": base64.b64encode(signature).decode(),
            }
        )
        return r
