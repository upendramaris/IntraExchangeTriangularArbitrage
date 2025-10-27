import asyncio
from typing import Dict

from loguru import logger

from .ws_client import WebSocketClient
from .orderbook import OrderBook
from ..exchange.base import ExchangeAdapter


class MarketDataAggregator:
    def __init__(self, exchange: ExchangeAdapter, symbols: list[str]):
        self.exchange = exchange
        self.symbols = symbols
        self.order_books: Dict[str, OrderBook] = {s: OrderBook(s) for s in symbols}
        self.ws_client = WebSocketClient(exchange, symbols, exchange.get_l2_channel_name())
        self.queue = self.ws_client.get_queue()

    async def run(self):
        asyncio.create_task(self.ws_client.run())
        while True:
            try:
                message = await self.queue.get()
                self._process_message(message)
            except Exception as e:
                logger.error(f"Error processing message from queue: {e}")

    def _process_message(self, message: dict):
        # This needs to be adapted to the specific format of the exchange's WebSocket message
        # For Binance stream like <symbol>@depth<levels>, the structure is different.
        # Example for binance: {"stream":"<symbol>@depth<levels>","data":{...}}
        stream = message.get('stream')
        if not stream:
            return

        symbol_norm = stream.split('@')[0]
        symbol = self.exchange.denormalize_symbol(symbol_norm.upper())

        if symbol in self.order_books:
            data = message.get('data', {})
            bids = [(float(p), float(q)) for p, q in data.get('bids', [])]
            asks = [(float(p), float(q)) for p, q in data.get('asks', [])]
            self.order_books[symbol].update_bids(bids)
            self.order_books[symbol].update_asks(asks)
            # logger.debug(f"Updated order book for {symbol}")

    def get_order_book(self, symbol: str) -> OrderBook | None:
        return self.order_books.get(symbol)
