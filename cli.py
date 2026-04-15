import argparse
import sys
from bot.client import BinanceClientWrapper
from bot.validators import validate_input, format_order_response
from bot.logging_config import logger
from tabulate import tabulate

def parse_args():
    parser = argparse.ArgumentParser(description="Primetrade AI Trading Bot (Binance Testnet)")
    parser.add_argument("--market", type=str, choices=['SPOT', 'FUTURES'], default='FUTURES', help="Market type (default: FUTURES)")
    parser.add_argument("--symbol", type=str, required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, choices=['BUY', 'SELL'], required=True, help="Order side")
    parser.add_argument("--type", type=str, choices=['MARKET', 'LIMIT'], required=True, help="Order type")
    parser.add_argument("--quantity", type=float, required=True, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price (required for LIMIT orders)")
    return parser.parse_args()

def main():
    args = parse_args()

    # Validate Input
    try:
        validate_input(args.symbol, args.side, args.type, args.quantity, args.price)
    except ValueError as e:
        logger.error(f"Input Validation Error: {e}")
        sys.exit(1)

    # Place Order
    try:
        # Load Client Wrapper (which will use .env automatically)
        client = BinanceClientWrapper()
        
        # Place the order based on market type
        if args.market.upper() == 'SPOT':
            response = client.place_spot_order(
                symbol=args.symbol,
                side=args.side,
                order_type=args.type,
                quantity=args.quantity,
                price=args.price
            )
            market_name = "Binance Spot Testnet"
        else:
            response = client.place_futures_order(
                symbol=args.symbol,
                side=args.side,
                order_type=args.type,
                quantity=args.quantity,
                price=args.price
            )
            market_name = "Binance Futures Testnet"

        # Process and display response
        summary = format_order_response(response, logger)
        
        # Display using tabulate for clean output
        print("\n=== Order Confirmation ===")
        print(tabulate(summary.items(), headers=['Field', 'Value'], tablefmt='pretty'))
        print(f"\nSuccess: Order placed successfully on {market_name}.\n")

    except Exception as e:
        logger.error(f"Execution Error: {str(e)}")
        print(f"\nError: {str(e)}\nCheck bot.log for full details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
