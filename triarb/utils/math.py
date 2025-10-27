from decimal import Decimal, getcontext

# Set precision for Decimal operations
getcontext().prec = 30

def bps_to_decimal(bps: float) -> Decimal:
    """Convert basis points to a decimal value."""
    return Decimal(bps) / Decimal(10000)

def decimal_to_bps(dec: Decimal) -> float:
    """Convert a decimal value to basis points."""
    return float(dec * Decimal(10000))
