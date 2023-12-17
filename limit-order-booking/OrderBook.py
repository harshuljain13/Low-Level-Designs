from Order import Order, OrderType
from collections import defaultdict, deque
from DataStructures import BuyOrdersMaxHeap, SellOrdersMinHeap


class OrderBook:
    def __init__(self) -> None:
        self.buy_orders = BuyOrdersMaxHeap() # max heap for buy order
        self.sell_orders = SellOrdersMinHeap() # min heap for sell order

        self.buy_volume_at_price = defaultdict(int) # hashmap to maintain buy volume at price
        self.sell_volume_at_price = defaultdict(int) # hashmap to maintain sell volume at price

        self.buy_order_price_to_heap_index_map = dict() 
        self.sell_order_price_to_heap_index_map = dict()


    def store_buy_order_in_order_book(self, order: Order) -> None:
        '''
        store the buy order in the order book
        '''
        print(f'.............Storing buy order...............')
        
        order_price = order.price
            
        print(f'Buy heap state before storing order : {self.buy_order_price_to_heap_index_map}')
        # check price exists in heap
        if order_price not in self.buy_order_price_to_heap_index_map:
            
            # add the order to heap as new node.
            new_node_index = self.buy_orders.push_order(order)

            # update the price to heap node map.
            self.buy_order_price_to_heap_index_map[order_price] = new_node_index
            print(f'heap index map after storing buy order {order.order_id}: {self.buy_order_price_to_heap_index_map}')
        else:
            print(f'Buy order with {order.order_id, order_price} found in heap index map: {self.buy_order_price_to_heap_index_map}')
            # get the price_node
            heap_index = self.buy_order_price_to_heap_index_map[order_price]
            print(f'Buy order with exists in heap index map at {heap_index}')

            # add the order to specific heap node.
            self.buy_orders.push_order_at_index(order, heap_index)

        # update the volume 
        self.buy_volume_at_price[order.price] += order.volume
        print(f'Volume at price {order.price} after adding order: {self.buy_volume_at_price[order.price]}')

    def store_sell_order_in_order_book(self, order: Order) -> None:
        '''
        store the sell order in the order book
        '''
        print(f'.............Storing sell order...............')

        order_price = order.price
        
        print(f'Sell heap state before storing order : {self.sell_order_price_to_heap_index_map}')
        # check price exists in heap
        if order_price not in self.sell_order_price_to_heap_index_map:
            # add the order to heap as new node.
            new_node_index = self.sell_orders.push_order(order)

            # update the price to heap node map.
            self.sell_order_price_to_heap_index_map[order_price] = new_node_index
            print(f'heap index map after storing sell order {order.order_id}: {self.sell_order_price_to_heap_index_map}')
        else:
            # get the price_node
            heap_index = self.sell_order_price_to_heap_index_map[order_price]
            print(f'Sell order with exists in heap index map at {heap_index}')

            # add the order to specific heap node.
            self.sell_orders.push_order_at_index(order, heap_index)

        # update the volume 
        self.sell_volume_at_price[order.price] += order.volume
        print(f'Volume at price {order.price} after adding order: {self.sell_volume_at_price[order.price]}')

    def place_buy_order(self, order: Order) -> None:
        print('............Placing buy order..............')
        is_order_matched = self.match_order(order)
        
        if not is_order_matched:
            self.store_buy_order_in_order_book(order)
        else:
            print(f'............buy order matched..............')
            
    def place_sell_order(self, order: Order):
        print('............Placing sell order..............')
        is_order_matched = self.match_order(order)
        if not is_order_matched:
            self.store_sell_order_in_order_book(order)
        else:
            print(f'............sell order matched..............')

    def place_order(self, order: Order):
        print(f'\n')
        print('...............Placing the order.................')
        if order.order_type  == OrderType.BUY:
            print(f'Detected a buy order with id:{order.order_id}, price:{order.price}, volume:{order.volume}')
            self.place_buy_order(order)
        else:
            print(f'Detected a sell order with id:{order.order_id}, price:{order.price}, volume:{order.volume}')
            self.place_sell_order(order)

    def delete_buy_order(self, order):
        '''
        delete the buy order from the order book
        '''
        order_price = order.price
        print(f'........Deleting buy order........')

        if order_price not in self.buy_order_price_to_heap_index_map:
            print(f'buy order with price {order_price} does not exist in heap {self.buy_order_price_to_heap_index_map}')
            return

        # get the order from the heap.
        print(f'deleting buy order {order.order_id} from the buy_orders')
        is_index_valid = self.buy_orders.delete_order(self.buy_order_price_to_heap_index_map[order_price], order.order_id)
        if not is_index_valid:
            del self.buy_order_price_to_heap_index_map[order_price]
            print(f'After deleting the buy order with price {order_price}: {self.buy_order_price_to_heap_index_map}')

        # update the volume 
        self.buy_volume_at_price[order.price] -= order.volume
        print(f'update buy orders volume at price {order_price}: {self.buy_volume_at_price[order_price]} ')

        if self.buy_volume_at_price[order_price] == 0:
            print(f'delete buy orders volume entry at price {order_price}')
            del self.buy_volume_at_price[order_price]
            print(f'after deleting the buy orders volume entry at price {order_price}: {self.buy_volume_at_price}')

    def delete_sell_order(self, order):
        '''
        delete the buy order from the order book
        '''
        order_price = order.price
        print(f'........Deleting sell order........')

        if order_price not in self.sell_order_price_to_heap_index_map:
            print(f'sell order with price {order_price} does not exist in heap {self.sell_order_price_to_heap_index_map}')
            return

        # get the order from the heap.
        print(f'deleting sell order {order.order_id} from the sell_orders')
        is_index_valid = self.sell_orders.delete_order(self.sell_order_price_to_heap_index_map[order_price], order.order_id)

        if not is_index_valid:
            del self.sell_order_price_to_heap_index_map[order_price]
            print(f'After deleting the sell order with price {order_price}: {self.sell_order_price_to_heap_index_map}')

        # update the volume 
        self.sell_volume_at_price[order.price] -= order.volume
        print(f'update sell orders volume at price {order_price}: {self.sell_volume_at_price[order_price]} ')

        if self.sell_volume_at_price == 0:
            print(f'delete sell orders volume entry at price {order_price}')
            del self.sell_volume_at_price[order_price]
            print(f'after deleting the sell orders volume entry at price {order_price}: {self.sell_volume_at_price}')


    def cancel_order(self, order):
        '''
        cancels the order with a certain order id
        '''
        # check if order_price exists in the map
        if order.order_type == OrderType.BUY:
            self.delete_buy_order(order)
        else:
            self.delete_sell_order(order)

    def get_volumne_at_price(self, price, order_type):
        '''
        need to fetch the volume at a particular price and order type        
        '''
        if order_type == OrderType.BUY:
            return self.buy_volume_at_price[price]
        else:
            return self.sell_volume_at_price[price]

    def match_buy_order(self, order: Order):
        '''
        check if buy order can be matched with sell order
        '''
        print("............Trying to match buy order ..............")
        while order.volume > 0:
            best_sell_order = self.sell_orders.peek()
        
            # check if best sell order is available
            if best_sell_order is None:
                print('No sell order available...')
                return False
            
            # check if best sell order is greater than the order
            if best_sell_order.price > order.price:
                print(f'Sell order available with id:{best_sell_order.order_id},  price:{best_sell_order.price} but cant be matched')
                return False
            
            print(f'Matching Sell order available with id:{best_sell_order.order_id},  price:{best_sell_order.price}, volume:{best_sell_order.volume}')
            print(f'sell volume before matching : {self.sell_volume_at_price}')
            if order.volume < best_sell_order.volume:
                best_sell_order.volume -= order.volume
                self.sell_volume_at_price[best_sell_order.price] -= order.volume
                order.volume = 0
                print(f'updated volume of matching sell order with id: {best_sell_order.order_id}: {best_sell_order.volume}')
            else:
                order.volume -= best_sell_order.volume
                self.delete_sell_order(best_sell_order)

            print(f'sell volume after matching : {self.sell_volume_at_price}')
        return True
    
    def match_sell_order(self, order: Order):
        '''
        check if sell order can be matched with buy order
        '''
        print("............Trying to match sell order ............")
        while order.volume > 0:
            best_buy_order = self.buy_orders.peek()
        
            # check if best buy order is available
            if best_buy_order is None:
                print(f'No buy order available : {self.buy_orders}')
                return False
            
            # check if best buy order is greater than the order
            if best_buy_order.price < order.price:
                print(f'buy order available with id:{best_buy_order.order_id},  price:{best_buy_order.price} but cant be matched')
                return False
            
            print(f'Matching buy order available with id:{best_buy_order.order_id},  price:{best_buy_order.price}, volume:{best_buy_order.volume}')
            print(f'buy volume before matching : {self.buy_volume_at_price}')

            if order.volume < best_buy_order.volume:
                best_buy_order.volume -= order.volume
                self.buy_volume_at_price[best_buy_order.price] -= order.volume
                order.volume = 0
                print(f'updated volume of matching buy order with id: {best_buy_order.order_id}: {best_buy_order.volume}')
            else:
                order.volume -= best_buy_order.volume
                self.delete_buy_order(best_buy_order)

            print(f'buy volume after matching : {self.buy_volume_at_price}')
        
        return True

    def match_order(self, order: Order):
        '''
        check if there is a trade can be executed
        '''
        if order.order_type == OrderType.BUY:
            return self.match_buy_order(order)
        else:
            return self.match_sell_order(order)
