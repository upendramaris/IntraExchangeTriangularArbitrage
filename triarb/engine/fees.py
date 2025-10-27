from decimal import Decimal

from ..config import settings


def get_effective_rate(price: Decimal, side: str, fee_bps: Decimal, slippage_bps: Decimal) -> Decimal:
    """
    Calculates the effective rate after accounting for fees and slippage.
    For buys, the effective rate is higher. For sells, it's lower.
    """
    fee_mult = Decimal(1) + fee_bps
    slip_mult = Decimal(1) + slippage_bps

    if side == 'buy':
        return price * fee_mult * slip_mult
    elif side == 'sell':
        return price / (fee_mult * slip_mult) # or price * (1 - fee_bps - slippage_bps)
    else:
        raise ValueError(f"Invalid side: {side}")


def get_taker_fee_bps(exchange: str) -> Decimal:
    """Get the taker fee in basis points for a given exchange."""
    fee_info = settings.FEE_TABLE.get(exchange, {})
    taker_fee = fee_info.get('taker', 0.001) # Default to 0.1% if not found
    return Decimal(taker_fee) * 100 # Convert to bps
