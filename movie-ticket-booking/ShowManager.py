from typing import List, Dict, Optional
from datetime import datetime, timedelta
from Show import Show, ShowStatus
from Seat import Seat, SeatStatus


class ShowManager:
    '''
    ShowManager class - Handles show-specific business logic.
    
    Design Pattern: MANAGER PATTERN (Service Layer)
    OOP Principles:
    - Single Responsibility: Manages show operations only
    - Encapsulation: Encapsulates show management logic
    - Composition: Works with Show's seat layout
    '''
    
    def __init__(self):
        self._blocked_seats: Dict[str, Dict[str, datetime]] = {}  # show_id -> {seat_id: block_time}
        self._block_timeout = timedelta(minutes=15)  # 15 minutes timeout for blocked seats
    
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
            return False
        
        if show.show_id not in self._blocked_seats:
            self._blocked_seats[show.show_id] = {}
        
        self._blocked_seats[show.show_id][seat_id] = datetime.now()
        return True
    
    def unblock_seat(self, show: Show, seat_id: str) -> bool:
        """Unblock a seat."""
        return self._unblock_seat(show.show_id, seat_id)
    
    def block_multiple_seats(self, show: Show, seat_ids: List[str]) -> Dict[str, bool]:
        """Block multiple seats and return results for each seat."""
        results = {}
        
        for seat_id in seat_ids:
            results[seat_id] = self.block_seat(show, seat_id)
        
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
            "occupancy_percentage": (booked_seats / total_seats * 100) if total_seats > 0 else 0,
            "status": show.status.value
        }
    
    def get_show_revenue(self, show: Show) -> float:
        """Calculate total revenue for a show using pricing strategy."""
        total_revenue = 0.0
        
        for row in range(show.seat_layout.num_rows):
            for col in range(show.seat_layout.seats_per_row[row]):
                seat = show.seat_layout.get_seat(row, col)
                if seat and seat.status == SeatStatus.BOOKED:
                    total_revenue += show.calculate_seat_price(seat.seat_id)
        
        return total_revenue
    
    # Show Status Management
    def can_start_show(self, show: Show) -> bool:
        """Check if a show can be started."""
        if show.status != ShowStatus.SCHEDULED:
            return False
        
        current_time = datetime.now()
        return current_time >= show.show_time
    
    def can_cancel_show(self, show: Show) -> bool:
        """Check if a show can be cancelled."""
        return show.status not in [ShowStatus.COMPLETED, ShowStatus.CANCELLED]
    
    def has_time_conflict(self, new_show: Show, existing_shows: List[Show]) -> bool:
        """Check if a new show has time conflicts with existing shows on the same screen."""
        new_start = new_show.show_time
        new_end = new_show.get_show_end_time()
        
        for existing_show in existing_shows:
            if existing_show.screen.screen_id == new_show.screen.screen_id:
                existing_start = existing_show.show_time
                existing_end = existing_show.get_show_end_time()
                
                # 30 minutes buffer between shows
                buffer = timedelta(minutes=30)
                if (new_start < existing_end + buffer and 
                    new_end > existing_start - buffer):
                    return True
        
        return False
    
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
        if show_id in self._blocked_seats and seat_id in self._blocked_seats[show_id]:
            del self._blocked_seats[show_id][seat_id]
            
            # Remove empty show entries
            if not self._blocked_seats[show_id]:
                del self._blocked_seats[show_id]
            
            return True
        return False 