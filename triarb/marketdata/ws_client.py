import asyncio
import json
from typing import List

import websockets
from loguru import logger

from ..exchange.base import ExchangeAdapter


class WebSocketClient:
    def __init__(self, exchange: ExchangeAdapter, symbols: List[str], channel: str):
        self.exchange = exchange
        self.symbols = symbols
        self.channel = channel
        self.ws_url = ""
        self.connection = None
        self.queue = asyncio.Queue()

    async def connect(self):
        self.ws_url = await self.exchange.get_ws_url()
        streams = [f"{self.exchange.normalize_symbol(s).lower()}@depth5" for s in self.symbols]
        full_url = f"{self.ws_url}/stream?streams={'/'.join(streams)}"
        logger.info(f"Connecting to WebSocket: {full_url}")
        self.connection = await websockets.connect(full_url)

    async def subscribe(self):
        # Subscription is handled in the connection URL for Binance
        pass

    async def run(self):
        await self.connect()
        while True:
            try:
                message = await self.connection.recv()
                data = json.loads(message)
                await self.queue.put(data)
            except websockets.exceptions.ConnectionClosed as e:
                logger.warning(f"WebSocket connection closed: {e}. Reconnecting...")
                await asyncio.sleep(5)
                await self.connect()
            except Exception as e:
                logger.error(f"Error in WebSocket client: {e}")
                # Consider more robust error handling and reconnection logic here

    def get_queue(self) -> asyncio.Queue:
        return self.queue
