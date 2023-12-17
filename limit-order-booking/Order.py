from datetime import datetime
from enum import Enum

class OrderType(Enum):
    BUY = 'Buy'
    SELL = 'Sell'

class Order:
    def __init__(self, order_id, order_type, price, volume, timestamp):
        self.order_id = order_id
        self.timestamp = timestamp 
        self.order_type = order_type
        self.price = price
        self.volume = volume
        
    def with_order_id(self, order_id):
        self.order_id = order_id
        return self
    
    def with_timestamp(self, timestamp):
        self.timestamp = timestamp
        return self
    
    def with_order_type(self, order_type):
        self.order_type = order_type
        return self

    def with_price(self, price):
        self.price = price
        return self

    def with_volume(self, volume):
        self.volume = volume
        return self

    def build(self):
        return self
