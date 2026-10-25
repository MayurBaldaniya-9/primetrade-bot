import argparse
import sys

from tabulate import tabulate

from bot.logging_config import logger
from bot.orders import place_order_for_market


def parse_args():
    parser = argparse.ArgumentParser(description="Primetrade AI Trading Bot (Binance Testnet)")
    parser.add_argument("--market", type=str, choices=["SPOT", "FUTURES"], default="FUTURES", help="Market type (default: FUTURES)")
    parser.add_argument("--symbol", type=str, required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, choices=["BUY", "SELL"], required=True, help="Order side")
    parser.add_argument("--type", type=str, choices=["MARKET", "LIMIT"], required=True, help="Order type")
    parser.add_argument("--quantity", type=float, required=True, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price (required for LIMIT orders)")
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        summary = place_order_for_market(
            market=args.market,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
        )

        print("\n=== Order Confirmation ===")
        print(tabulate(summary.items(), headers=["Field", "Value"], tablefmt="pretty"))
        print(f"\nSuccess: Order placed successfully on Binance {args.market.title()} Testnet.\n")
    except ValueError as exc:
        logger.error(f"Input Validation Error: {exc}")
        print(f"\nError: {str(exc)}\nCheck bot.log for full details.")
        sys.exit(1)
    except Exception as exc:
        logger.error(f"Execution Error: {str(exc)}")
        print(f"\nError: {str(exc)}\nCheck bot.log for full details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
