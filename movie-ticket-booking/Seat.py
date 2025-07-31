from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime

# Import pricing strategies from separate module
from SeatPricingStrategy import PricingStrategy, SeatType, PricingStrategyFactory


class SeatStatus(Enum):
    """
    Enum for seat status.

    OOP Principle: Encapsulation
    - Type-safe seat status management
    - Clear state definitions for seat availability
    """

    AVAILABLE = "available"
    BOOKED = "booked"
    BLOCKED = "blocked"


class Seat(ABC):
    """
    Abstract base class for all seat types.

    OOP Principles Demonstrated:
    1. ABSTRACTION: Abstract class defines seat interface without implementation details
       - Abstract method get_seat_type() forces subclasses to implement their specific behavior
       - Common interface for all seat operations

    2. ENCAPSULATION: Private attributes with controlled access
       - Private attributes prevent direct manipulation
       - Properties provide controlled access to seat data
       - Validation ensures data integrity

    3. INHERITANCE: Base class for specialized seat types
       - Common functionality (ID, number, status) defined once
       - Subclasses add seat-type-specific behavior

    4. STRATEGY PATTERN: Uses strategy for price calculation
       - Pricing strategy is passed to calculate_price method
       - Flexible pricing without modifying seat classes

    Why this design?
    - Seat has base price but actual pricing depends on strategy
    - Same seat can have different prices at different times
    - Clean separation between seat behavior and pricing logic
    - Pricing strategies are in separate module for better organization
    """

    def __init__(self, seat_id: str, seat_number: str, base_price: float):
        """
        Initialize seat with basic information.

        OOP Principle: Encapsulation
        - Constructor validates and encapsulates seat data
        - Sets up private attributes with proper defaults
        - Base price is stored but actual price calculated via strategy
        """
        if not seat_id or not seat_id.strip():
            raise ValueError("Seat ID cannot be empty")
        if not seat_number or not seat_number.strip():
            raise ValueError("Seat number cannot be empty")
        if base_price < 0:
            raise ValueError("Base price cannot be negative")

        self._seat_id = seat_id
        self._seat_number = seat_number
        self._base_price = base_price
        self._status = SeatStatus.AVAILABLE
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

    # Properties demonstrate ENCAPSULATION
    @property
    def seat_id(self) -> str:
        """
        Get seat ID (read-only).

        OOP Principle: Encapsulation
        - Controlled read access to private attribute
        - Prevents external modification of seat identifier
        """
        return self._seat_id

    @property
    def seat_number(self) -> str:
        """
        Get seat number (read-only).

        OOP Principle: Encapsulation
        - Safe access to seat number
        """
        return self._seat_number

    @property
    def base_price(self) -> float:
        """
        Get base price.

        OOP Principle: Encapsulation
        - Controlled access to base pricing
        - Actual price calculated via strategy
        """
        return self._base_price

    @property
    def status(self) -> SeatStatus:
        """
        Get seat status.

        OOP Principle: Encapsulation
        - Type-safe access to seat status
        """
        return self._status

    def is_available(self) -> bool:
        """
        Check if seat is available for booking.

        OOP Principle: Encapsulation
        - Encapsulates availability logic
        - Hides internal status representation
        """
        return self._status == SeatStatus.AVAILABLE

    def is_booked(self) -> bool:
        """
        Check if seat is booked.

        OOP Principle: Encapsulation
        - Encapsulates booked status logic
        - Hides internal status representation
        """
        return self._status == SeatStatus.BOOKED

    def is_blocked(self) -> bool:
        """
        Check if seat is blocked.

        OOP Principle: Encapsulation
        - Encapsulates blocked status logic
        - Hides internal status representation
        """
        return self._status == SeatStatus.BLOCKED

    def book_seat(self) -> None:
        """
        Book the seat.

        OOP Principle: Encapsulation
        - Encapsulates booking logic
        - Hides internal booking implementation
        """
        if self.is_available():
            self._status = SeatStatus.BOOKED
            self._updated_at = datetime.now()
        else:
            raise ValueError("Seat is not available for booking")

    def release_seat(self) -> None:
        """
        Release the seat.

        OOP Principle: Encapsulation
        - Encapsulates release logic
        - Hides internal release implementation
        """
        if self.is_booked():
            self._status = SeatStatus.AVAILABLE
            self._updated_at = datetime.now()
        else:
            raise ValueError("Seat is not booked")

    @abstractmethod
    def get_seat_type(self) -> SeatType:
        """
        Get seat type - must be implemented by subclasses.

        OOP Principle: Abstraction
        - Forces subclasses to define their type
        - Enables polymorphic behavior
        """
        pass

    def calculate_price(self, pricing_strategy: PricingStrategy) -> float:
        """
        Calculate seat price using provided pricing strategy.

        OOP Principles:
        1. STRATEGY PATTERN: Delegates pricing to strategy object
        2. DEPENDENCY INJECTION: Strategy provided as parameter
        3. SINGLE RESPONSIBILITY: Seat handles seat logic, strategy handles pricing
        4. OPEN/CLOSED: Can use new pricing strategies without modifying seat
        5. SEPARATION OF CONCERNS: Pricing logic separated into different module

        This is the key method that demonstrates Strategy pattern in action!

        Parameters:
            pricing_strategy: Strategy to use for price calculation (from SeatPricingStrategy module)
            **context: Additional context for pricing (demand_level, etc.)

        Returns:
            float: Calculated price based on strategy

        Example Usage:
            from SeatPricingStrategy import WeekdayPricingStrategy, WeekendPricingStrategy

            holiday_price = seat.calculate_price(HolidayPricingStrategy())
        """
        print(
            "Calculating price for seat: ",
            self._seat_id,
            " with base price: ",
            self._base_price,
        )
        return pricing_strategy.calculate_price(self._base_price)

    def __str__(self) -> str:
        """
        String representation.

        OOP Principle: Polymorphism
        - Calls polymorphic get_seat_type() method
        - Same method works for all subclasses
        """
        return f"{self.get_seat_type().value.title()} Seat {self._seat_number} (ID: {self._seat_id})"

    def __repr__(self) -> str:
        """
        Developer-friendly representation.

        OOP Principle: Polymorphism
        - Uses class name dynamically
        """
        return f"{self.__class__.__name__}(id={self._seat_id}, \
            number={self._seat_number})"


class RegularSeat(Seat):
    """
    Regular seat type.

    OOP Principles Demonstrated:
    1. INHERITANCE: Inherits from Seat base class
       - Gets all common functionality (booking, status management)
       - Only needs to implement seat-specific behavior

    2. POLYMORPHISM: Implements abstract method
       - Provides regular-seat-specific implementation of get_seat_type()
       - Can be used anywhere Seat is expected

    3. LISKOV SUBSTITUTION PRINCIPLE: Can replace Seat
       - Behaves correctly in all contexts expecting Seat
       - Maintains contract defined by parent class

    4. SINGLE RESPONSIBILITY: Only handles seat type identification
       - Pricing logic handled by separate strategy classes
       - Clean separation of concerns
    """

    def get_seat_type(self) -> SeatType:
        """
        Return regular seat type.

        OOP Principle: Polymorphism
        - Concrete implementation of abstract method
        - Enables polymorphic behavior in pricing strategies
        """
        return SeatType.REGULAR


class PremiumSeat(Seat):
    """
    Premium seat type.

    OOP Principles: Same as RegularSeat but for premium type
    - Inherits all seat behavior
    - Only implements seat type identification
    - Pricing handled by strategies in separate module
    """

    def get_seat_type(self) -> SeatType:
        """Return premium seat type."""
        return SeatType.PREMIUM


class ReclinerSeat(Seat):
    """
    Recliner seat type.

    OOP Principles: Same as RegularSeat but for recliner type
    - Inherits all seat behavior
    - Only implements seat type identification
    - Pricing handled by strategies in separate module
    """

    def get_seat_type(self) -> SeatType:
        """Return recliner seat type."""
        return SeatType.RECLINER


class SeatFactory:
    """
    Factory class to create different types of seats.

    Design Pattern: FACTORY PATTERN

    OOP Principles Demonstrated:
    1. ENCAPSULATION: Hides seat creation complexity
       - Clients don't need to know specific seat constructors
       - Centralizes creation logic and validation

    2. SINGLE RESPONSIBILITY: Only responsible for seat creation
       - Separates creation logic from seat behavior
       - Pricing logic handled by separate strategy module
       - Easy to modify creation process

    3. POLYMORPHISM: Returns Seat interface
       - Clients work with Seat interface, not concrete types
       - Actual seat type determined at runtime

    Benefits:
    - Consistent validation across all seat types
    - Easy to add new seat types
    - Type safety through enum-driven creation
    - Centralized seat creation logic
    - Clean separation from pricing concerns
    """

    @staticmethod
    def create_seat(
        seat_type: SeatType, seat_id: str, seat_number: str, base_price: float
    ) -> Seat:
        """
        Create seat based on seat type.

        OOP Principles:
        1. FACTORY PATTERN: Centralizes object creation
        2. POLYMORPHISM: Returns Seat interface
        3. TYPE SAFETY: Uses enum for seat type
        4. SEPARATION OF CONCERNS: Only handles seat creation, not pricing

        Parameters:
            seat_type: Enum specifying which seat type to create
            seat_id, seat_number, base_price: Common seat attributes

        Returns:
            Seat: Concrete seat instance (RegularSeat, PremiumSeat, or ReclinerSeat)

        Raises:
            ValueError: If unsupported seat type

        Note:
            Pricing is handled separately via strategies from SeatPricingStrategy module
        """
        if seat_type == SeatType.REGULAR:
            return RegularSeat(seat_id, seat_number, base_price)

        elif seat_type == SeatType.PREMIUM:
            return PremiumSeat(seat_id, seat_number, base_price)

        elif seat_type == SeatType.RECLINER:
            return ReclinerSeat(seat_id, seat_number, base_price)

        else:
            raise ValueError(f"Invalid seat type: {seat_type}")

    @staticmethod
    def create_seat_row(
        seat_type: SeatType, row_number: int, seats_count: int, base_price: float
    ) -> list[Seat]:
        """
        Create a row of seats of the same type.

        OOP Principle: Factory Pattern Extension
        - Convenient method for bulk seat creation
        - Maintains consistent naming convention
        - Separates seat creation from pricing logic
        """
        seats = []
        for seat_num in range(1, seats_count + 1):
            seat_id = f"R{row_number:02d}S{seat_num:02d}"
            seat_number = f"{row_number}{chr(64 + seat_num)}"  # 1A, 1B, 1C, etc.
            seat = SeatFactory.create_seat(seat_type, seat_id, seat_number, base_price)
            seats.append(seat)
        return seats


if __name__ == "__main__":
    # Create a premium seat for testing
    premium_seat = SeatFactory.create_seat(
        SeatType.PREMIUM, "TEST001", "S1", base_price=100.0
    )

    print(f"Testing with: {premium_seat}")
    print(f"Base price: ₹{premium_seat.base_price}")

    default_pricing_strategy = PricingStrategyFactory.create_default_strategy()
    print(f"Default pricing strategy: {default_pricing_strategy}")
    print(
        f"Default seat price: {premium_seat.calculate_price(default_pricing_strategy)}"
    )

    holiday_pricing_strategy = PricingStrategyFactory.create_holiday_strategy(
        holiday_surcharge=0.5
    )
    print(f"Holiday pricing strategy: {holiday_pricing_strategy}")
    print(
        f"Holiday seat price: {premium_seat.calculate_price(holiday_pricing_strategy)}"
    )

    student_discount_pricing_strategy = (
        PricingStrategyFactory.create_student_discount_strategy(discount_rate=0.2)
    )
    print(f"Student discount pricing strategy: {student_discount_pricing_strategy}")
    print(
        f"Student discount seat price: {premium_seat.calculate_price(student_discount_pricing_strategy)}"
    )

    composite_pricing_strategy = PricingStrategyFactory.create_composite_strategy(
        [
            default_pricing_strategy,
            holiday_pricing_strategy,
            student_discount_pricing_strategy,
        ],
        combination_method="sequential",
    )
    print(f"Composite pricing strategy: {composite_pricing_strategy}")
    print(
        f"Composite seat price: {premium_seat.calculate_price(composite_pricing_strategy)}"
    )
