#!/usr/bin/env python3
"""
Example usage of the comprehensive Screen seat management system.

This example demonstrates:
1. Creating different screen types with custom layouts
2. Managing seats with 2D grid structure
3. Finding adjacent seats for group bookings
4. Thread-safe operations for concurrent booking
5. Different seat management operations

OOP Principles Demonstrated:
- Factory Pattern for screen creation
- Inheritance with different screen types
- Encapsulation of seat management logic
- Polymorphism in screen configurations
"""

from Screen import ScreenFactory, ScreenType, SeatLayout
from Seat import SeatType
from SeatPricingStrategy import PricingStrategyFactory


def demonstrate_basic_screen_operations():
    """Demonstrate basic screen and seat management operations."""
    print("=== Basic Screen Operations ===")

    # Create a standard regular screen
    screen = ScreenFactory.create_standard_screen("SCR001", "Main Screen 1")

    print(f"Created: {screen}")
    print(f"Total capacity: {screen.total_capacity}")
    print(f"Available seats: {screen.available_count}")
    print(f"Screen type: {screen.screen_type.value}")
    print()

    # Get some seats and book them
    available_seats = screen.get_available_seats()
    print(f"Found {len(available_seats)} available seats")

    # Book first 5 seats
    for i in range(5):
        seat = available_seats[i]
        # Using weekend pricing for booking demonstration
        pricing_strategy = PricingStrategyFactory.create_weekend_strategy()
        booking_price = seat.calculate_price(100.0, pricing_strategy)  # Base price 100
        seat.book_seat()
        print(f"Booked {seat.seat_id} at price: ₹{booking_price}")

    print(
        f"After booking - Available: {screen.available_count}, Occupied: {screen.occupied_count}"
    )
    print(f"Occupancy rate: {screen.get_occupancy_rate():.1f}%")
    print()


def demonstrate_custom_layout():
    """Demonstrate creating screens with custom layouts."""
    print("=== Custom Layout Screen ===")

    # Create a custom layout - like a small intimate theater
    # Row 1: 8 seats, Row 2: 10 seats, Row 3: 12 seats, Row 4: 10 seats, Row 5: 8 seats
    seats_per_row = [8, 10, 12, 10, 8]
    layout = SeatLayout(total_rows=5, seats_per_row=seats_per_row)

    # Create a premium screen with this layout
    screen = ScreenFactory.create_screen(
        ScreenType.PREMIUM, "SCR_PREMIUM_001", "VIP Premium Hall", layout
    )

    print(f"Created custom layout screen: {screen}")
    print(f"Layout - Total rows: {layout.total_rows}")
    print(f"Seats per row: {layout.seats_per_row}")
    print(f"Total capacity: {layout.total_capacity}")
    print()

    # Show seat map structure
    seat_map = screen.get_seat_map()
    print("Seat Map (showing seat IDs):")
    for row_idx, row in enumerate(seat_map, 1):
        print(
            f"Row {row_idx:2d}: {' '.join(seat[:12] if seat else '____' for seat in row)}"
        )
    print()


def demonstrate_imax_screen():
    """Demonstrate IMAX screen with specialized configuration."""
    print("=== IMAX Screen Configuration ===")

    # Create IMAX screen with factory method
    imax_screen = ScreenFactory.create_imax_screen("IMAX_001", "IMAX Experience Hall")

    print(f"Created: {imax_screen}")
    print(f"IMAX capacity: {imax_screen.total_capacity}")

    # Show distribution of seat types in IMAX
    premium_seats = imax_screen.get_available_seats_by_type(SeatType.PREMIUM)
    recliner_seats = imax_screen.get_available_seats_by_type(SeatType.RECLINER)

    print(f"Premium seats: {len(premium_seats)}")
    print(f"Recliner seats: {len(recliner_seats)}")
    print()

    # Show first few rows of IMAX layout
    seat_map = imax_screen.get_seat_map()
    print("IMAX Seat Layout (first 5 rows):")
    for row_idx, row in enumerate(seat_map[:5], 1):
        seat_ids = [
            seat[-6:] if seat else "______" for seat in row
        ]  # Show last 6 chars
        print(f"Row {row_idx}: {' '.join(seat_ids)}")
    print()


def demonstrate_seat_finding_operations():
    """Demonstrate advanced seat finding operations."""
    print("=== Advanced Seat Finding ===")

    screen = ScreenFactory.create_standard_screen("SCR002", "Main Screen 2")

    # Find adjacent seats for group booking
    print("Finding adjacent seats for group booking:")

    # Try to find 3 adjacent seats in row 5
    adjacent_groups = screen.get_adjacent_seats(row=5, column=1, count=3)
    if adjacent_groups:
        seats = adjacent_groups[0]  # Take first group found
        print(f"Found 3 adjacent seats in row 5: {[s.seat_id for s in seats]}")

        # Book these adjacent seats
        for seat in seats:
            seat.book_seat()
        print("Booked the adjacent seats")
    else:
        print("No 3 adjacent seats found in row 5")

    # Try to find 2 adjacent seats in row 8
    adjacent_groups = screen.get_adjacent_seats(row=8, column=5, count=2)
    if adjacent_groups:
        seats = adjacent_groups[0]
        print(f"Found 2 adjacent seats in row 8: {[s.seat_id for s in seats]}")

    print()


def demonstrate_seat_lookup_operations():
    """Demonstrate different ways to lookup and access seats."""
    print("=== Seat Lookup Operations ===")

    screen = ScreenFactory.create_standard_screen("SCR003", "Main Screen 3")

    # Get seat by position
    seat_5_10 = screen.get_seat_by_position(5, 10)
    if seat_5_10:
        print(f"Seat at Row 5, Column 10: {seat_5_10.seat_id}")
        print(f"Seat type: {seat_5_10.seat_type.value}")

    # Get seat by ID
    if seat_5_10:
        found_seat = screen.get_seat_by_id(seat_5_10.seat_id)
        print(f"Found seat by ID {seat_5_10.seat_id}: {found_seat is not None}")

    # Get seats by type
    premium_seats = screen.get_available_seats_by_type(SeatType.PREMIUM)
    recliner_seats = screen.get_available_seats_by_type(SeatType.RECLINER)
    regular_seats = screen.get_available_seats_by_type(SeatType.REGULAR)

    print(f"Available Premium seats: {len(premium_seats)}")
    print(f"Available Recliner seats: {len(recliner_seats)}")
    print(f"Available Regular seats: {len(regular_seats)}")
    print()


def demonstrate_concurrent_booking_safety():
    """Demonstrate thread-safe operations for concurrent booking."""
    print("=== Thread Safety Demonstration ===")

    import threading
    import time
    import random

    screen = ScreenFactory.create_standard_screen("SCR_THREAD", "Thread Safe Screen")

    def booking_worker(worker_id: int):
        """Simulate a booking worker that tries to book random seats."""
        for i in range(3):  # Each worker tries to book 3 seats
            try:
                available_seats = screen.get_available_seats()
                if available_seats:
                    # Pick a random available seat
                    seat = random.choice(available_seats)
                    success = seat.book_seat()
                    if success:
                        print(f"Worker {worker_id}: Successfully booked {seat.seat_id}")
                    else:
                        print(
                            f"Worker {worker_id}: Failed to book {seat.seat_id} (already booked)"
                        )

                    time.sleep(
                        0.01
                    )  # Small delay to increase chance of race conditions
                else:
                    print(f"Worker {worker_id}: No available seats")
                    break
            except Exception as e:
                print(f"Worker {worker_id}: Error - {e}")

    # Create multiple threads to simulate concurrent booking
    threads = []
    for i in range(3):  # 3 concurrent booking workers
        thread = threading.Thread(target=booking_worker, args=(i + 1,))
        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(
        f"Final state - Available: {screen.available_count}, Occupied: {screen.occupied_count}"
    )
    print()


def demonstrate_pricing_with_screen_context():
    """Demonstrate how screens can be used with pricing strategies."""
    print("=== Pricing with Screen Context ===")

    screen = ScreenFactory.create_imax_screen("IMAX_PRICING", "IMAX Pricing Demo")

    # Get different types of seats
    premium_seat = screen.get_available_seats_by_type(SeatType.PREMIUM)[0]
    recliner_seat = screen.get_available_seats_by_type(SeatType.RECLINER)[0]

    # Try different pricing strategies
    base_price = 150.0  # Base IMAX price

    pricing_strategies = [
        ("Weekday", PricingStrategyFactory.create_weekday_strategy()),
        ("Weekend", PricingStrategyFactory.create_weekend_strategy()),
        ("Holiday", PricingStrategyFactory.create_holiday_strategy()),
    ]

    print(f"IMAX Pricing for base price ₹{base_price}")
    print("-" * 50)

    for strategy_name, strategy in pricing_strategies:
        premium_price = premium_seat.calculate_price(base_price, strategy)
        recliner_price = recliner_seat.calculate_price(base_price, strategy)

        print(
            f"{strategy_name:8} - Premium: ₹{premium_price:6.2f}, Recliner: ₹{recliner_price:6.2f}"
        )

    print()


def main():
    """Run all demonstration examples."""
    print("Screen Seat Management System - Comprehensive Demo")
    print("=" * 55)
    print()

    try:
        demonstrate_basic_screen_operations()
        demonstrate_custom_layout()
        demonstrate_imax_screen()
        demonstrate_seat_finding_operations()
        demonstrate_seat_lookup_operations()
        demonstrate_concurrent_booking_safety()
        demonstrate_pricing_with_screen_context()

        print("✅ All demonstrations completed successfully!")

    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
