from bot.logging_config import logger
from bot.service import place_order


def place_order_for_market(market, symbol, side, order_type, quantity, price=None):
    """Main order placement logic for CLI and API usage."""
    try:
        logger.info(f"Initializing order: {side} {quantity} {symbol} ({order_type})")
        return place_order(
            market=market,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
    except Exception as exc:
        logger.error(f"Error in order placement logic: {str(exc)}")
        raise
