# Kalshi Bot

Small Python bot that scans Kalshi for the currently active 15-minute BTC market and prints updates in a continuous loop.

## Architecture

| File | Role |
|------|------|
| `bot_main.py` | Runtime entrypoint. Owns loop cadence and output. |
| `kalshi_manager.py` | Single Kalshi API integration layer and market parsing. |
| `market_scanner.py` | Utility scanner that reuses `KalshiManager`. |
| `price_engine.py` | Binance websocket feed for live BTC price updates. |

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```env
KALSHI_KEY_ID=your_kalshi_key_id
KALSHI_PRIVATE_KEY_PATH=kalshi_key.pem
```

## Run

```bash
python bot_main.py
```

For a one-shot market scan:

```bash
python market_scanner.py
```

## Notes

- The private key and `.env` are ignored via `.gitignore` and must not be committed.
- `market_scanner.py` can be run directly for one-shot market visibility.
- `price_engine.py` connects to the Binance public trade stream; no API key is required.

## CI

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request:

- Installs dependencies
- Lints with `flake8`
- Runs tests with `pytest`