"""
This module contains the ShowManager class, which handles show scheduling
and validation logic.

Design Pattern: MANAGER PATTERN (Service Layer)
OOP Principles:
- Single Responsibility: Manages show scheduling and validation only
- Encapsulation: Encapsulates show scheduling logic
- Composition: Works with Show objects
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from Show import Show, ShowStatus
from Theatre import Theatre


class ShowManager:
    """
    ShowManager class - Handles show scheduling and validation logic.

    Design Pattern: MANAGER PATTERN (Service Layer)
    OOP Principles:
    - Single Responsibility: Manages show scheduling and validation only
    - Encapsulation: Encapsulates show scheduling logic
    - Composition: Works with Show objects
    """

    def __init__(self):
        self._buffer_time = timedelta(minutes=30)  # Buffer between shows
    
    # Show Scheduling and Validation
    def can_schedule_show(self, new_show: Show, theatre: Theatre) -> Dict[str, any]:
        """
        Check if a show can be scheduled in a theatre.
        
        Returns:
            Dict with 'can_schedule' (bool) and 'conflicts' (list of conflict details)
        """
        conflicts = []
        
        # Check if screen exists in theatre
        if not theatre.get_screen_by_id(new_show.screen.screen_id):
            conflicts.append(f"Screen {new_show.screen.screen_id} not found in theatre")
        
        # Check for time conflicts with existing shows
        time_conflicts = self._check_time_conflicts(new_show, theatre.shows)
        conflicts.extend(time_conflicts)
        
        # Check if show time is in the future
        if new_show.show_time <= datetime.now():
            conflicts.append("Show time must be in the future")
        
        # Check if show duration is reasonable
        if new_show.show_duration <= 0 or new_show.show_duration > 300:  # 5 hours max
            conflicts.append("Show duration must be between 1 and 300 minutes")
        
        return {
            "can_schedule": len(conflicts) == 0,
            "conflicts": conflicts
        }

    def find_available_slots(self, theatre: Theatre, screen_id: str, 
                           date: datetime, duration: int) -> List[Dict[str, datetime]]:
        """
        Find available time slots for a show on a specific screen and date.
        
        Returns:
            List of available slots with start and end times
        """
        available_slots = []
        
        # Get all shows for the screen on the given date
        screen_shows = [
            show for show in theatre.shows 
            if show.screen.screen_id == screen_id and 
            show.show_time.date() == date.date()
        ]
        
        # Sort shows by start time
        screen_shows.sort(key=lambda x: x.show_time)
        
        # Define business hours (e.g., 9 AM to 11 PM)
        business_start = date.replace(hour=9, minute=0, second=0, microsecond=0)
        business_end = date.replace(hour=23, minute=0, second=0, microsecond=0)
        
        current_time = business_start
        
        for show in screen_shows:
            # Check if there's enough time before this show
            if current_time + timedelta(minutes=duration) + self._buffer_time <= show.show_time:
                available_slots.append({
                    "start_time": current_time,
                    "end_time": current_time + timedelta(minutes=duration)
                })
            
            # Move current time to after this show ends
            current_time = show.get_show_end_time() + self._buffer_time
        
        # Check if there's time after the last show
        if current_time + timedelta(minutes=duration) <= business_end:
            available_slots.append({
                "start_time": current_time,
                "end_time": current_time + timedelta(minutes=duration)
            })
        
        return available_slots

    def get_show_schedule(self, theatre: Theatre, screen_id: Optional[str] = None, 
                         date: Optional[datetime] = None) -> List[Show]:
        """
        Get show schedule for a theatre, optionally filtered by screen and date.
        
        Returns:
            List of shows sorted by start time
        """
        shows = theatre.shows
        
        # Filter by screen if specified
        if screen_id:
            shows = [show for show in shows if show.screen.screen_id == screen_id]
        
        # Filter by date if specified
        if date:
            shows = [
                show for show in shows 
                if show.show_time.date() == date.date()
            ]
        
        # Sort by start time
        shows.sort(key=lambda x: x.show_time)
        return shows

    def validate_show_transition(self, show: Show, new_status: ShowStatus) -> bool:
        """
        Validate if a show can transition to a new status.
        
        Returns:
            True if transition is valid, False otherwise
        """
        valid_transitions = {
            ShowStatus.SCHEDULED: [ShowStatus.RUNNING, ShowStatus.CANCELLED],
            ShowStatus.RUNNING: [ShowStatus.COMPLETED, ShowStatus.CANCELLED],
            ShowStatus.COMPLETED: [],  # Terminal state
            ShowStatus.CANCELLED: []   # Terminal state
        }
        
        current_status = show.status
        return new_status in valid_transitions.get(current_status, [])

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

    def can_complete_show(self, show: Show) -> bool:
        """Check if a show can be completed."""
        return show.status == ShowStatus.RUNNING

    def start_show(self, show: Show) -> bool:
        """Start a show if conditions are met."""
        if not self.can_start_show(show):
            return False
        show.status = ShowStatus.RUNNING
        return True

    def cancel_show(self, show: Show) -> bool:
        """Cancel a show if conditions are met."""
        if not self.can_cancel_show(show):
            print(f"Cannot cancel show {show.show_id} because it is not in the scheduled state")
            return False
        print(f"Cancelling show {show.show_id}")
        show.status = ShowStatus.CANCELLED
        return True

    def complete_show(self, show: Show) -> bool:
        """Complete a show if conditions are met."""
        if not self.can_complete_show(show):
            return False
        show.status = ShowStatus.COMPLETED
        return True

    # Private helper methods
    def _check_time_conflicts(self, new_show: Show, existing_shows: List[Show]) -> List[str]:
        """Check for time conflicts with existing shows on the same screen."""
        conflicts = []
        new_start = new_show.show_time
        new_end = new_show.get_show_end_time()

        for existing_show in existing_shows:
            if existing_show.screen.screen_id == new_show.screen.screen_id:
                existing_start = existing_show.show_time
                existing_end = existing_show.get_show_end_time()

                # Check for overlap with buffer time
                if (
                    new_start < existing_end + self._buffer_time
                    and new_end > existing_start - self._buffer_time
                ):
                    conflicts.append(
                        f"Time conflict with show {existing_show.show_id} "
                        f"({existing_start} - {existing_end})"
                    )

        return conflicts


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
    show_time = datetime.now().replace(hour=14, minute=30, second=0, microsecond=0)
    test_show = Show(
        "SH001", movie, screen, show_time, 120,
        PricingStrategyFactory.create_default_strategy()
    )
    
    # Test show manager
    show_manager = ShowManager()
    
    # Test scheduling validation
    result = show_manager.can_schedule_show(test_show, theatre)
    print(f"Can schedule show: {result['can_schedule']}")
    if result['conflicts']:
        print(f"Conflicts: {result['conflicts']}")
    
    # Test available slots
    date = datetime.now().date()
    slots = show_manager.find_available_slots(theatre, "S001", datetime.now(), 120)
    print(f"Available slots: {len(slots)}")
    
    # Test show schedule
    schedule = show_manager.get_show_schedule(theatre)
    print(f"Show schedule: {len(schedule)} shows")
