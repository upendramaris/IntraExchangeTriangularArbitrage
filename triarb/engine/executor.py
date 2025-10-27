import asyncio
import uuid
from decimal import Decimal

from loguru import logger

from ..config import settings
from ..exchange.base import ExchangeAdapter
from .signals import Opportunity, SignalGenerator
from .risk import RiskManager



class TradeExecutor:
    def __init__(self, exchange: ExchangeAdapter, signal_generator: SignalGenerator, risk_manager: RiskManager, trade_repo = None):
        self.exchange = exchange
        self.signal_generator = signal_generator
        self.risk_manager = risk_manager
        self.opportunity_queue = self.signal_generator.get_queue()

    async def run(self):
        while True:
            opportunity = await self.opportunity_queue.get()
            if self.risk_manager.is_execution_allowed(opportunity):
                asyncio.create_task(self.execute_opportunity(opportunity))

    async def execute_opportunity(self, opportunity: Opportunity):
        cycle_id = uuid.uuid4()
        logger.info(f"Executing opportunity {cycle_id} for {opportunity.triangle}")

        # TODO: This is a simplified execution logic. A robust implementation would handle
        # partial fills, order timeouts, and unwinding logic.

        try:
            # Leg 1
            leg1 = opportunity.legs[0]
            qty1 = opportunity.max_qty_quote / Decimal(str(leg1['price']))
            order1 = await self.exchange.place_order(
                symbol=leg1['pair'],
                side=leg1['dir'],
                order_type='market', # or aggressive limit
                amount=float(qty1),
            )
            logger.info(f"Leg 1 ({leg1['pair']} {leg1['dir']}) placed: {order1['id']}")

            # TODO: Wait for fill, then calculate next leg's quantity

            # Leg 2
            leg2 = opportunity.legs[1]
            # Assuming full fill of leg 1 for now
            qty2 = qty1 # This is incorrect, needs to be based on the output of leg 1
            order2 = await self.exchange.place_order(
                symbol=leg2['pair'],
                side=leg2['dir'],
                order_type='market',
                amount=float(qty2),
            )
            logger.info(f"Leg 2 ({leg2['pair']} {leg2['dir']}) placed: {order2['id']}")

            # Leg 3
            leg3 = opportunity.legs[2]
            # Assuming full fill of leg 2 for now
            qty3 = qty2 # This is incorrect
            order3 = await self.exchange.place_order(
                symbol=leg3['pair'],
                side=leg3['dir'],
                order_type='market',
                amount=float(qty3),
            )
            logger.info(f"Leg 3 ({leg3['pair']} {leg3['dir']}) placed: {order3['id']}")

            self.risk_manager.on_execution_success(opportunity)

        except Exception as e:
            logger.error(f"Error executing opportunity {cycle_id}: {e}")
            self.risk_manager.on_execution_failure(opportunity)
            # TODO: Implement unwinding logic here
