import asyncio
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Tuple

from loguru import logger

from ..config import settings
from ..marketdata.aggregator import MarketDataAggregator
from ..utils.math import bps_to_decimal
from .triangle import Triangle, get_direction_and_pair
from .fees import get_effective_rate, get_taker_fee_bps


@dataclass
class Opportunity:
    triangle: Triangle
    gross_edge_bps: Decimal
    net_edge_bps: Decimal
    max_qty_quote: Decimal
    legs: List[dict]


class SignalGenerator:
    def __init__(self, market_data: MarketDataAggregator, triangles: List[Triangle]):
        self.market_data = market_data
        self.triangles = triangles
        self.opportunity_queue = asyncio.Queue()
        self.fee_bps = bps_to_decimal(get_taker_fee_bps(settings.EXCHANGE))
        self.slippage_bps = bps_to_decimal(settings.SLIPPAGE_BPS)

    async def run(self):
        while True:
            await asyncio.sleep(0.1) # Small sleep to prevent busy-looping
            for triangle in self.triangles:
                try:
                    opportunity = self._check_triangle(triangle)
                    if opportunity:
                        await self.opportunity_queue.put(opportunity)
                except Exception as e:
                    logger.warning(f"Error checking triangle {triangle}: {e}")

    def _check_triangle(self, triangle: Triangle) -> Opportunity | None:
        """Checks a single triangle for an arbitrage opportunity."""
        p1, p2, p3 = triangle.path
        pairs = triangle.cycle

        # Leg 1: p1 -> p2
        dir1, pair1 = get_direction_and_pair(p1, p2, pairs)
        ob1 = self.market_data.get_order_book(pair1)
        if not ob1: return None

        # Leg 2: p2 -> p3
        dir2, pair2 = get_direction_and_pair(p2, p3, pairs)
        ob2 = self.market_data.get_order_book(pair2)
        if not ob2: return None

        # Leg 3: p3 -> p1
        dir3, pair3 = get_direction_and_pair(p3, p1, pairs)
        ob3 = self.market_data.get_order_book(pair3)
        if not ob3: return None

        # Get top of book prices
        bid1, ask1 = ob1.get_best_bid_ask()
        bid2, ask2 = ob2.get_best_bid_ask()
        bid3, ask3 = ob3.get_best_bid_ask()

        if not all([bid1, ask1, bid2, ask2, bid3, ask3]):
            return None # Not all books have depth

        # Gross rate calculation (no fees/slippage)
        rate1_gross = Decimal(str(ask1)) if dir1 == 'buy' else Decimal(str(1/bid1))
        rate2_gross = Decimal(str(ask2)) if dir2 == 'buy' else Decimal(str(1/bid2))
        rate3_gross = Decimal(str(ask3)) if dir3 == 'buy' else Decimal(str(1/bid3))
        gross_edge = (rate1_gross * rate2_gross * rate3_gross) - 1
        gross_edge_bps = gross_edge * 10000

        if gross_edge_bps < settings.MIN_GROSS_EDGE_BPS:
            return None

        # Net rate calculation (with fees/slippage)
        price1_eff = get_effective_rate(Decimal(str(ask1 if dir1 == 'buy' else bid1)), dir1, self.fee_bps, self.slippage_bps)
        price2_eff = get_effective_rate(Decimal(str(ask2 if dir2 == 'buy' else bid2)), dir2, self.fee_bps, self.slippage_bps)
        price3_eff = get_effective_rate(Decimal(str(ask3 if dir3 == 'buy' else bid3)), dir3, self.fee_bps, self.slippage_bps)

        rate1_net = price1_eff if dir1 == 'buy' else 1 / price1_eff
        rate2_net = price2_eff if dir2 == 'buy' else 1 / price2_eff
        rate3_net = price3_eff if dir3 == 'buy' else 1 / price3_eff

        net_edge = (rate1_net * rate2_net * rate3_net) - 1
        net_edge_bps = net_edge * 10000

        if net_edge_bps < settings.MIN_NET_EDGE_BPS:
            return None

        # TODO: Calculate max executable quantity based on depth
        max_qty_quote = Decimal(str(settings.TARGET_NOTIONAL_QUOTE))

        legs = [
            {"pair": pair1, "dir": dir1, "price": ask1 if dir1 == 'buy' else bid1},
            {"pair": pair2, "dir": dir2, "price": ask2 if dir2 == 'buy' else bid2},
            {"pair": pair3, "dir": dir3, "price": ask3 if dir3 == 'buy' else bid3},
        ]

        opportunity = Opportunity(
            triangle=triangle,
            gross_edge_bps=gross_edge_bps,
            net_edge_bps=net_edge_bps,
            max_qty_quote=max_qty_quote,
            legs=legs
        )

        logger.info(f"Found opportunity: {opportunity}")
        return opportunity

    def get_queue(self) -> asyncio.Queue:
        return self.opportunity_queue
