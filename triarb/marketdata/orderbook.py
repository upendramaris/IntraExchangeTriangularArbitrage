from typing import List, Tuple
from sortedcontainers import SortedDict


class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.bids = SortedDict()
        self.asks = SortedDict()

    def update_bids(self, bids: List[Tuple[float, float]]):
        for price, qty in bids:
            if qty == 0:
                if price in self.bids:
                    del self.bids[price]
            else:
                self.bids[price] = qty

    def update_asks(self, asks: List[Tuple[float, float]]):
        for price, qty in asks:
            if qty == 0:
                if price in self.asks:
                    del self.asks[price]
            else:
                self.asks[price] = qty

    def get_best_bid_ask(self) -> Tuple[float | None, float | None]:
        best_bid = self.bids.peekitem(-1)[0] if self.bids else None
        best_ask = self.asks.peekitem(0)[0] if self.asks else None
        return best_bid, best_ask

    def get_cumulative_depth(self, side: str, levels: int) -> List[Tuple[float, float]]:
        """Returns the cumulative depth for a given side and number of levels."""
        depth = []
        cumulative_qty = 0
        if side == 'bids':
            for i in range(min(levels, len(self.bids))):
                price, qty = self.bids.peekitem(-1 - i)
                cumulative_qty += qty
                depth.append((price, cumulative_qty))
        elif side == 'asks':
            for i in range(min(levels, len(self.asks))):
                price, qty = self.asks.peekitem(i)
                cumulative_qty += qty
                depth.append((price, cumulative_qty))
        return depth
