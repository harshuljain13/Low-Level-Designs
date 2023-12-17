from Order import Order

class DoublyLinkedListNode:
    def __init__(self, value: Order):
        self.value = value
        self.next = None
        self.prev = None
        
class DoublyLinkedList:
    def __init__(self, price) -> None:
        self.head = DoublyLinkedListNode(None)
        self.tail = DoublyLinkedListNode(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.current_size = 0
        self.price = price

        # map to allow delete in O(1)
        self.order_id_to_dll_node_map = dict()

    def add_order(self, order: Order):

        print(f'...........Adding order to to DLL.......')
        node = DoublyLinkedListNode(order)
        
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node
        
        self.order_id_to_dll_node_map[node.value.order_id] = node
        self.current_size += 1
        print(f'DLL state map after adding order : {self.order_id_to_dll_node_map}')
        print(f'DLL current size after adding order : {self.current_size}')

    def delete_order(self, order_id):
        print(f'...........Deleting order from DLL.......')
        node = self.order_id_to_dll_node_map[order_id]

        node.prev.next = node.next
        node.next.prev = node.prev
        del self.order_id_to_dll_node_map[order_id]
        self.current_size -= 1
        print(f'DLL state map after deleting order : {self.order_id_to_dll_node_map}')
        print(f'DLL current size after deleting order : {self.current_size}')

    def peek(self):

        return self.head.next

    def size(self):
        print(f'DLL current size : {self.current_size}')
        return self.current_size


class SellOrdersMinHeap:
    def __init__(self):
        self.heap = []
        self.current_size = 0

    def initialize_dll(self, order: Order) -> DoublyLinkedList:
        return DoublyLinkedList(order.price)

    def bottom_top_min_heapify(self, index:int) -> None:
        # work your way upwards to meet the heap property.
        parent_index = (index - 1) // 2
        while parent_index >= 0:
            if self.heap[index].price < self.heap[parent_index].price:
                # swapping
                temp = self.heap[parent_index]
                self.heap[parent_index] = self.heap[index]
                self.heap[index] = temp

                # setup new order_index and parent_index
                index = parent_index
                parent_index = (index - 1) // 2
    
    def top_bottom_min_heapify(self, index:int) -> None:
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2

        smallest_index = index

        if left_child_index < self.current_size and self.heap[left_child_index].price < self.heap[smallest_index].price:
            smallest_index = left_child_index
        
        if right_child_index < self.current_size and self.heap[right_child_index].price < self.heap[smallest_index].price:
            smallest_index = right_child_index
        
        if smallest_index != index:
            temp = self.heap[smallest_index]
            self.heap[smallest_index] = self.heap[index]
            self.heap[index] = temp

            self.top_bottom_min_heapify(smallest_index)

    def push_order(self, order: Order) -> DoublyLinkedList:
        # initialize the doubly linked list for the new price and add order to the dll.
        order_dll = self.initialize_dll(order)
        order_dll.add_order(order)

        # add dll at the end of the heap.
        self.heap.append(order_dll)
        self.current_size += 1
        order_dll_index = self.current_size - 1

        self.bottom_top_min_heapify(order_dll_index)
        
        return order_dll_index

    def push_order_at_index(self, order: Order, index: int):
        '''
        add order to the specific dll in the heap.
        '''
        print('Adding order in the heap node')
        dll = self.heap[index]
        dll.add_order(order)

    def delete_node(self, index: int):
        self.heap[index] = self.heap[self.current_size - 1]
        self.heap.pop()
        self.current_size -= 1

        self.top_bottom_min_heapify(index)


    def delete_order(self, index: int, order_id) -> bool:
        print(f'Deleting the order {order_id} at index {index}')
        dll = self.heap[index]
        dll.delete_order(order_id)

        if dll.size() == 0:
            # remove the dll from the heap
            self.delete_node(index)
            return False
        return True

    def peek(self):
        print(f'sell heap state while peeking: {self.heap}, {self.current_size}')
        if self.current_size == 0:
            return None
        
        dll = self.heap[0]
        return dll.peek().value

    def size(self):
        return self.current_size

class BuyOrdersMaxHeap:
    def __init__(self):
        self.heap = []
        self.current_size = 0

    def initialize_dll(self, order: Order) -> DoublyLinkedList:
        return DoublyLinkedList(order.price)

    def bottom_top_max_heapify(self, index:int) -> None:
        # work your way upwards to meet the heap property.
        parent_index = (index - 1) // 2
        while parent_index >= 0:
            if self.heap[index].price > self.heap[parent_index].price:
                # swapping
                temp = self.heap[parent_index]
                self.heap[parent_index] = self.heap[index]
                self.heap[index] = temp

                # setup new order_index and parent_index
                index = parent_index
                parent_index = (index - 1) // 2
    
    def top_bottom_max_heapify(self, index:int) -> None:
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2

        smallest_index = index

        if left_child_index < self.current_size and self.heap[left_child_index].price > self.heap[smallest_index].price:
            smallest_index = left_child_index
        
        if right_child_index < self.current_size and self.heap[right_child_index].price > self.heap[smallest_index].price:
            smallest_index = right_child_index
        
        if smallest_index != index:
            temp = self.heap[smallest_index]
            self.heap[smallest_index] = self.heap[index]
            self.heap[index] = temp

            self.top_bottom_max_heapify(smallest_index)

    def push_order(self, order: Order) -> DoublyLinkedList:
        # initialize the doubly linked list for the new price and add order to the dll.
        order_dll = self.initialize_dll(order)
        order_dll.add_order(order)

        # add dll at the end of the heap.
        self.heap.append(order_dll)
        self.current_size += 1
        order_dll_index = self.current_size - 1

        self.bottom_top_max_heapify(order_dll_index)
        print(f'buy heap state after adding order: {self.heap}')
        print(f'buy heap size after adding order: {self.current_size}')
        
        return order_dll_index

    def push_order_at_index(self, order: Order, index: int):
        print('Adding order in the heap node')
        dll = self.heap[index]
        dll.add_order(order)

    def delete_node(self, index: int):  
        self.heap[index] = self.heap[self.current_size - 1]
        self.heap.pop()
        self.current_size -= 1

        self.top_bottom_max_heapify(index)

    def delete_order(self, index: int, order_id) -> bool:
        print(f'Deleting the order {order_id} at index {index}')
        dll = self.heap[index]
        dll.delete_order(order_id)

        if dll.size() == 0:
            # remove the dll from the heap
            self.delete_node(index)
            return False
        return True

    def peek(self) -> DoublyLinkedListNode:
        print(f'buy heap state while peeking: {self.heap}, {self.current_size}')
        if self.current_size == 0:
            return None
        
        dll = self.heap[0]
        return dll.peek().value

    def size(self):
        return self.current_size
