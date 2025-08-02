# Booking Manager UML Diagram

## Seat Booking & Management

```mermaid
classDiagram
    class BookingManager {
        -_blocked_seats: Dict[str, Dict[str, datetime]]
        -_block_timeout: timedelta
        +get_available_seats(show: Show): List[str]
        +is_seat_available(show: Show, seat_id: str): bool
        +get_seat_price(show: Show, seat_id: str): float
        +book_seat(show: Show, seat_id: str): bool
        +cancel_seat_booking(show: Show, seat_id: str): bool
        +book_multiple_seats(show: Show, seat_ids: List[str]): Dict[str, bool]
        +block_seat(show: Show, seat_id: str): bool
        +unblock_seat(show: Show, seat_id: str): bool
        +block_multiple_seats(show: Show, seat_ids: List[str]): Dict[str, bool]
        +get_blocked_seats(show: Show): List[str]
        +get_show_statistics(show: Show): Dict
        +get_show_revenue(show: Show): float
        +cleanup_expired_blocks(): int
        +_find_seat_in_layout(show: Show, seat_id: str): Seat
        +_is_seat_blocked(show_id: str, seat_id: str): bool
        +_get_blocked_seats_for_show(show_id: str): List[str]
        +_unblock_seat(show_id: str, seat_id: str): bool
    }
    
    class Show {
        -_show_id: str
        -_show_time: datetime
        -_status: ShowStatus
        -_pricing_strategy: PricingStrategy
        +show_id: str
        +show_time: datetime
        +status: ShowStatus
        +pricing_strategy: PricingStrategy
        +seat_layout: SeatLayout
        +calculate_seat_price(seat_row_num: int, seat_col_num: int): float
    }
    
    class SeatLayout {
        -_num_rows: int
        -_seats_per_row: List[int]
        -_seats: List[List[Seat]]
        +num_rows: int
        +seats_per_row: List[int]
        +get_seat(row: int, col: int): Seat
        +get_seat_by_id(seat_id: str): Seat
        +get_all_seats(): List[Seat]
    }
    
    class Seat {
        -_seat_id: str
        -_row_num: int
        -_col_num: int
        -_seat_type: SeatType
        -_status: SeatStatus
        -_price: float
        +seat_id: str
        +row_num: int
        +col_num: int
        +seat_type: SeatType
        +status: SeatStatus
        +price: float
        +is_available(): bool
        +book(): bool
        +release(): void
    }
    
    class PricingStrategy {
        <<abstract>>
        +calculate_price(base_price: float): float
    }
    
    class SeatStatus {
        <<enumeration>>
        AVAILABLE
        BOOKED
        BLOCKED
        MAINTENANCE
    }
    
    class SeatType {
        <<enumeration>>
        REGULAR
        PREMIUM
        VIP
        COUPLE
    }
    
    BookingManager ..> Show : works with
    BookingManager ..> Seat : manages
    BookingManager ..> SeatLayout : accesses
    Show *-- SeatLayout : has
    Show *-- PricingStrategy : uses
    SeatLayout *-- Seat : contains
    Seat *-- SeatStatus : has
    Seat *-- SeatType : has
```

## Description
This diagram shows the BookingManager's responsibilities for seat booking, availability management, and financial operations. It handles seat blocking, booking, pricing, and provides statistics and revenue calculations. The BookingManager manages the complete seat lifecycle from availability checking to booking and revenue tracking. The layout is balanced with both vertical and horizontal elements for better visual distribution. 