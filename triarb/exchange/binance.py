import ccxt.async_support as ccxt
from typing import List, Dict, Any

from .base import ExchangeAdapter
from ..config import settings


class BinanceAdapter(ExchangeAdapter):
    def __init__(self):
        self.exchange = ccxt.binance({
            'apiKey': settings.BINANCE_API_KEY,
            'secret': settings.BINANCE_API_SECRET,
            'options': {
                'defaultType': 'spot',
            },
        })
        if settings.PAPER_MODE:
            self.exchange.set_sandbox_mode(True)

    async def get_symbols(self) -> List[str]:
        markets = await self.exchange.load_markets()
        return list(markets.keys())

    async def get_ws_url(self) -> str:
        return self.exchange.urls['api']['ws']['spot']

    def get_l2_channel_name(self) -> str:
        return 'depth'

    def normalize_symbol(self, symbol: str) -> str:
        return symbol.replace('/', '')

    def denormalize_symbol(self, symbol: str) -> str:
        # This is a bit of a simplification. A more robust solution
        # would use the market data from ccxt to find the correct base/quote.
        if symbol.endswith(settings.QUOTE):
            base = symbol[:-len(settings.QUOTE)]
            return f'{base}/{settings.QUOTE}'
        # This is a guess for non-quote pairs, needs improvement
        for base in settings.TRI_SYMBOLS:
            if symbol.startswith(base):
                quote = symbol[len(base):]
                return f'{base}/{quote}'
        return symbol # fallback

    async def place_order(self, symbol: str, side: str, order_type: str, amount: float, price: float | None = None) -> Dict[str, Any]:
        return await self.exchange.create_order(symbol, order_type, side, amount, price)

    async def fetch_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        return await self.exchange.fetch_order(order_id, symbol)

    async def cancel_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        return await self.exchange.cancel_order(order_id, symbol)

    async def fetch_balance(self) -> Dict[str, Any]:
        return await self.exchange.fetch_balance()

    async def close(self):
        await self.exchange.close()
