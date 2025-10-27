from triarb.marketdata.orderbook import OrderBook


def test_orderbook_update():
    ob = OrderBook("BTC/USDT")
    bids = [(100, 1), (99, 2)]
    asks = [(101, 3), (102, 4)]
    ob.update_bids(bids)
    ob.update_asks(asks)

    assert ob.get_best_bid_ask() == (100, 101)

    # Test update
    ob.update_bids([(100.5, 5)])
    assert ob.get_best_bid_ask()[0] == 100.5

    # Test removal
    ob.update_asks([(101, 0)])
    assert ob.get_best_bid_ask()[1] == 102

def test_cumulative_depth():
    ob = OrderBook("BTC/USDT")
    bids = [(100, 1), (99, 2), (98, 3)]
    ob.update_bids(bids)

    depth = ob.get_cumulative_depth('bids', 2)
    assert len(depth) == 2
    assert depth[0] == (100, 1) # Price, cumulative qty
    assert depth[1] == (99, 3)
