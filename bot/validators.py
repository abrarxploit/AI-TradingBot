"""
validators.py — Input validation for all order parameters.

All validators raise ValueError with a clear, user-facing message on failure.
validate_all() is the single entry point used by the CLI.
"""

from __future__ import annotations

from typing import Optional

VALID_SIDES = ("BUY", "SELL")
VALID_ORDER_TYPES = ("MARKET", "LIMIT", "STOP_MARKET")
VALID_TIF = ("GTC", "IOC", "FOK")


def validate_symbol(symbol: str) -> str:
    """Normalise and validate trading symbol."""
    if not symbol:
        raise ValueError("Symbol cannot be empty. Example: BTCUSDT")
    symbol = symbol.strip().upper()
    if not symbol.isalnum():
        raise ValueError(
            f"Symbol '{symbol}' contains invalid characters. "
            "Use alphanumeric only, e.g. BTCUSDT"
        )
    return symbol


def validate_side(side: str) -> str:
    """Validate order side."""
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Side must be BUY or SELL, got '{side}'")
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type."""
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Order type must be one of {VALID_ORDER_TYPES}, got '{order_type}'"
        )
    return order_type


def validate_quantity(quantity) -> float:
    """Parse and validate order quantity."""
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(
            f"Quantity must be a positive number, got '{quantity}'"
        )
    if qty <= 0:
        raise ValueError(f"Quantity must be > 0, got {qty}")
    return qty


def validate_price(price, order_type: str) -> Optional[float]:
    """Validate price — required for LIMIT, not used for MARKET/STOP_MARKET."""
    if order_type in ("MARKET", "STOP_MARKET"):
        return None  # price not applicable

    if price is None:
        raise ValueError(f"--price is required for {order_type} orders")

    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValueError(f"Price must be a positive number, got '{price}'")

    if p <= 0:
        raise ValueError(f"Price must be > 0, got {p}")

    return p


def validate_stop_price(stop_price, order_type: str) -> Optional[float]:
    """Validate stop price — required for STOP_MARKET only."""
    if order_type != "STOP_MARKET":
        return None

    if stop_price is None:
        raise ValueError("--stop-price is required for STOP_MARKET orders")

    try:
        sp = float(stop_price)
    except (TypeError, ValueError):
        raise ValueError(f"Stop price must be a positive number, got '{stop_price}'")

    if sp <= 0:
        raise ValueError(f"Stop price must be > 0, got {sp}")

    return sp


def validate_tif(tif: str, order_type: str) -> str:
    """Validate time-in-force — only meaningful for LIMIT orders."""
    tif = tif.strip().upper()
    if order_type == "LIMIT" and tif not in VALID_TIF:
        raise ValueError(
            f"Time-in-force must be one of {VALID_TIF} for LIMIT orders, got '{tif}'"
        )
    return tif


def validate_all(
    *,
    symbol: str,
    side: str,
    order_type: str,
    quantity,
    price=None,
    stop_price=None,
    tif: str = "GTC",
) -> dict:
    """
    Run all validators and return a clean, typed parameter dict.
    Raises ValueError with a descriptive message on the first failure.

    Returns:
        dict with keys: symbol, side, order_type, quantity, price, stop_price, tif
    """
    v_symbol = validate_symbol(symbol)
    v_side = validate_side(side)
    v_type = validate_order_type(order_type)
    v_qty = validate_quantity(quantity)
    v_price = validate_price(price, v_type)
    v_stop = validate_stop_price(stop_price, v_type)
    v_tif = validate_tif(tif, v_type)

    return {
        "symbol": v_symbol,
        "side": v_side,
        "order_type": v_type,
        "quantity": v_qty,
        "price": v_price,
        "stop_price": v_stop,
        "tif": v_tif,
    }
