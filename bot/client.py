
import logging
import os
from typing import List, Dict, Any

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
    """

    def __init__(self):
        api_key = os.getenv("API_KEY", "").strip()
        api_secret = os.getenv("API_SECRET", "").strip()

        if not api_key or not api_secret:
            raise BinanceClientError(
                "API_KEY and API_SECRET must be set in your .env file.\n"
                "Example:\n"
                "API_KEY=your_testnet_api_key\n"
                "API_SECRET=your_testnet_api_secret\n"
                "Register at: https://testnet.binancefuture.com"
            )

        self._client = Client(api_key, api_secret, testnet=True)
        logger.info("BinanceClient initialised — testnet=True")

    # ── Market data ─────────────────────────────────────────

    def get_klines(
        self, symbol: str, interval: str = "1m", limit: int = 100
    ) -> List[List[Any]]:
        logger.info(
            "Fetching klines — symbol=%s interval=%s limit=%s",
            symbol,
            interval,
            limit,
        )
        try:
            klines = self._client.futures_klines(
                symbol=symbol, interval=interval, limit=limit
            )
            return klines
        except BinanceAPIException as e:
            logger.error("Klines API error — code=%s msg=%s", e.code, e.message)
            raise
        except BinanceRequestException as e:
            logger.error("Klines network error — %s", e)
            raise

    # ── Order placement ─────────────────────────────────────

    def create_order(self, **kwargs) -> Dict[str, Any]:
        logger.info("Placing order — params=%s", kwargs)

        try:
            response = self._client.futures_create_order(**kwargs)
            return response
        except BinanceAPIException as e:
            logger.error("Order API error — code=%s msg=%s", e.code, e.message)
            raise
        except BinanceRequestException as e:
            logger.error("Order network error — %s", e)
            raise

    # ── Account info ───────────────────────────────────────

    def get_account(self) -> Dict[str, Any]:
        logger.info("Fetching account info")
        try:
            return self._client.futures_account()
        except BinanceAPIException as e:
            logger.error("Account API error — code=%s msg=%s", e.code, e.message)
            raise

    def get_open_orders(self, symbol: str | None = None) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {}

        if symbol:
            params["symbol"] = symbol

        logger.info("Fetching open orders — symbol=%s", symbol or "ALL")

        try:
            return self._client.futures_get_open_orders(**params)
        except BinanceAPIException as e:
            logger.error("Open orders API error — code=%s msg=%s", e.code, e.message)
            raise
