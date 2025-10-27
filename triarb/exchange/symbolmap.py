from typing import List, Tuple
from itertools import permutations

from ..config import settings


def get_triangular_pairs(quote_currency: str, base_currencies: List[str]) -> List[Tuple[str, str, str]]:
    """
    Generates all unique triangular arbitrage pairs from a list of base currencies and a quote currency.
    A triangular pair is a tuple of three symbols, e.g., (BTC/USDT, ETH/BTC, ETH/USDT).
    """
    all_currencies = [quote_currency] + base_currencies
    pairs = set()

    # Generate all permutations of 3 currencies
    for p in permutations(all_currencies, 3):
        c1, c2, c3 = p

        # Attempt to form a triangle
        # Path 1: c1 -> c2 -> c3 -> c1
        try:
            pair1 = f"{c2}/{c1}"
            pair2 = f"{c3}/{c2}"
            pair3 = f"{c3}/{c1}" # or f'{c1}/{c3}'
            # We need to check which way the market exists
            # This is a simplification. A real implementation would check against available markets.
            pairs.add(tuple(sorted((pair1, pair2, pair3))))
        except ValueError:
            pass

    # A more direct way for the specified structure Q -> B1 -> B2 -> Q
    pairs = set()
    for b1, b2 in permutations(base_currencies, 2):
        # Triangle: QUOTE -> b1 -> b2 -> QUOTE
        # Leg 1: b1/QUOTE
        # Leg 2: b2/b1
        # Leg 3: b2/QUOTE
        pair1 = f"{b1}/{quote_currency}"
        pair2 = f"{b2}/{b1}"
        pair3 = f"{b2}/{quote_currency}"
        pairs.add(tuple(sorted((pair1, pair2, pair3))))

    return [tuple(p) for p in pairs]

def get_all_symbols_from_triangles(triangles: List[Tuple[str, str, str]]) -> List[str]:
    """Extracts all unique symbols from a list of triangular pairs."""
    symbols = set()
    for tri in triangles:
        for symbol in tri:
            symbols.add(symbol)
    return list(symbols)
