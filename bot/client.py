"""
client.py — Binance Futures Testnet client wrapper.

Wraps python-binance to provide:
  - Safe credential loading from .env
  - Testnet configuration
  - Kline fetching
  - Order placement
  - Structured logging throughout
"""

import logging
import os

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class BinanceClientError(Exception):
    """Raised for configuration or credential errors."""


class BinanceClient:
    """
    Wrapper around python-binance Client for Futures Testnet.

    Credentials are loaded from environment variables:
        API_KEY     — Binance Futures Testnet API key
        API_SECRET  — Binance Futures Testnet API secret
    """

    def __init__(self):
        api_key = os.getenv("API_KEY", "").strip()
        api_secret = os.getenv("API_SECRET", "").strip()

        if not api_key or not api_secret:
            raise BinanceClientError(
                "API_KEY and API_SECRET must be set in your .env file.\n"
                "  Example:\n"
                "    API_KEY=your_testnet_api_key\n"
                "    API_SECRET=your_testnet_api_secret\n"
                "  Register at: https://testnet.binancefuture.com"
            )

        # testnet=True automatically routes to testnet.binancefuture.com
        self._client = Client(api_key, api_secret, testnet=True)
        logger.info("BinanceClient initialised — testnet=True")

    # ── Market data ────────────────────────────────────────────────────────────

    def get_klines(self, symbol: str, interval: str = "1m", limit: int = 100) -> list:
        """
        Fetch OHLCV candlestick data for a symbol.

        Args:
            symbol:   Trading pair, e.g. "BTCUSDT"
            interval: Candlestick interval, e.g. "1m", "5m", "1h"
            limit:    Number of candles to fetch (default 100)

        Returns:
            List of kline arrays from Binance
        """
        logger.info("Fetching klines — symbol=%s interval=%s limit=%s", symbol, interval, limit)
        try:
            klines = self._client.futures_klines(
                symbol=symbol, interval=interval, limit=limit
            )
            logger.debug("Klines received — count=%d", len(klines))
            return klines
        except BinanceAPIException as e:
            logger.error("Klines API error — code=%s msg=%s", e.code, e.message)
            raise
        except BinanceRequestException as e:
            logger.error("Klines network error — %s", e)
            raise

    # ── Order placement ────────────────────────────────────────────────────────

    def create_order(self, **kwargs) -> dict:
        """
        Place a futures order.

        Accepts all standard Binance futures_create_order parameters.
        Keeps the raw client private — callers use this method only.

        Returns:
            Raw Binance API order response dict

        Raises:
            BinanceAPIException: on API-level errors (e.g. insufficient margin)
            BinanceRequestException: on network failures
        """
        # Log request without exposing sensitive data
        loggable = {k: v for k, v in kwargs.items()}
        logger.info("Placing order — params=%s", loggable)

        try:
            response = self._client.futures_create_order(**kwargs)
            logger.info(
                "Order accepted — orderId=%s status=%s executedQty=%s avgPrice=%s",
                response.get("orderId"),
                response.get("status"),
                response.get("executedQty"),
                response.get("avgPrice"),
            )
            return response

        except BinanceAPIException as e:
            logger.error("Order API error — code=%s msg=%s", e.code, e.message)
            raise
        except BinanceRequestException as e:
            logger.error("Order network error — %s", e)
            raise

    # ── Account info ───────────────────────────────────────────────────────────

    def get_account(self) -> dict:
        """Fetch futures account details including balances and positions."""
        logger.info("Fetching account info")
        try:
            return self._client.futures_account()
        except BinanceAPIException as e:
            logger.error("Account API error — code=%s msg=%s", e.code, e.message)
            raise

    def get_open_orders(self, symbol: str = None) -> list:
        """
        Fetch open orders, optionally filtered by symbol.

        Args:
            symbol: Optional trading pair filter, e.g. "BTCUSDT"
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        logger.info("Fetching open orders — symbol=%s", symbol or "ALL")
        try:
            return self._client.futures_get_open_orders(**params)
        except BinanceAPIException as e:
            logger.error("Open orders API error — code=%s msg=%s", e.code, e.message)
            raise
