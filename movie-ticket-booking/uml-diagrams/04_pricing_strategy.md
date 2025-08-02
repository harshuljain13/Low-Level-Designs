# Pricing Strategy Pattern UML Diagram

## Step 4: Pricing Strategy Pattern

```mermaid
classDiagram
    class PricingStrategy {
        <<abstract>>
        +calculate_price(base_price: float)*: float
    }
    
    class DefaultPricingStrategy {
        -multiplier: float
        +calculate_price(base_price: float): float
    }
    
    class HolidayPricingStrategy {
        -holiday_surcharge: float
        +calculate_price(base_price: float): float
    }
    
    class StudentDiscountPricingStrategy {
        -discount_rate: float
        +calculate_price(base_price: float): float
    }
    
    class CompositePricingStrategy {
        -strategies: List[PricingStrategy]
        -combination_method: str
        +calculate_price(base_price: float): float
        +add_strategy(strategy: PricingStrategy): void
        +remove_strategy(strategy: PricingStrategy): void
    }
    
    class PricingStrategyFactory {
        +create_default_strategy(): DefaultPricingStrategy
        +create_holiday_strategy(holiday_surcharge: float): HolidayPricingStrategy
        +create_student_discount_strategy(discount_rate: float): StudentDiscountPricingStrategy
        +create_composite_strategy(strategies: List[PricingStrategy], combination_method: str): CompositePricingStrategy
    }
    
    PricingStrategy <|-- DefaultPricingStrategy
    PricingStrategy <|-- HolidayPricingStrategy
    PricingStrategy <|-- StudentDiscountPricingStrategy
    PricingStrategy <|-- CompositePricingStrategy
    PricingStrategyFactory ..> PricingStrategy : creates
    Seat ..> PricingStrategy : uses strategy
```

## Description
This diagram shows the Strategy pattern implementation for pricing. The abstract PricingStrategy class defines the interface, and concrete strategies implement different pricing algorithms (default, holiday, student discount, composite). The PricingStrategyFactory creates different strategy instances. The Seat class uses these strategies to calculate prices. 