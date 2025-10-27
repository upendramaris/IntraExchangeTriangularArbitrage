from decimal import Decimal
import uuid

from loguru import logger

from ..config import settings
from .signals import Opportunity


class PaperTrader:
    """Simulates trades without executing them on a real exchange."""

    def __init__(self, inventory_manager):
        self.inventory_manager = inventory_manager

    async def execute_opportunity(self, opportunity: Opportunity):
        cycle_id = uuid.uuid4()
        logger.info(f"[PAPER] Executing opportunity {cycle_id} for {opportunity.triangle}")

        # Simulate the flow of funds
        # This is a highly simplified simulation.
        # A real simulation would need to account for price movements and fill probabilities.

        try:
            # Initial quote currency
            quote_currency = settings.QUOTE
            initial_amount = Decimal(str(opportunity.max_qty_quote))

            # Leg 1
            leg1 = opportunity.legs[0]
            base1, _ = leg1['pair'].split('/')
            rate1 = Decimal(str(leg1['price']))
            amount_base1 = initial_amount / rate1 if leg1['dir'] == 'buy' else initial_amount * rate1
            logger.info(f"[PAPER] Leg 1: {leg1['dir']} {initial_amount:.4f} {quote_currency} for {amount_base1:.8f} {base1} @ {rate1}")

            # Leg 2
            leg2 = opportunity.legs[1]
            base2, _ = leg2['pair'].split('/')
            rate2 = Decimal(str(leg2['price']))
            amount_base2 = amount_base1 / rate2 if leg2['dir'] == 'buy' else amount_base1 * rate2
            logger.info(f"[PAPER] Leg 2: {leg2['dir']} {amount_base1:.8f} {base1} for {amount_base2:.8f} {base2} @ {rate2}")

            # Leg 3
            leg3 = opportunity.legs[2]
            final_quote_currency, _ = leg3['pair'].split('/')
            rate3 = Decimal(str(leg3['price']))
            final_amount = amount_base2 / rate3 if leg3['dir'] == 'buy' else amount_base2 * rate3
            logger.info(f"[PAPER] Leg 3: {leg3['dir']} {amount_base2:.8f} {base2} for {final_amount:.4f} {final_quote_currency} @ {rate3}")

            pnl = final_amount - initial_amount
            logger.success(f"[PAPER] Cycle {cycle_id} completed. PnL: {pnl:.4f} {quote_currency}")

            # Here you would update the paper inventory
            # await self.inventory_manager.update_balance(quote_currency, pnl)

        except Exception as e:
            logger.error(f"[PAPER] Error during simulated execution {cycle_id}: {e}")
