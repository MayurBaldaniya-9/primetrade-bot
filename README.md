# Primetrade Trading Bot

A simplified Python trading bot for Binance Futures Testnet (USDT-M).

## Setup instructions

1. **Clone the repository** (or navigate to the folder)
2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   Create a `.env` file in the root directory with your Binance Testnet credentials:
   ```env
   BINANCE_API_KEY=your_testnet_api_key
   BINANCE_SECRET_KEY=your_testnet_api_secret
   BINANCE_TESTNET=true
   ```

## Usage

Run the bot using the CLI:

### Quick Start Examples
Run a **MARKET BUY** order:
```powershell
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Run a **LIMIT SELL** order:
```powershell
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 90000
```


### Place a Market Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a Spot Market Order
```bash
python cli.py --market SPOT --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a Limit Order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 60000
```

## Features
- Market and Limit orders on USDT-M Futures and Spot Testnets
- Automatic Server Time Synchronization (fixes timestamp errors)
- Input validation
- Structured logging to `bot.log`
- Robust error handling
- Structured logging to `bot.log`
- Robust error handling
- Deployment-ready with Docker support
