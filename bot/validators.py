from bot.logging_config import logger

def validate_input(symbol, side, order_type, quantity, price=None):
    """
    Validate CLI user input
    """
    if not symbol:
        raise ValueError("Symbol is required")
    
    if side.upper() not in ['BUY', 'SELL']:
        raise ValueError("Side must be BUY or SELL")

    if order_type.upper() not in ['MARKET', 'LIMIT']:
        raise ValueError("Order Type must be MARKET or LIMIT")

    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero")
    except (ValueError, TypeError):
        raise ValueError("Quantity must be a valid number")

    if order_type.upper() == 'LIMIT':
        if not price:
            raise ValueError("Price is required for LIMIT orders")
        try:
            p = float(price)
            if p <= 0:
                raise ValueError("Price must be greater than zero")
        except (ValueError, TypeError):
            raise ValueError("Price must be a valid number")

    return True

def format_order_response(response, logger_obj=None):
    """
    Extract and format relevant information from order response
    """
    summary = {
        'orderId': response.get('orderId'),
        'status': response.get('status'),
        'symbol': response.get('symbol'),
        'type': response.get('type'),
        'side': response.get('side'),
        'origQty': response.get('origQty'),
        'executedQty': response.get('executedQty'),
        'avgPrice': response.get('avgPrice', 'N/A')
    }
    
    if logger_obj:
        logger_obj.info(f"Order Successful: {summary['orderId']} (Status: {summary['status']})")
        
    return summary
