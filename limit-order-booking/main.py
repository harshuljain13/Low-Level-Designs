from Order import Order, OrderType
from OrderBook import OrderBook

def main():
    test_case_1()

    
    
def test_case_1():
    print('running testcase 1 ...')    
    buy_order_1 = Order('b1', OrderType.BUY, 100.1, 10, 1)
    sell_order_1 = Order('s1', OrderType.SELL, 100.2, 5, 2)
    
    ob = OrderBook()

    print ('.............Placing first order..............')
    ob.place_order(buy_order_1)

    print ('.............Placing next order..............')
    ob.place_order(sell_order_1)


if __name__ == "__main__":
    main()