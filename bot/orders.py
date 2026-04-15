# Utility file for order logic
from bot.client import BinanceClientWrapper
from bot.validators import validate_input, format_order_response
from bot.logging_config import logger

def place_order(symbol, side, order_type, quantity, price=None):
    """
    Main logic for placing an order.
    """
    try:
        # Validate Input
        validate_input(symbol, side, order_type, quantity, price)
        
        logger.info(f"Initializing order: {side} {quantity} {symbol} ({order_type})")
        
        # Initialize Client
        client = BinanceClientWrapper()
        
        # Place the order
        response = client.place_futures_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        # Process and return summary
        summary = format_order_response(response, logger)
        return summary
    except Exception as e:
        logger.error(f"Error in order placement logic: {str(e)}")
        raise
