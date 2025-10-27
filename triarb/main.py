import asyncio
import uvicorn
from loguru import logger

from .config import settings
from .logging import setup_logging
from .exchange.binance import BinanceAdapter

from .exchange.symbolmap import get_triangular_pairs

from .marketdata.aggregator import MarketDataAggregator
from .engine.triangle import Triangle
from .engine.signals import SignalGenerator
from .engine.executor import TradeExecutor
from .engine.risk import RiskManager
from .api.server import create_app


async def main():
    setup_logging()
    logger.info("Starting Triangular Arbitrage Bot")

    # Initialize components
    exchange = BinanceAdapter()
    tri_symbols = [s.strip() for s in settings.TRI_SYMBOLS.split(",")]
    triangular_pairs = get_triangular_pairs(settings.QUOTE, tri_symbols)
    market_data = MarketDataAggregator(exchange, [s for tri in triangular_pairs for s in tri])

    triangles = [
        Triangle(cycle=pair, path=(settings.QUOTE, pair[0].split('/')[0], pair[1].split('/')[0]))
        for pair in triangular_pairs
    ]

    signal_generator = SignalGenerator(market_data, triangles)
    risk_manager = RiskManager()

    executor = TradeExecutor(exchange, signal_generator, risk_manager, None)

    # Start background tasks
    market_data_task = asyncio.create_task(market_data.run())
    signal_task = asyncio.create_task(signal_generator.run())
    executor_task = asyncio.create_task(executor.run())

    # Start API server
    app = create_app()
    config = uvicorn.Config(app, host="0.0.0.0", port=settings.ADMIN_PORT, log_level="info")
    server = uvicorn.Server(config)
    server_task = asyncio.create_task(server.serve())

    await asyncio.gather(market_data_task, signal_task, executor_task, server_task)

    await exchange.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
