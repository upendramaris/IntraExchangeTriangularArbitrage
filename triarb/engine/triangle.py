from dataclasses import dataclass
from typing import Tuple


@dataclass
class Triangle:
    """Represents a triangular arbitrage path."""
    cycle: Tuple[str, str, str]  # e.g., (BTC/USDT, ETH/BTC, ETH/USDT)
    path: Tuple[str, str, str]   # e.g., (USDT, BTC, ETH)

    def __repr__(self) -> str:
        return f"Triangle({' -> '.join(self.path)} -> {self.path[0]})"


def get_direction_and_pair(leg_from: str, leg_to: str, pairs: Tuple[str, str, str]) -> Tuple[str, str]:
    """Determines if a trade is a buy or sell for a given leg of a triangle."""
    for pair in pairs:
        base, quote = pair.split('/')
        if (leg_from == quote and leg_to == base):
            return 'buy', pair
        if (leg_from == base and leg_to == quote):
            return 'sell', pair
    raise ValueError(f"No pair found for leg {leg_from} -> {leg_to} in {pairs}")
