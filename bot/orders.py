"""
orders.py — Order placement logic.

Sits between the CLI and BinanceClient:
  - Builds the correct parameter set per order type
  - Returns a clean OrderResult dataclass
  - Logs the full request/response lifecycle
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger(__name__)


# ── Result dataclass ──────────────────────────────────────────────────────────

@dataclass
class OrderResult:
    """Typed, display-ready representation of an order outcome."""

    success: bool
    order_id: Optional[int] = None
    client_order_id: Optional[str] = None
    symbol: Optional[str] = None
    side: Optional[str] = None
    order_type: Optional[str] = None
    status: Optional[str] = None
    orig_qty: Optional[str] = None
    executed_qty: Optional[str] = None
    avg_price: Optional[str] = None
    price: Optional[str] = None
    stop_price: Optional[str] = None
    time_in_force: Optional[str] = None
    error_message: Optional[str] = None
    raw: dict = field(default_factory=dict)

    @classmethod
    def from_response(cls, data: dict) -> "OrderResult":
        """Build an OrderResult from a raw Binance API response."""
        return cls(
            success=True,
            order_id=data.get("orderId"),
            client_order_id=data.get("clientOrderId"),
            symbol=data.get("symbol"),
            side=data.get("side"),
            order_type=data.get("type"),
            status=data.get("status"),
            orig_qty=data.get("origQty"),
            executed_qty=data.get("executedQty"),
            avg_price=data.get("avgPrice") or data.get("price"),
            price=data.get("price"),
            stop_price=data.get("stopPrice"),
            time_in_force=data.get("timeInForce"),
            raw=data,
        )

    @classmethod
    def from_error(cls, message: str) -> "OrderResult":
        return cls(success=False, error_message=message)

    def print_summary(self) -> None:
        """Print a formatted order result to the terminal."""
        sep = "─" * 55
        if not self.success:
            print(f"\n{sep}")
            print(f"  ✗  ORDER FAILED")
            print(f"  {self.error_message}")
            print(sep)
            return

        print(f"\n{sep}")
        print(f"  ✓  ORDER PLACED SUCCESSFULLY")
        print(sep)
        print(f"  Order ID      : {self.order_id}")
        print(f"  Client OID    : {self.client_order_id}")
        print(f"  Symbol        : {self.symbol}")
        print(f"  Side          : {self.side}")
        print(f"  Type          : {self.order_type}")
        print(f"  Status        : {self.status}")
        print(f"  Orig Qty      : {self.orig_qty}")
        print(f"  Executed Qty  : {self.executed_qty}")
        print(f"  Avg Price     : {self.avg_price or 'N/A (pending fill)'}")
        if self.stop_price and self.stop_price != "0":
            print(f"  Stop Price    : {self.stop_price}")
        if self.time_in_force:
            print(f"  Time In Force : {self.time_in_force}")
        print(sep)


# ── Order placement ───────────────────────────────────────────────────────────

def place_order(
    binance_client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
    time_in_force: str = "GTC",
) -> OrderResult:
    """
    Place a futures order and return a structured OrderResult.

    Args:
        binance_client : BinanceClient instance
        symbol         : Trading pair, e.g. "BTCUSDT"
        side           : "BUY" or "SELL"
        order_type     : "MARKET", "LIMIT", or "STOP_MARKET"
        quantity       : Order quantity
        price          : Required for LIMIT orders
        stop_price     : Required for STOP_MARKET orders
        time_in_force  : "GTC" | "IOC" | "FOK" (LIMIT only, default GTC)

    Returns:
        OrderResult (success=True with details, or success=False with error_message)
    """
    params: dict = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        if price is None:
            return OrderResult.from_error("Price is required for LIMIT orders.")
        params["price"] = price
        params["timeInForce"] = time_in_force

    elif order_type == "STOP_MARKET":
        if stop_price is None:
            return OrderResult.from_error("stop_price is required for STOP_MARKET orders.")
        params["stopPrice"] = stop_price

    logger.info(
        "order_request | symbol=%s side=%s type=%s qty=%s price=%s stopPrice=%s",
        symbol, side, order_type, quantity, price, stop_price,
    )

    try:
        raw = binance_client.create_order(**params)
        result = OrderResult.from_response(raw)
        logger.info(
            "order_success | orderId=%s status=%s executedQty=%s avgPrice=%s",
            result.order_id, result.status, result.executed_qty, result.avg_price,
        )
        return result

    except BinanceAPIException as e:
        msg = f"Binance API error {e.code}: {e.message}"
        logger.error("order_failed | %s", msg)
        return OrderResult.from_error(msg)

    except BinanceRequestException as e:
        msg = f"Network error: {e}"
        logger.error("order_network_error | %s", msg)
        return OrderResult.from_error(msg)

    except Exception as e:
        logger.exception("order_unexpected_error | %s", e)
        return OrderResult.from_error(f"Unexpected error: {e}")
