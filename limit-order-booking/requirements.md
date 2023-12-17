### Definition

1. A log book that has the open orders of buy or sell side. These are the orders that can't be fulfilled immediately. 
    - This means if a person X wants to buy an asset at 100 USD but all sellers want to sell at minimum of 150 USD, then request for buying (bidding) will be entered in the log book.
2. An Order will have 4 parts
    - Order Id : Something that uniquely identifies the order.
    - Type of the order : Buy (Bid) or Sell(Ask)
    - Volume : Number of the assets to buy or sell in the order
    - Limit Price: Unit Price of the asset such that
        - For buying, this will be maximum price buyer can bid. 
        - For selling, this will be minimum price seller can ask.
    - Timestamp: when the order was logged.
3. Trade is executed when the highest bid price >= lowest ask price and highest bid volume >= lowest ask volume. This also means spread is being crossed. 
4. Price at which the trade is executed is that of the entry present in the order book. 
    - This means if person X want to buy an asset at 100 USD, but there is a seller who was waiting in order book to sell at 80 USD, assets will be sold to Buyer for 80 USD. 
4. If there are more than 1 orders (buy or sell) with same price, the one that was logged earlier will be preferred.

### APIs

1. PlaceOrder(order) : Takes an order as input and either fills or places in order book if no match found on other side.
2. CancelOrder(orderId) : Takes in orderId as input and cancels it if it is part of order book. If it has already being filled, then no-op.
3. GetVolumeAtPrice(price, orderType): Get volume of the open buy or sell orders at a certain price.