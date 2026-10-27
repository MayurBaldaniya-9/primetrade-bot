# Primetrade Trading Bot

A Binance Testnet trading bot with:
- Python backend API + CLI
- React frontend for order placement

## Backend setup

1. Create virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create `.env` from `.env.example` and set Binance credentials.

## Run backend API

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Available endpoints:
- `GET /health`
- `POST /api/orders`

Example payload:
```json
{
  "market": "FUTURES",
  "symbol": "BTCUSDT",
  "side": "BUY",
  "type": "MARKET",
  "quantity": 0.001
}
```

## Run CLI (still supported)

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

## Frontend setup

1. Configure API base URL:
   ```bash
   cp frontend/.env.example frontend/.env
   ```
2. Install and run:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

Frontend defaults to `VITE_API_BASE_URL=http://localhost:8000`.

## Tests

Backend tests:
```bash
python -m unittest tests_validators.py tests_api.py
```

Frontend tests:
```bash
cd frontend
npm run test
```

## Optional Docker Compose

```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## Security note

Never expose Binance API keys in frontend code. Keys stay only in backend `.env`.
