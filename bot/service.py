from bot.client import BinanceClientWrapper
from bot.validators import format_order_response, validate_input


def place_order(market, symbol, side, order_type, quantity, price=None, client=None):
    market_name = market.upper()
    if market_name not in ["SPOT", "FUTURES"]:
        raise ValueError("Market must be SPOT or FUTURES")

    validate_input(symbol, side, order_type, quantity, price)

    trading_client = client or BinanceClientWrapper()

    if market_name == "SPOT":
        response = trading_client.place_spot_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
    else:
        response = trading_client.place_futures_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

    return format_order_response(response)
