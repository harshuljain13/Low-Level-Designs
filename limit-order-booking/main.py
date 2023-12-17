from Order import Order, OrderType
from OrderBook import OrderBook

def main():
    test_case_1()
    print('###############################')
    test_case_2()

    
def test_case_1():
    print('running testcase 1 ...')    
    buy_order_1 = Order('b1', OrderType.BUY, 100.1, 10, 1)
    sell_order_1 = Order('s1', OrderType.SELL, 100.0, 5, 2)
    
    ob = OrderBook()
    ob.place_order(buy_order_1)
    ob.place_order(sell_order_1)

    
def test_case_2():
    print('running testcase 2 ...')    
    buy_order_1 = Order('b1', OrderType.BUY, 100.1, 10, 1)
    sell_order_1 = Order('s1', OrderType.SELL, 100.2, 5, 2)
    sell_order_2 = Order('s2', OrderType.SELL, 100.2, 5, 3)
    buy_order_2 = Order('b2', OrderType.BUY, 100.3, 5, 4)
    buy_order_3 = Order('b3', OrderType.BUY, 100.2, 5, 5)
    
    
    ob = OrderBook()
    ob.place_order(buy_order_1)
    ob.place_order(sell_order_1)
    ob.place_order(sell_order_2)
    ob.place_order(buy_order_2)
    ob.place_order(buy_order_3)


if __name__ == "__main__":
    main()