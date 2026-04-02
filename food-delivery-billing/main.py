from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod



class Item:
    def __init__(self, name, price):
        self.id = id
        self.name = name
        self.price = price


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"


class OrderBill:
    def __init__(self, order_id):
        self.order_id = order_id
        self.itemized_prices = []
        self.items_total = 0
        self.delivery_fee = 0
        self.surcharge_fee = 0
        self.tax = 0
        self.discount = 0
        self.final_total = 0


class Order:
    def __init__(self, id):
        self.id = id
        self.items = []
        self.driver_id = None
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.bill = None
    
    def assign_driver(self, driver_id):
        self.driver_id = driver_id

    def update_status(self, status: OrderStatus):
        self.status = status
        self.updated_at = datetime.now()

    def assign_bill(self, bill: OrderBill):
        self.bill = bill


class RuleType(Enum):
    FEE = "Fee"
    DISCOUNT = "Discount"
    SURCHARGE = "Surcharge"
    TAX = "Tax"


class FeeComponent:
    def __init__(self, rule_type: RuleType, name, amount):
        self.rule_type = rule_type
        self.name = name
        self.amount = amount


class Rule(ABC):
    def __init__(self, name, rule_type: RuleType):
        self.name = name
        self.rule_type = rule_type
    
    @abstractmethod
    def is_applicable(self, order: Order):
        pass

    @abstractmethod
    def apply(self, order: Order) -> FeeComponent:
        pass


class BaseDeliveryFeeRule(Rule):
    def __init__(self, name, fee_amount):
        super().__init__(name, RuleType.FEE)
        self.fee_amount = fee_amount

    def is_applicable(self, order: Order):
        return True

    def apply(self, order: Order):
        return FeeComponent(
            rule_type=RuleType.FEE, 
            name="Base Delivery Fee", 
            amount=self.fee_amount
        )


class SurchargeDeliveryRule(Rule):
    def __init__(self, name, surcharge_amount):
        super().__init__(name, RuleType.SURCHARGE)
        self.surcharge_amount = surcharge_amount
    
    def is_applicable(self, order: Order):
        # Example condition: apply surcharge after 9 PM
        current_hour = datetime.now().hour
        return current_hour >= 21

    def apply(self, order: Order):
        return FeeComponent(
            rule_type=RuleType.SURCHARGE,
            name="Night Time Surcharge",
            amount=self.surcharge_amount
        )


class RuleEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def apply_rules(self, order: Order):
        components = []
        for rule in self.rules:
            if rule.is_applicable(order):
                components.append(rule.apply(order))
        return components


class OrderBillGenerator:
    def __init__(self):
        self.rule_engine = RuleEngine()

        # Setup rules
        self.rule_engine.add_rule(BaseDeliveryFeeRule("Base Fee", 20))
        self.rule_engine.add_rule(SurchargeDeliveryRule("Night Surcharge", 5))

    def create_bill_for_order(self, order):
        order.bill = OrderBill(order.id)

    def generate_bill(self, order: Order):
        all_fee_discount_components = self.rule_engine.apply_rules(order)
        self.create_bill_for_order(order)

        self.apply_components_on_order_bill(
            order,
            all_fee_discount_components
        )
    
    def apply_components_on_order_bill(self, order: Order, components: list[FeeComponent]):
        order_bill = order.bill

        for component in components:
            if component.rule_type == RuleType.FEE:
                order_bill.delivery_fee += component.amount
            elif component.rule_type == RuleType.SURCHARGE:
                order_bill.surcharge_fee += component.amount
            elif component.rule_type == RuleType.TAX:
                order_bill.tax += component.amount
            elif component.rule_type == RuleType.DISCOUNT:
                order_bill.discount += component.amount

        order_bill.items_total = sum(item.price for item in order.items)
        order_bill.final_total = (
                order_bill.items_total +
                order_bill.delivery_fee +
                order_bill.surcharge_fee +
                order_bill.tax -
                order_bill.discount
        )
    
    def print_bill(self, bill: OrderBill):
        print(f"Order ID: {bill.order_id}")
        print(f"Items Total: ${bill.items_total}")
        print(f"Delivery Fee: ${bill.delivery_fee}")
        print(f"Surcharge Fee: ${bill.surcharge_fee}")
        print(f"Tax: ${bill.tax}")
        print(f"Discount: ${bill.discount}")
        print(f"Final Total: ${bill.final_total}")


if __name__ == "__main__":
    # Create items
    item1 = Item("Burger", 10)
    item2 = Item("Fries", 5)
    item3 = Item("Soda", 2)

    # Create order
    order = Order(1)
    order.items.extend([item1, item2, item3])

    # Generate bill
    bill_generator = OrderBillGenerator()
    bill_generator.generate_bill(order)
    bill_generator.print_bill(order.bill)






