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
       - Encapsulates both seat type multipliers

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
    def calculate_price(self, base_price: float) -> float:
        """
        Calculate price based on strategy.

        Parameters:
            base_price: Base price of the seat
            seat_type: Type of seat (Regular, Premium, Recliner)

        Returns:
            float: Final calculated price
        """
        pass


class DefaultPricingStrategy(PricingStrategy):
    """
    Weekday pricing strategy with standard seat type multipliers.

    OOP Principle: Strategy Pattern Implementation
    - Concrete implementation for weekday pricing
    """

    def __init__(self):
        """
        Initialize weekday pricing with standard multipliers.

        OOP Principle: Encapsulation
        - Encapsulates weekday-specific pricing logic
        """
        self.multiplier = 1.0

    def calculate_price(self, base_price: float) -> float:
        """
        Calculate weekday price with seat type multiplier.

        OOP Principle: Strategy Pattern
        - Implements specific pricing algorithm for weekdays
        - Combines base price with seat type multiplier
        """
        final_price = base_price * self.multiplier
        return round(final_price, 2)


class HolidayPricingStrategy(PricingStrategy):
    """
    Holiday pricing strategy with premium rates.

    OOP Principle: Strategy Pattern Implementation
    - Special pricing for holidays and special events
    - Shows extensibility of strategy pattern
    """

    def __init__(self, holiday_surcharge: float = 0.5):
        """
        Initialize holiday pricing with higher surcharge.

        OOP Principle: Encapsulation
        - Encapsulates holiday-specific pricing logic
        """
        self.multiplier = 1 + holiday_surcharge

    def calculate_price(self, base_price: float) -> float:
        """
        Calculate holiday price with maximum multipliers.

        OOP Principle: Strategy Pattern
        - Implements holiday-specific pricing algorithm
        - Highest prices for special occasions
        """

        final_price = base_price * self.multiplier
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
        self.multiplier = 1.0 - discount_rate

    def calculate_price(self, base_price: float) -> float:
        """
        Calculate student discounted price.

        OOP Principle: Strategy Pattern
        - Implements student-specific pricing
        - Shows how discounts can be applied uniformly
        """
        final_price = base_price * self.multiplier
        return round(final_price, 2)


# COMPOSITE STRATEGY PATTERN for combining multiple strategies
class CompositePricingStrategy(PricingStrategy):
    """
    Composite strategy that combines multiple pricing strategies.

    Design Pattern: COMPOSITE PATTERN + STRATEGY PATTERN

    OOP Principles Demonstrated:
    1. COMPOSITION: Combines multiple strategies into one
    2. OPEN/CLOSED: Can add new strategies without modifying existing ones
    3. SINGLE RESPONSIBILITY: Each component strategy handles one aspect
    4. FLEXIBILITY: Dynamic combination of strategies

    Why Composite Strategy?
    - Avoid creating strategies for every possible combination
    - Reuse existing strategies in different combinations
    - Easy to apply multiple discounts or surcharges
    - Maintains clean separation of concerns
    """

    def __init__(
        self, strategies: list[PricingStrategy], combination_method: str = "sequential"
    ):
        """
        Initialize composite strategy with multiple strategies.

        Parameters:
            strategies: List of pricing strategies to combine
            combination_method: How to combine strategies ("sequential", "parallel", "custom")
        """
        if not strategies:
            raise ValueError("At least one strategy must be provided")

        self._strategies = strategies
        self._combination_method = combination_method

    def calculate_price(self, base_price: float) -> float:
        """
        Calculate price by combining multiple strategies.

        OOP Principle: Composite Pattern
        - Delegates to component strategies
        - Combines results based on combination method
        """
        if self._combination_method == "sequential":
            return self._calculate_sequential_price(base_price)
        elif self._combination_method == "parallel":
            return self._calculate_parallel_price(base_price)
        else:
            raise ValueError(f"Unknown combination method: {self._combination_method}")

    def _calculate_sequential_price(self, base_price: float) -> float:
        """
        Apply strategies sequentially (each builds on previous result).

        Example: Base price → Weekday pricing → Student discount
        """
        current_price = base_price

        for strategy in self._strategies:
            current_price = strategy.calculate_price(current_price)

        return round(current_price, 2)

    def _calculate_parallel_price(self, base_price: float) -> float:
        """
        Apply strategies in parallel and combine results.

        Example: Average of multiple strategy results
        """
        prices = []

        for strategy in self._strategies:
            price = strategy.calculate_price(base_price)
            prices.append(price)

        # Calculate average (can be modified for other combination logic)
        final_price = sum(prices) / len(prices)
        return round(final_price, 2)

    def add_strategy(self, strategy: PricingStrategy) -> None:
        """Add a strategy to the composite."""
        self._strategies.append(strategy)

    def remove_strategy(self, strategy: PricingStrategy) -> None:
        """Remove a strategy from the composite."""
        if strategy in self._strategies:
            self._strategies.remove(strategy)


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
    def create_default_strategy() -> DefaultPricingStrategy:
        """Create default pricing strategy."""
        return DefaultPricingStrategy()

    @staticmethod
    def create_holiday_strategy(
        holiday_surcharge: float = 1.5,
    ) -> HolidayPricingStrategy:
        """Create holiday pricing strategy with optional custom surcharge."""
        return HolidayPricingStrategy(holiday_surcharge)

    @staticmethod
    def create_student_discount_strategy(
        discount_rate: float = 0.2,
    ) -> StudentDiscountPricingStrategy:
        """Create student discount strategy."""
        return StudentDiscountPricingStrategy(discount_rate)

    @staticmethod
    def create_composite_strategy(
        strategies: list[PricingStrategy], combination_method: str = "sequential"
    ) -> CompositePricingStrategy:
        """Create composite strategy combining multiple strategies."""
        return CompositePricingStrategy(strategies, combination_method)
