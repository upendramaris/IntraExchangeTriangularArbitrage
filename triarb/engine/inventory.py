from typing import Dict
from decimal import Decimal

from ..data.redis_state import RedisState


class InventoryManager:
    def __init__(self, redis: RedisState):
        self.redis = redis

    async def get_balance(self, currency: str) -> Decimal:
        """Get the balance for a specific currency."""
        balance = await self.redis.get(f"balance:{currency}")
        return Decimal(balance) if balance else Decimal(0)

    async def set_balance(self, currency: str, amount: Decimal):
        """Set the balance for a specific currency."""
        await self.redis.set(f"balance:{currency}", str(amount))

    async def update_balance(self, currency: str, change: Decimal):
        """Update the balance for a specific currency by a delta."""
        # This should be an atomic operation in a real system
        current_balance = await self.get_balance(currency)
        await self.set_balance(currency, current_balance + change)

    async def get_all_balances(self) -> Dict[str, Decimal]:
        """Get all balances."""
        # This is a simplified implementation. In a real system, you would
        # scan for all balance keys.
        keys = await self.redis.keys("balance:*")
        balances = {}
        for key in keys:
            currency = key.split(":")[1]
            balances[currency] = await self.get_balance(currency)
        return balances
