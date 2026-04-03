import click
from bot.client import BinanceClient
from bot.orders import place_order
from bot.validators import validate_input
from bot.logging_config import setup_logging
from bot.ai_signal import get_signal

setup_logging()

@click.command()
@click.option('--symbol', required=True)
@click.option('--side', required=True)
@click.option('--order_type', required=True)
@click.option('--quantity', required=True, type=float)
@click.option('--price', required=False, type=float)

def run(symbol, side, order_type, quantity, price):
    try:
        validate_input(symbol, side, order_type, quantity, price)

        # ✅ Create Binance object
        binance = BinanceClient()
        client = binance.get_client()

        # ✅ Fetch market data for AI
        klines = binance.get_klines(symbol)
        prices = [float(k[4]) for k in klines]

        # ✅ Get AI signal
        signal = get_signal(prices)
        print(f"\n🤖 AI Signal: {signal}")

        # ✅ Optional: Override side using AI
        if signal != "HOLD":
            side = signal
            print(f"⚡ Using AI Signal → New Side: {side}")
        else:
            print("⚠️ HOLD signal - no trade executed")
            return

        print("\n🔹 Order Request Summary")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Type: {order_type}")
        print(f"Quantity: {quantity}")
        if price:
            print(f"Price: {price}")

        response = place_order(
            client,
            symbol,
            side,
            order_type,
            quantity,
            price
        )

        print("\n✅ Order Placed Successfully!")
        print(f"Order ID: {response.get('orderId')}")
        print(f"Status: {response.get('status')}")
        print(f"Executed Qty: {response.get('executedQty')}")
        print(f"Avg Price: {response.get('avgPrice')}")

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    run()