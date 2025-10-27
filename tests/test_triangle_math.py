from decimal import Decimal

import pytest

from triarb.engine.fees import get_effective_rate
from triarb.utils.math import bps_to_decimal


def test_effective_rate_buy():
    price = Decimal("100")
    fee_bps = bps_to_decimal(10)  # 0.1%
    slippage_bps = bps_to_decimal(5) # 0.05%
    effective_price = get_effective_rate(price, 'buy', fee_bps, slippage_bps)
    assert effective_price > price
    # 100 * (1 + 0.001) * (1 + 0.0005) = 100.15005
    assert effective_price == pytest.approx(Decimal("100.15005"))

def test_effective_rate_sell():
    price = Decimal("100")
    fee_bps = bps_to_decimal(10)
    slippage_bps = bps_to_decimal(5)
    effective_price = get_effective_rate(price, 'sell', fee_bps, slippage_bps)
    assert effective_price < price
    # 100 / ((1 + 0.001) * (1 + 0.0005)) = 99.8500998...
    assert effective_price == pytest.approx(Decimal("99.85009985"))

# TODO: Add tests for cycle edge calculation
