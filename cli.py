import sys
import click

from bot.client import BinanceClient, BinanceClientError
from bot.logging_config import setup_logging
from bot.orders import place_order
from bot.validators import validate_all
from bot.ai_signal import get_signal

# Initialise logging before anything else
# File captures DEBUG+, console shows WARNING+ (clean terminal)
setup_logging(console_level="WARNING")


# ── Shared client builder ─────────────────────────────────────────────────────

def _get_client() -> BinanceClient:
    try:
        return BinanceClient()
    except BinanceClientError as e:
        click.echo(f"\n❌ Configuration Error:\n   {e}\n", err=True)
        sys.exit(1)


# ── place command ─────────────────────────────────────────────────────────────

@click.group()
def cli():
    """Binance Futures Testnet Trading Bot."""
    pass


@cli.command()
@click.option("--symbol",      required=True,  help="Trading pair, e.g. BTCUSDT")
@click.option("--side",        required=True,  type=click.Choice(["BUY", "SELL"], case_sensitive=False),
              help="Order side")
@click.option("--order-type",  "order_type",   required=True,
              type=click.Choice(["MARKET", "LIMIT", "STOP_MARKET"], case_sensitive=False),
              help="Order type")
@click.option("--quantity",    required=True,  type=float, help="Order quantity")
@click.option("--price",       default=None,   type=float, help="Limit price (LIMIT orders only)")
@click.option("--stop-price",  "stop_price",   default=None, type=float,
              help="Stop trigger price (STOP_MARKET orders only)")
@click.option("--tif",         default="GTC",
              type=click.Choice(["GTC", "IOC", "FOK"], case_sensitive=False),
              help="Time-in-force for LIMIT orders (default: GTC)")
@click.option("--use-ai",      "use_ai",       is_flag=True, default=False,
              help="Fetch RSI signal and optionally override --side")
def place(symbol, side, order_type, quantity, price, stop_price, tif, use_ai):
    """Place a MARKET, LIMIT, or STOP_MARKET futures order."""

    # ── Validate inputs ───────────────────────────────────────────────────────
    try:
        params = validate_all(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
            tif=tif,
        )
    except ValueError as e:
        click.echo(f"\n❌ Validation Error: {e}\n", err=True)
        sys.exit(1)

    # ── AI signal (optional) ──────────────────────────────────────────────────
    if use_ai:
        binance = _get_client()
        click.echo("\n🔍 Fetching market data for AI signal...")
        try:
            klines = binance.get_klines(params["symbol"], limit=100)
            prices = [float(k[4]) for k in klines]
            signal = get_signal(prices)
        except Exception as e:
            click.echo(f"⚠️  AI signal failed ({e}), using your original --side.", err=True)
            signal = "HOLD"

        click.echo(f"🤖 AI Signal (RSI): {signal}")

        if signal == "HOLD":
            click.echo("⚠️  Signal is HOLD — no trade will be executed.")
            sys.exit(0)

        if signal != params["side"]:
            click.echo(
                f"\n⚠️  AI Signal ({signal}) differs from your input ({params['side']})."
            )
            if click.confirm("Override your --side with the AI signal?", default=False):
                params["side"] = signal
                click.echo(f"⚡ Side overridden → {params['side']}")
            else:
                click.echo(f"✔  Keeping your original side: {params['side']}")
        else:
            click.echo(f"✔  AI Signal agrees with your input: {params['side']}")

    # ── Print request summary ─────────────────────────────────────────────────
    sep = "─" * 55
    click.echo(f"\n{sep}")
    click.echo("  ORDER REQUEST SUMMARY")
    click.echo(sep)
    click.echo(f"  Symbol      : {params['symbol']}")
    click.echo(f"  Side        : {params['side']}")
    click.echo(f"  Type        : {params['order_type']}")
    click.echo(f"  Quantity    : {params['quantity']}")
    if params.get("price"):
        click.echo(f"  Price       : {params['price']}")
    if params.get("stop_price"):
        click.echo(f"  Stop Price  : {params['stop_price']}")
    if params["order_type"] == "LIMIT":
        click.echo(f"  TIF         : {params['tif']}")
    click.echo(sep)

    # ── Place order ───────────────────────────────────────────────────────────
    if not use_ai:
        binance = _get_client()

    result = place_order(
        binance,
        symbol=params["symbol"],
        side=params["side"],
        order_type=params["order_type"],
        quantity=params["quantity"],
        price=params["price"],
        stop_price=params["stop_price"],
        time_in_force=params["tif"],
    )

    result.print_summary()

    if not result.success:
        sys.exit(1)


# ── account command ───────────────────────────────────────────────────────────

@cli.command()
def account():
    """Show Futures Testnet account balances."""
    binance = _get_client()
    try:
        data = binance.get_account()
    except Exception as e:
        click.echo(f"\n❌ Error fetching account: {e}\n", err=True)
        sys.exit(1)

    assets = data.get("assets", [])
    sep = "─" * 55
    click.echo(f"\n{sep}")
    click.echo("  ACCOUNT BALANCES (non-zero)")
    click.echo(sep)
    printed = 0
    for asset in assets:
        balance = float(asset.get("walletBalance", 0))
        if balance > 0:
            click.echo(
                f"  {asset['asset']:<10} "
                f"wallet={balance:.4f}  "
                f"available={asset.get('availableBalance', 'N/A')}"
            )
            printed += 1
    if printed == 0:
        click.echo("  No funded assets found.")
        click.echo("  → Go to https://testnet.binancefuture.com and click 'Get' to add test USDT.")
    click.echo(sep)


# ── open-orders command ───────────────────────────────────────────────────────

@cli.command("open-orders")
@click.option("--symbol", default=None, help="Filter by symbol, e.g. BTCUSDT")
def open_orders(symbol):
    """List all open futures orders."""
    binance = _get_client()
    try:
        orders = binance.get_open_orders(symbol=symbol)
    except Exception as e:
        click.echo(f"\n❌ Error fetching open orders: {e}\n", err=True)
        sys.exit(1)

    sep = "─" * 55
    label = f"OPEN ORDERS{' — ' + symbol if symbol else ''}"
    click.echo(f"\n{sep}")
    click.echo(f"  {label}")
    click.echo(sep)
    if not orders:
        click.echo("  No open orders.")
    for o in orders:
        click.echo(
            f"  [{o['orderId']}] {o['symbol']} {o['side']} {o['type']} "
            f"qty={o['origQty']} price={o.get('price', 'N/A')} status={o['status']}"
        )
    click.echo(sep)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli()
