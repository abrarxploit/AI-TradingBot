import logging

logger = logging.getLogger(__name__)

def place_order(client, symbol, side, order_type, quantity, price=None):
    try:
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        logger.info(f"Placing order: {params}")

        response = client.futures_create_order(**params)

        logger.info(f"Order Response: {response}")
        return response

    except Exception as e:
        logger.error(f"Error placing order: {e}")
        raise