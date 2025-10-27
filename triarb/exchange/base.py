from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ExchangeAdapter(ABC):
    """Abstract base class for exchange adapters."""

    @abstractmethod
    async def get_symbols(self) -> List[str]:
        """Fetch all symbols from the exchange."""
        pass

    @abstractmethod
    async def get_ws_url(self) -> str:
        """Get the WebSocket URL for the exchange."""
        pass

    @abstractmethod
    def get_l2_channel_name(self) -> str:
        """Get the name of the L2 order book channel."""
        pass

    @abstractmethod
    def normalize_symbol(self, symbol: str) -> str:
        """Normalize a symbol to the exchange's format."""
        pass

    @abstractmethod
    def denormalize_symbol(self, symbol: str) -> str:
        """Denormalize a symbol from the exchange's format."""
        pass

    @abstractmethod
    async def place_order(self, symbol: str, side: str, order_type: str, amount: float, price: float | None = None) -> Dict[str, Any]:
        """Place an order on the exchange."""
        pass

    @abstractmethod
    async def fetch_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """Fetch an order from the exchange."""
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """Cancel an order on the exchange."""
        pass

    @abstractmethod
    async def fetch_balance(self) -> Dict[str, Any]:
        """Fetch account balances from the exchange."""
        pass
