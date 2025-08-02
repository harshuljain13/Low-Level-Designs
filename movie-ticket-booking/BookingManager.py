"""
This module contains the BookingManager class, which handles seat booking
and seat state management.

Design Pattern: MANAGER PATTERN (Service Layer)
OOP Principles:
- Single Responsibility: Manages seat booking operations only
- Encapsulation: Encapsulates booking management logic
- Composition: Works with Show's seat layout
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from Show import Show, ShowStatus
from Seat import Seat, SeatStatus


class BookingManager:
    """
    BookingManager class - Handles seat booking and seat state management.

    Design Pattern: MANAGER PATTERN (Service Layer)
    OOP Principles:
    - Single Responsibility: Manages seat booking operations only
    - Encapsulation: Encapsulates booking management logic
    - Composition: Works with Show's seat layout
    """

    def __init__(self):
        self._blocked_seats: Dict[str, Dict[str, datetime]] = (
            {}
        )  # show_id -> {seat_id: block_time}
        self._block_timeout = timedelta(
            minutes=15
        )  # 15 minutes timeout for blocked seats

    # Seat Availability Management
    def get_available_seats(self, show: Show) -> List[str]:
        """Get list of available seat IDs for a show."""
        if show.status != ShowStatus.SCHEDULED:
            return []

        available_seats = []
        for row in range(show.seat_layout.num_rows):
            for col in range(show.seat_layout.seats_per_row[row]):
                seat = show.seat_layout.get_seat(row, col)
                if seat and seat.status == SeatStatus.AVAILABLE:
                    # Check if seat is not blocked
                    if not self._is_seat_blocked(show.show_id, seat.seat_id):
                        available_seats.append(seat.seat_id)

        return available_seats

    def is_seat_available(self, show: Show, seat_id: str) -> bool:
        """Check if a specific seat is available for booking."""
        if show.status != ShowStatus.SCHEDULED:
            return False

        # Find the seat in the layout
        seat = self._find_seat_in_layout(show, seat_id)
        if not seat:
            return False

        # Check if seat is available and not blocked
        return (seat.status == SeatStatus.AVAILABLE and 
                not self._is_seat_blocked(show.show_id, seat_id))

    def get_seat_price(self, show: Show, seat_id: str) -> Optional[float]:
        """Get the price for a specific seat in a show using pricing strategy."""
        return show.calculate_seat_price(seat_id)

    # Seat Booking Management
    def book_seat(self, show: Show, seat_id: str) -> bool:
        """Book a seat for a show."""
        if not self.is_seat_available(show, seat_id):
            return False

        seat = self._find_seat_in_layout(show, seat_id)
        if seat:
            seat.book_seat()
            self._unblock_seat(show.show_id, seat_id)
            return True

        return False

    def cancel_seat_booking(self, show: Show, seat_id: str) -> bool:
        """Cancel a seat booking."""
        seat = self._find_seat_in_layout(show, seat_id)
        if seat and seat.status == SeatStatus.BOOKED:
            seat.release_seat()
            return True
        return False

    def book_multiple_seats(self, show: Show, seat_ids: List[str]) -> Dict[str, bool]:
        """Book multiple seats and return results for each seat."""
        results = {}

        for seat_id in seat_ids:
            results[seat_id] = self.book_seat(show, seat_id)

        return results

    # Seat Blocking Management (for booking process)
    def block_seat(self, show: Show, seat_id: str) -> bool:
        """Block a seat temporarily for booking process."""
        if not self.is_seat_available(show, seat_id):
            print(f"Seat {seat_id} is not available")
            return False

        if show.show_id not in self._blocked_seats:
            self._blocked_seats[show.show_id] = {}

        self._blocked_seats[show.show_id][seat_id] = datetime.now()
        print(f"Blocked seat {seat_id}: Success")
        return True

    def unblock_seat(self, show: Show, seat_id: str) -> bool:
        """Unblock a seat."""
        return self._unblock_seat(show.show_id, seat_id)

    def unblock_multiple_seats(self, show: Show, seat_ids: List[str]) -> Dict[str, bool]:
        """Unblock multiple seats and return results for each seat."""
        results = {}
        for seat_id in seat_ids:
            results[seat_id] = self.unblock_seat(show, seat_id)
        print(f"Unblocked seats: {results}")
        return results

    def block_multiple_seats(self, show: Show, seat_ids: List[str]) -> Dict[str, bool]:
        """Block multiple seats and return results for each seat."""
        results = {}

        for seat_id in seat_ids:
            results[seat_id] = self.block_seat(show, seat_id)
        print(f"Blocked seats: {results}")
        return results

    def get_blocked_seats(self, show: Show) -> List[str]:
        """Get list of currently blocked seats for a show."""
        return self._get_blocked_seats_for_show(show.show_id)

    # Show Statistics
    def get_show_statistics(self, show: Show) -> Dict[str, any]:
        """Get statistics for a specific show."""
        total_seats = 0
        booked_seats = 0
        available_seats = 0

        for row in range(show.seat_layout.num_rows):
            for col in range(show.seat_layout.seats_per_row[row]):
                seat = show.seat_layout.get_seat(row, col)
                if seat:
                    total_seats += 1
                    if seat.status == SeatStatus.BOOKED:
                        booked_seats += 1
                    elif seat.status == SeatStatus.AVAILABLE:
                        available_seats += 1

        blocked_seats = len(self._get_blocked_seats_for_show(show.show_id))

        return {
            "show_id": show.show_id,
            "total_seats": total_seats,
            "booked_seats": booked_seats,
            "blocked_seats": blocked_seats,
            "available_seats": available_seats,
            "occupancy_percentage": (
                (booked_seats / total_seats * 100) if total_seats > 0 else 0
            ),
            "status": show.status.value,
        }

    # Cleanup expired blocks
    def cleanup_expired_blocks(self) -> int:
        """Clean up expired seat blocks and return number of cleaned blocks."""
        cleaned_count = 0
        current_time = datetime.now()

        for show_id in list(self._blocked_seats.keys()):
            expired_seats = []

            for seat_id, block_time in self._blocked_seats[show_id].items():
                if current_time - block_time > self._block_timeout:
                    expired_seats.append(seat_id)

            for seat_id in expired_seats:
                del self._blocked_seats[show_id][seat_id]
                cleaned_count += 1

            # Remove empty show entries
            if not self._blocked_seats[show_id]:
                del self._blocked_seats[show_id]

        return cleaned_count

    # Private helper methods
    def _find_seat_in_layout(self, show: Show, seat_id: str) -> Optional[Seat]:
        """Find a seat in the show's seat layout by seat ID."""
        for row in range(show.seat_layout.num_rows):
            for col in range(show.seat_layout.seats_per_row[row]):
                seat = show.seat_layout.get_seat(row, col)
                if seat and seat.seat_id == seat_id:
                    return seat
        return None

    def _is_seat_blocked(self, show_id: str, seat_id: str) -> bool:
        """Check if a seat is currently blocked."""
        if show_id not in self._blocked_seats:
            return False

        if seat_id not in self._blocked_seats[show_id]:
            return False

        # Check if block has expired
        block_time = self._blocked_seats[show_id][seat_id]
        if datetime.now() - block_time > self._block_timeout:
            # Remove expired block
            del self._blocked_seats[show_id][seat_id]
            return False

        return True

    def _get_blocked_seats_for_show(self, show_id: str) -> List[str]:
        """Get list of blocked seats for a show (excluding expired ones)."""
        if show_id not in self._blocked_seats:
            return []

        current_time = datetime.now()
        valid_blocked_seats = []

        for seat_id, block_time in self._blocked_seats[show_id].items():
            if current_time - block_time <= self._block_timeout:
                valid_blocked_seats.append(seat_id)
            else:
                # Remove expired block
                del self._blocked_seats[show_id][seat_id]

        return valid_blocked_seats

    def _unblock_seat(self, show_id: str, seat_id: str) -> bool:
        """Unblock a seat."""
        if (show_id in self._blocked_seats and 
            seat_id in self._blocked_seats[show_id]):
            del self._blocked_seats[show_id][seat_id]

            # Remove empty show entries
            if not self._blocked_seats[show_id]:
                del self._blocked_seats[show_id]
                
            print(f"Unblocked seat {seat_id}: Success")
            return True
        print(f"Unblocked seat {seat_id}: Failed")
        return False


if __name__ == "__main__":
    # Example usage
    from Theatre import Theatre
    from Movie import Movie, MovieLanguage, MovieGenre
    from Screen import IMAXScreen
    from Show import Show
    from SeatPricingStrategy import PricingStrategyFactory
    
    # Create a theatre
    theatre = Theatre("T001", "Test Theatre", "Test City", "Test Address", "123-456-7890", "test@theatre.com")
    
    # Create a screen
    screen = IMAXScreen("S001", "IMAX Screen 1", 100, 2, [10, 10])
    theatre.add_screen(screen)
    
    # Create a movie
    movie = Movie(
        "M001", "Test Movie", 120, MovieLanguage.ENGLISH, 
        MovieGenre.ACTION, 8.5, "2024-01-01", "Test Director", 
        "Test Cast", "test-trailer.com"
    )
    
    # Create a show
    print("--------------------------------")
    print("Creating a show")
    show_time = datetime.now().replace(hour=14, minute=30, second=0, microsecond=0)
    show = Show(
        "SH001", movie, screen, show_time, 120,
        PricingStrategyFactory.create_default_strategy()
    )
    
    # Test booking manager
    print("--------------------------------")
    print("Creating a booking manager")
    booking_manager = BookingManager()
    
    # Test seat availability
    print("--------------------------------")
    print("Testing seat availability")
    available_seats = booking_manager.get_available_seats(show)
    print(f"Available seats: {len(available_seats)}")
    
    # Test seat booking
    print("--------------------------------")
    print("Testing seat booking")
    if available_seats:
        seat_id = available_seats[0]
        success = booking_manager.book_seat(show, seat_id)
        if success:
            print(f"Booking seat {seat_id}: Success")
        else:
            print(f"Failed to book seat {seat_id}")
    
    # Test show statistics
    print("--------------------------------")
    print("Testing show statistics")
    stats = booking_manager.get_show_statistics(show)
    print(f"Show statistics: {stats}")

    # Test seat cancellation
    print("--------------------------------")
    print("Testing seat cancellation")
    success = booking_manager.cancel_seat_booking(show, seat_id)
    if success:
        print(f"Cancelled seat {seat_id}: Success")
    else:
        print(f"Failed to cancel seat {seat_id}")

    # Test show statistics
    print("--------------------------------")
    print("Testing show statistics")
    stats = booking_manager.get_show_statistics(show)
    print(f"Show statistics: {stats}")

    # Test seat blocking
    print("--------------------------------")
    print("Testing seat blocking")
    success = booking_manager.block_seat(show, seat_id)

    # Test show statistics
    print("--------------------------------")
    print("Testing show statistics")
    stats = booking_manager.get_show_statistics(show)
    print(f"Show statistics: {stats}")

    # Test seat unblocking
    print("--------------------------------")
    print("Testing seat unblocking")
    success = booking_manager.unblock_seat(show, seat_id)
    

    # Test show statistics
    print("--------------------------------")
    print("Testing show statistics")
    stats = booking_manager.get_show_statistics(show)
    print(f"Show statistics: {stats}")

    # Blocking multiple seats
    print("--------------------------------")
    print("Testing blocking multiple seats")
    seat_ids = ["R0C0", "R0C1", "R0C2"]
    success = booking_manager.block_multiple_seats(show, seat_ids)

    # Test show statistics
    print("--------------------------------")
    print("Testing show statistics")
    stats = booking_manager.get_show_statistics(show)
    print(f"Show statistics: {stats}")

    # Unblocking multiple seats
    print("--------------------------------")
    print("Testing unblocking multiple seats")
    success = booking_manager.unblock_multiple_seats(show, seat_ids)

    # Test show statistics
    print("--------------------------------")
    print("Testing show statistics")
    stats = booking_manager.get_show_statistics(show)
    print(f"Show statistics: {stats}")