def test_post_acknowledgement():
    from model.trademax_api import TrademaxAPI
    t = TrademaxAPI()
    poa = t.post_purchase_order_acknowledgement('IO1544032', '2020-11-05T14:14:52+0100')
    print(poa)

    print(t.get_purchase_order('IO1544032'))
