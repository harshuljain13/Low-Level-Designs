from abc import ABC, abstractmethod
from enum import Enum

class SeatType(Enum):
    """
    Enum for seat types.
    
    OOP Principle: Encapsulation
    - Encapsulates seat type constants in a type-safe way
    - Prevents invalid seat type values
    """
    REGULAR = "regular"
    PREMIUM = "premium"
    RECLINER = "recliner"

# STRATEGY PATTERN for Pricing
class PricingStrategy(ABC):
    """
    Abstract base class for pricing strategies.
    
    Design Pattern: STRATEGY PATTERN
    
    OOP Principles Demonstrated:
    1. ABSTRACTION: Defines pricing interface without implementation
       - Abstract method forces concrete strategies to implement pricing logic
       - Common interface for all pricing algorithms
    
    2. SINGLE RESPONSIBILITY: Only handles price calculation
       - Each strategy focuses on one pricing approach (weekday/weekend/holiday/etc.)
       - Encapsulates both seat type multipliers and contextual pricing
    
    3. OPEN/CLOSED PRINCIPLE: Easy to extend with new strategies
       - Can add new pricing algorithms without modifying existing code
       - Closed for modification, open for extension
    
    Why Strategy Pattern?
    - Pricing logic varies based on day type, season, demand, etc.
    - Same seat can have different prices at different times
    - Easy to A/B test different pricing strategies
    - Clean separation between seat behavior and pricing logic
    """
    
    @abstractmethod
    def calculate_price(self, base_price: float, seat_type: SeatType, **context) -> float:
        """
        Calculate price based on strategy.
        
        Parameters:
            base_price: Base price of the seat
            seat_type: Type of seat (Regular, Premium, Recliner)
            **context: Additional context (show_time, demand_level, etc.)
        
        Returns:
            float: Final calculated price
        """
        pass

class WeekdayPricingStrategy(PricingStrategy):
    """
    Weekday pricing strategy with standard seat type multipliers.
    
    OOP Principle: Strategy Pattern Implementation
    - Concrete implementation for weekday pricing
    - Handles both seat type pricing and weekday context
    """
    
    def __init__(self):
        """
        Initialize weekday pricing with standard multipliers.
        
        OOP Principle: Encapsulation
        - Encapsulates weekday-specific pricing logic
        """
        self._seat_multipliers = {
            SeatType.REGULAR: 1.0,   # Base price for regular seats
            SeatType.PREMIUM: 1.5,   # 50% more for premium seats
            SeatType.RECLINER: 2.0   # 100% more for recliner seats
        }
    
    def calculate_price(self, base_price: float, seat_type: SeatType, **context) -> float:
        """
        Calculate weekday price with seat type multiplier.
        
        OOP Principle: Strategy Pattern
        - Implements specific pricing algorithm for weekdays
        - Combines base price with seat type multiplier
        """
        seat_multiplier = self._seat_multipliers.get(seat_type, 1.0)
        
        # Additional context-based adjustments can be added here
        demand_multiplier = context.get('demand_multiplier', 1.0)
        
        final_price = base_price * seat_multiplier * demand_multiplier
        return round(final_price, 2)

class WeekendPricingStrategy(PricingStrategy):
    """
    Weekend pricing strategy with premium multipliers.
    
    OOP Principle: Strategy Pattern Implementation
    - Different pricing algorithm for weekends
    - Demonstrates flexibility of strategy pattern
    """
    
    def __init__(self, weekend_surcharge: float = 1.2):
        """
        Initialize weekend pricing with surcharge.
        
        OOP Principle: Encapsulation
        - Encapsulates weekend-specific pricing logic
        - Configurable weekend surcharge
        """
        self._weekend_surcharge = weekend_surcharge
        self._seat_multipliers = {
            SeatType.REGULAR: 1.0 * weekend_surcharge,    # 20% weekend surcharge
            SeatType.PREMIUM: 1.5 * weekend_surcharge,    # Premium + weekend surcharge
            SeatType.RECLINER: 2.0 * weekend_surcharge    # Recliner + weekend surcharge
        }
    
    def calculate_price(self, base_price: float, seat_type: SeatType, **context) -> float:
        """
        Calculate weekend price with seat type and weekend multipliers.
        
        OOP Principle: Strategy Pattern
        - Implements weekend-specific pricing algorithm
        - Higher prices due to weekend demand
        """
        seat_multiplier = self._seat_multipliers.get(seat_type, self._weekend_surcharge)
        
        # Additional context-based adjustments
        demand_multiplier = context.get('demand_multiplier', 1.0)
        
        final_price = base_price * seat_multiplier * demand_multiplier
        return round(final_price, 2)

class HolidayPricingStrategy(PricingStrategy):
    """
    Holiday pricing strategy with premium rates.
    
    OOP Principle: Strategy Pattern Implementation
    - Special pricing for holidays and special events
    - Shows extensibility of strategy pattern
    """
    
    def __init__(self, holiday_surcharge: float = 1.5):
        """
        Initialize holiday pricing with higher surcharge.
        
        OOP Principle: Encapsulation
        - Encapsulates holiday-specific pricing logic
        """
        self._holiday_surcharge = holiday_surcharge
        self._seat_multipliers = {
            SeatType.REGULAR: 1.0 * holiday_surcharge,    # 50% holiday surcharge
            SeatType.PREMIUM: 1.5 * holiday_surcharge,    # Premium + holiday surcharge
            SeatType.RECLINER: 2.0 * holiday_surcharge    # Recliner + holiday surcharge
        }
    
    def calculate_price(self, base_price: float, seat_type: SeatType, **context) -> float:
        """
        Calculate holiday price with maximum multipliers.
        
        OOP Principle: Strategy Pattern
        - Implements holiday-specific pricing algorithm
        - Highest prices for special occasions
        """
        seat_multiplier = self._seat_multipliers.get(seat_type, self._holiday_surcharge)
        
        # Additional context-based adjustments
        demand_multiplier = context.get('demand_multiplier', 1.0)
        
        final_price = base_price * seat_multiplier * demand_multiplier
        return round(final_price, 2)

class StudentDiscountPricingStrategy(PricingStrategy):
    """
    Student discount pricing strategy.
    
    OOP Principle: Strategy Pattern Implementation
    - Special pricing for students
    - Shows how to implement discount strategies
    """
    
    def __init__(self, discount_rate: float = 0.2):
        """
        Initialize student discount pricing.
        
        Parameters:
            discount_rate: Percentage discount (0.2 = 20% discount)
        """
        self._discount_multiplier = 1.0 - discount_rate
        self._seat_multipliers = {
            SeatType.REGULAR: 1.0 * self._discount_multiplier,
            SeatType.PREMIUM: 1.5 * self._discount_multiplier,
            SeatType.RECLINER: 2.0 * self._discount_multiplier
        }
    
    def calculate_price(self, base_price: float, seat_type: SeatType, **context) -> float:
        """
        Calculate student discounted price.
        
        OOP Principle: Strategy Pattern
        - Implements student-specific pricing
        - Shows how discounts can be applied uniformly
        """
        seat_multiplier = self._seat_multipliers.get(seat_type, self._discount_multiplier)
        
        final_price = base_price * seat_multiplier
        return round(final_price, 2)

class SeniorDiscountPricingStrategy(PricingStrategy):
    """
    Senior citizen discount pricing strategy.
    
    OOP Principle: Strategy Pattern Implementation
    - Special pricing for senior citizens
    - Similar to student discount but different rates
    """
    
    def __init__(self, discount_rate: float = 0.15):
        """
        Initialize senior discount pricing.
        
        Parameters:
            discount_rate: Percentage discount (0.15 = 15% discount)
        """
        self._discount_multiplier = 1.0 - discount_rate
        self._seat_multipliers = {
            SeatType.REGULAR: 1.0 * self._discount_multiplier,
            SeatType.PREMIUM: 1.5 * self._discount_multiplier,
            SeatType.RECLINER: 2.0 * self._discount_multiplier
        }
    
    def calculate_price(self, base_price: float, seat_type: SeatType, **context) -> float:
        """
        Calculate senior discounted price.
        
        OOP Principle: Strategy Pattern
        - Implements senior-specific pricing
        """
        seat_multiplier = self._seat_multipliers.get(seat_type, self._discount_multiplier)
        
        final_price = base_price * seat_multiplier
        return round(final_price, 2)

# Convenience factory for creating pricing strategies
class PricingStrategyFactory:
    """
    Factory for creating pricing strategies.
    
    Design Pattern: FACTORY PATTERN
    
    OOP Principles:
    1. ENCAPSULATION: Hides strategy creation complexity
    2. SINGLE RESPONSIBILITY: Only creates pricing strategies
    3. OPEN/CLOSED: Easy to add new strategy types
    
    Benefits:
    - Centralized strategy creation
    - Easy to add new strategies
    - Type safety through enum-driven creation
    """
    
    @staticmethod
    def create_weekday_strategy() -> WeekdayPricingStrategy:
        """Create standard weekday pricing strategy."""
        return WeekdayPricingStrategy()
    
    @staticmethod
    def create_weekend_strategy(surcharge: float = 1.2) -> WeekendPricingStrategy:
        """Create weekend pricing strategy with optional custom surcharge."""
        return WeekendPricingStrategy(surcharge)
    
    @staticmethod
    def create_holiday_strategy(surcharge: float = 1.5) -> HolidayPricingStrategy:
        """Create holiday pricing strategy with optional custom surcharge."""
        return HolidayPricingStrategy(surcharge)
    
    @staticmethod
    def create_student_discount_strategy(discount_rate: float = 0.2) -> StudentDiscountPricingStrategy:
        """Create student discount strategy."""
        return StudentDiscountPricingStrategy(discount_rate)
    
    @staticmethod
    def create_senior_discount_strategy(discount_rate: float = 0.15) -> SeniorDiscountPricingStrategy:
        """Create senior discount strategy."""
        return SeniorDiscountPricingStrategy(discount_rate)
