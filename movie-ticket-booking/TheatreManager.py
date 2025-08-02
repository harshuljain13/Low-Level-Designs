'''
This module contains the TheatreManager class, which manages theatres 
and their operations.
'''
import copy
from typing import List, Dict, Optional
from datetime import datetime
from Theatre import Theatre, TheatreStatus
from Screen import Screen, IMAXScreen, ThreeD
from Show import Show, ShowStatus
from ShowManager import ShowManager
from Movie import Movie, MovieLanguage, MovieGenre
from SeatPricingStrategy import PricingStrategyFactory


class TheatreManager:
    """
    TheatreManager class - Manages theatres, screens, and shows.

    Design Pattern: COMPOSITION + MANAGER PATTERN
    OOP Principles:
    - Single Responsibility: Manages theatre operations only
    - Encapsulation: Encapsulates theatre management logic
    - Composition: Manages theatres, screens, and shows
    """

    def __init__(self):
        self._theatres: Dict[str, Theatre] = {}
        self._show_manager = ShowManager()  # Composition: Use ShowManager for show logic

    # Core Theatre Operations
    def add_theatre(self, theatre: Theatre) -> bool:
        """Add a theatre to the system."""
        if not theatre or theatre.theatre_id in self._theatres:
            return False
        self._theatres[theatre.theatre_id] = theatre
        return True

    def get_theatre(self, theatre_id: str) -> Optional[Theatre]:
        """Get theatre by ID."""
        return self._theatres.get(theatre_id)

    def get_all_theatres(self) -> List[Theatre]:
        """Get all theatres."""
        return list(self._theatres.values())

    def get_theatres_by_location(self, location: str) -> List[Theatre]:
        """Get theatres by location."""
        return [
            t
            for t in self._theatres.values()
            if t.theatre_location.lower() == location.lower()
        ]

    def get_active_theatres(self) -> List[Theatre]:
        """Get active theatres."""
        return [
            t for t in self._theatres.values()
            if t.status == TheatreStatus.ACTIVE
        ]

    # Theatre Status Management
    def set_theatre_status(self, theatre_id: str, status: TheatreStatus) -> bool:
        """Set theatre status."""
        theatre = self.get_theatre(theatre_id)
        if not theatre:
            return False
        theatre.set_status(status)
        return True

    # Screen Management
    def add_screen(self, theatre_id: str, screen: Screen) -> bool:
        """Add a screen to a theatre."""
        theatre = self.get_theatre(theatre_id)
        if not theatre or not screen:
            return False

        if theatre.get_screen_by_id(screen.screen_id):
            return False

        theatre.add_screen(screen)
        return True

    def get_screen(self, theatre_id: str, screen_id: str) -> Optional[Screen]:
        """Get screen by ID."""
        theatre = self.get_theatre(theatre_id)
        if not theatre:
            return None

        return theatre.get_screen_by_id(screen_id)

    def remove_screen(self, theatre_id: str, screen_id: str) -> bool:
        """Remove a screen from a theatre and handle related shows."""
        theatre = self.get_theatre(theatre_id)
        if not theatre:
            return False

        screen = theatre.get_screen_by_id(screen_id)
        if not screen:
            return False

        # Get all shows that reference this screen
        related_shows = theatre.get_shows_by_screen_id(screen_id)
        
        # Check if screen has active shows
        active_shows = [
            s for s in related_shows 
            if s.status == ShowStatus.SCHEDULED
        ]
        if active_shows:
            return False  # Cannot remove screen with active shows

        # Remove all shows that reference this screen
        for show in related_shows:
            theatre.remove_show(show)

        # Remove the screen
        theatre.remove_screen(screen)
        return True

    # Show Management
    def add_show(self, theatre_id: str, show: Show) -> bool:
        """Add a show to a theatre."""
        theatre = self.get_theatre(theatre_id)
        print("Getting the Theatre with id: ", theatre_id, " : ", theatre)
        if not theatre or not show:
            return False

        # Validate show scheduling using ShowManager
        validation = self._show_manager.can_schedule_show(show, theatre)
        if not validation["can_schedule"]:
            print(f"Cannot schedule show: {validation['conflicts']}")
            return False

        # Create a deep copy of the show to prevent external modifications
        show_copy = copy.deepcopy(show)
        theatre.add_show(show_copy)
        return True

    def get_show(self, theatre_id: str, show_id: str) -> Optional[Show]:
        """Get show by ID."""
        theatre = self.get_theatre(theatre_id)
        print("Getting the Theatre with id: ", theatre_id, " : ", theatre)
        show = theatre.get_show_by_id(show_id)
        return show

    def get_shows_by_theatre(self, theatre_id: str) -> List[Show]:
        """Get all shows in a theatre."""
        theatre = self.get_theatre(theatre_id)
        print("Theatre: ", theatre.shows)
        return theatre.shows if theatre else []

    def get_available_shows(self, theatre_id: Optional[str] = None) -> List[Show]:
        """Get available shows."""
        shows = []
        theatres = (
            [self.get_theatre(theatre_id)] if theatre_id 
            else list(self._theatres.values())
        )

        for theatre in theatres:
            if not theatre:
                continue
            for show in theatre.shows:
                if show.status == ShowStatus.SCHEDULED:
                    shows.append(show)
        return shows

    # Show Status Management (delegated to ShowManager for validation)
    def start_show(self, theatre_id: str, show_id: str) -> bool:
        """Start a show."""
        show = self.get_show(theatre_id, show_id)
        if not show:
            return False
        
        # Use ShowManager for validation and status change
        if self._show_manager.start_show(show):
            # Show status is updated in ShowManager, no storage update needed
            return True
        return False

    def cancel_show(self, theatre_id: str, show_id: str) -> bool:
        """Cancel a show."""
        show = self.get_show(theatre_id, show_id)
        if not show:
            return False
        
        # Use ShowManager for validation and status change
        if self._show_manager.cancel_show(show):
            # Show status is updated in ShowManager, no storage update needed
            return True
        return False

    def complete_show(self, theatre_id: str, show_id: str) -> bool:
        """Mark a show as completed."""
        show = self.get_show(theatre_id, show_id)
        if not show:
            return False
        
        # Use ShowManager for validation and status change
        if self._show_manager.complete_show(show):
            # Show status is updated in ShowManager, no storage update needed
            return True
        return False

    def remove_show(self, theatre_id: str, show_id: str) -> bool:
        """Remove a show from theatre storage."""
        theatre = self.get_theatre(theatre_id)
        if not theatre:
            return False
        
        show = theatre.get_show_by_id(show_id)
        if not show:
            return False
        
        # Check if show can be removed (not running or completed)
        if show.status in [ShowStatus.RUNNING, ShowStatus.COMPLETED]:
            return False
        
        theatre.remove_show(show)
        return True

    def cancel_and_remove_show(self, theatre_id: str, show_id: str) -> bool:
        """Cancel a show and optionally remove it from storage."""
        show = self.get_show(theatre_id, show_id)
        print("Getting the show with id: ", show_id, " : ", show)
        if not show:
            return False
        
        # Use ShowManager for validation and status change
        if self._show_manager.cancel_show(show):
            # Show is cancelled, now remove from storage
            return self.remove_show(theatre_id, show_id)
        return False


if __name__ == "__main__":
    theatre_manager = TheatreManager()
    print("--------------------------------")
    print("Theatre manager: ", theatre_manager)

    # Create theatres
    print("--------------------------------")
    print("Creating and adding theatre 1: ")
    theatre1 = Theatre(
        "1", "Theatre 1", "Location 1", "Address 1", "Contact 1", "Email 1"
    )
    theatre_manager.add_theatre(theatre1)

    print("Creating and adding theatre 2: ")
    theatre2 = Theatre(
        "2", "Theatre 2", "Location 2", "Address 2", "Contact 2", "Email 2"
    )
    theatre_manager.add_theatre(theatre2)

    # Fetch theatres
    print("--------------------------------")
    print("Fetching theatre 1: ", theatre_manager.get_theatre("1"))
    print("Fetching theatre 2: ", theatre_manager.get_theatre("2"))
    print("Fetching all theatres: ", theatre_manager.get_all_theatres())
    print(
        "Fetching theatres by location: ",
        theatre_manager.get_theatres_by_location("Location 1"),
    )
    print("Fetching active theatres: ", theatre_manager.get_active_theatres())

    # Create screens
    print("--------------------------------")
    screen1 = IMAXScreen("1", "Screen 1", 100, 2, [10, 10])
    print("Created screen 1: ", screen1)
    screen2 = ThreeD("2", "Screen 2", 100, 2, [10, 10])
    print("Created screen 2: ", screen2)

    # Add screens to theatres
    print("--------------------------------")
    print("Adding screen 1 & 2 to theatre 1: ", screen1, screen2)
    theatre_manager.add_screen("1", screen1)
    theatre_manager.add_screen("1", screen2)
    print("Adding screen 1 & 2 to theatre 2: ", screen1, screen2)
    theatre_manager.add_screen("2", screen1)
    theatre_manager.add_screen("2", screen2)

    # Fetch screens
    print("--------------------------------")
    print("Fetching screen 1 from theatre 1: ", theatre_manager.get_screen("1", "1"))
    print("Fetching screen 2 from theatre 1: ", theatre_manager.get_screen("1", "2"))
    print("Fetching screen 1 from theatre 2: ", theatre_manager.get_screen("2", "1"))
    print("Fetching screen 2 from theatre 2: ", theatre_manager.get_screen("2", "2"))

    # Create movies
    print("--------------------------------")
    movie1 = Movie(
        "1",
        "Movie 1",
        120,
        MovieLanguage.ENGLISH,
        MovieGenre.ACTION,
        9.0,
        "2021-01-01",
        "Director 1",
        "Cast 1",
        "Trailer 1",
    )
    movie2 = Movie(
        "2",
        "Movie 2",
        120,
        MovieLanguage.ENGLISH,
        MovieGenre.ACTION,
        9.0,
        "2021-01-01",
        "Director 2",
        "Cast 2",
        "Trailer 2",
    )
    print("Fetching movie 1: ", movie1)
    print("Fetching movie 2: ", movie2)

    # Create shows
    print("--------------------------------")
    show_time_1 = datetime.now().replace(hour=14, minute=30, second=0, microsecond=0)
    show_date_1 = datetime.now().date()
    print("Creating show 1 at: ", show_time_1)
    show1 = Show(
        show_id="SH001",
        movie=movie1,
        screen=screen1,
        show_time=show_time_1,
        show_duration=152,
        pricing_strategy=PricingStrategyFactory.create_holiday_strategy(
            holiday_surcharge=0.2
        ),
    )
    print("Created show 1: ", show1)
    show_time_2 = datetime.now().replace(hour=14, minute=30, second=0, microsecond=0)
    show_date_2 = datetime.now().date()
    print("Creating show 2: ", show_time_2)
    show2 = Show(
        show_id="SH002",
        movie=movie2,
        screen=screen2,
        show_time=show_time_2,
        show_duration=152,
        pricing_strategy=PricingStrategyFactory.create_student_discount_strategy(
            discount_rate=0.2
        ),
    )
    print("Created show 2: ", show2)

    # Add shows to theatres
    print("--------------------------------")
    print("Adding show 1 & 2: ", show1, " to theatre 1")
    theatre_manager.add_show("1", show1)
    theatre_manager.add_show("1", show2)
    print("Adding show 1 & 2: ", show2, " to theatre 2")
    theatre_manager.add_show("2", show1)
    theatre_manager.add_show("2", show2)

    # Theatre shows
    print("--------------------------------")
    print("Theatre 1shows: ", theatre_manager.get_shows_by_theatre("1"))
    print("Theatre 2 shows: ", theatre_manager.get_shows_by_theatre("2"))

    # Get show
    print("--------------------------------")
    show1 = theatre_manager.get_show("1", "SH001")
    print("Show 1: ", show1, " with price: ", show1.calculate_seat_price(1, 5))
    show2 = theatre_manager.get_show("2", "SH002")
    print("Show 2: ", show2, " with price: ", show2.calculate_seat_price(1, 5))

    # Start show
    print("--------------------------------")
    print("Starting show 1 from theatre 1: ", theatre_manager.start_show("1", "SH001"))
    print("Starting show 2 from theatre 2: ", theatre_manager.start_show("2", "SH002"))

    # Cancel show
    print("--------------------------------")
    print("Cancelling show 1 from theatre 1: ", theatre_manager.cancel_show("1", "SH001"))
    print("Cancelling show 2 from theatre 2: ", theatre_manager.cancel_show("2", "SH002"))

    # Complete show
    print("--------------------------------")
    print("Completing show 1 from theatre 1: ", theatre_manager.complete_show("1", "SH001"))
    print("Completing show 2 from theatre 2: ", theatre_manager.complete_show("2", "SH002"))

    # Remove show
    print("--------------------------------")
    print("Removing show 1 from theatre 1: ", theatre_manager.remove_show("1", "SH001"))
    print("Removing show 1 from theatre 2: ", theatre_manager.remove_show("2", "SH001"))

    # Cancel and remove show
    print("--------------------------------")
    print("Cancelling and removing show 2 from theatre 1: ",
          theatre_manager.cancel_and_remove_show("1", "SH002"))
