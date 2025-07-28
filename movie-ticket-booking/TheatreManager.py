from typing import List, Dict, Optional
from datetime import datetime, timedelta
from Theatre import Theatre, TheatreStatus
from Screen import Screen,IMAXScreen, ThreeD
from Show import Show, ShowStatus
from ShowManager import ShowManager
from Movie import Movie, MovieLanguage, MovieGenre
from SeatPricingStrategy import PricingStrategy, PricingStrategyFactory


class TheatreManager:
    '''
    TheatreManager class - Minimalistic theatre management with composition.
    
    Design Pattern: COMPOSITION + MANAGER PATTERN
    OOP Principles:
    - Single Responsibility: Manages theatre operations only
    - Encapsulation: Encapsulates theatre management logic
    - Composition: Contains ShowManager for show operations (demonstrates composition)
    - Abstraction: Delegates show-specific logic to ShowManager (demonstrates abstraction)
    '''
    
    def __init__(self):
        self._theatres: Dict[str, Theatre] = {}
        self._show_manager = ShowManager()  # Composition: TheatreManager uses ShowManager
    
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
        return [t for t in self._theatres.values() 
                if t.theatre_location.lower() == location.lower()]
    
    def get_active_theatres(self) -> List[Theatre]:
        """Get active theatres."""
        return [t for t in self._theatres.values() 
                if t.status == TheatreStatus.ACTIVE]
    
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
    
    def remove_screen(self, theatre_id: str, screen_id: str) -> bool:
        """Remove a screen from a theatre."""
        theatre = self.get_theatre(theatre_id)
        if not theatre:
            return False
        
        screen = theatre.get_screen_by_id(screen_id)
        if not screen:
            return False
        
        # Check if screen has active shows
        active_shows = [s for s in theatre.shows if s.screen.screen_id == screen_id and 
                        s.status == ShowStatus.SCHEDULED]
        if active_shows:
            return False  # Cannot remove screen with active shows
        
        theatre.remove_screen(screen)
        return True
    
    # Show Management
    def add_show(self, theatre_id: str, show: Show) -> bool:
        """Add a show to a theatre."""
        theatre = self.get_theatre(theatre_id)
        if not theatre or not show:
            return False
        
        if self._show_exists(show.show_id):
            return False
        
        if show.screen not in theatre.screens:
            return False
        
        # Delegate time conflict checking to ShowManager
        if self._show_manager.has_time_conflict(show, theatre.shows):
            return False
        
        theatre._add_show(show)
        return True
    
    def get_show(self, show_id: str) -> Optional[Show]:
        """Get show by ID."""
        for theatre in self._theatres.values():
            show = theatre.get_show_by_id(show_id)
            if show:
                return show
        return None
    
    def get_shows_by_theatre(self, theatre_id: str) -> List[Show]:
        """Get all shows in a theatre."""
        theatre = self.get_theatre(theatre_id)
        return theatre.shows if theatre else []
    
    def get_available_shows(self, theatre_id: Optional[str] = None) -> List[Show]:
        """Get available shows."""
        shows = []
        theatres = [self.get_theatre(theatre_id)] if theatre_id else self._theatres.values()
        
        for theatre in theatres:
            if not theatre:
                continue
            for show in theatre.shows:
                if show.status == ShowStatus.SCHEDULED:
                    shows.append(show)
        return shows
    
    # Show Status Management (delegated to ShowManager - demonstrates abstraction)
    def start_show(self, show_id: str) -> bool:
        """Start a show."""
        show = self.get_show(show_id)
        if not show or not self._show_manager.can_start_show(show):
            return False
        show.set_status(ShowStatus.RUNNING)
        return True
    
    def cancel_show(self, show_id: str) -> bool:
        """Cancel a show."""
        show = self.get_show(show_id)
        if not show or not self._show_manager.can_cancel_show(show):
            return False
        show.set_status(ShowStatus.CANCELLED)
        return True
    
    # Seat Management (delegated to ShowManager - demonstrates abstraction)
    def book_seat(self, show_id: str, seat_id: str) -> bool:
        """Book a seat for a show."""
        show = self.get_show(show_id)
        return self._show_manager.book_seat(show, seat_id) if show else False
    
    def get_available_seats(self, show_id: str) -> List[str]:
        """Get available seats for a show."""
        show = self.get_show(show_id)
        return self._show_manager.get_available_seats(show) if show else []
    
    def block_seat(self, show_id: str, seat_id: str) -> bool:
        """Block a seat temporarily."""
        show = self.get_show(show_id)
        return self._show_manager.block_seat(show, seat_id) if show else False
    
    # Statistics
    def get_theatre_stats(self, theatre_id: str) -> Dict[str, any]:
        """Get basic theatre statistics."""
        theatre = self.get_theatre(theatre_id)
        if not theatre:
            return {}
        
        return {
            "theatre_id": theatre_id,
            "total_screens": theatre.total_screens,
            "total_shows": theatre.total_shows,
            "active_shows": len([s for s in theatre.shows if s.status == ShowStatus.SCHEDULED])
        }
    
    def get_show_stats(self, show_id: str) -> Dict[str, any]:
        """Get statistics for a specific show (delegated to ShowManager)."""
        show = self.get_show(show_id)
        return self._show_manager.get_show_statistics(show) if show else {}
    
    def set_show_pricing_strategy(self, show_id: str, pricing_strategy: PricingStrategy) -> bool:
        """Set pricing strategy for a show."""
        show = self.get_show(show_id)
        if not show:
            return False
        show.set_pricing_strategy(pricing_strategy)
        return True
    
    # Private helper methods
    def _show_exists(self, show_id: str) -> bool:
        """Check if a show exists."""
        return self.get_show(show_id) is not None
    

if __name__ == "__main__":
    theatre_manager = TheatreManager()
    theatre1 = Theatre("1", "Theatre 1", "Location 1", "Address 1", "Contact 1", "Email 1")
    theatre2 = Theatre("2", "Theatre 2", "Location 2", "Address 2", "Contact 2", "Email 2")
    theatre_manager.add_theatre(theatre1)
    theatre_manager.add_theatre(theatre2)

    print("--------------------------------")
    print("Fetching theatre 1: ", theatre_manager.get_theatre("1"))
    print("--------------------------------")
    print("Fetching all theatres: ", theatre_manager.get_all_theatres())
    print("--------------------------------")
    print("Fetching theatres by location: ", theatre_manager.get_theatres_by_location(
        "Location 1"))
    print("--------------------------------")
    print("Fetching active theatres: ", theatre_manager.get_active_theatres())
    print("--------------------------------")

    screen1 = IMAXScreen("1", "Screen 1", 100, 2, [10, 10])
    screen2 = ThreeD("2", "Screen 2", 100, 2, [10, 10])

    theatre_manager.add_screen("1", screen1)
    theatre_manager.add_screen("1", screen2)

    print("--------------------------------")
    print("Fetching screen 1: ", theatre_manager.get_screen("1"))
    print("--------------------------------")
    print("Fetching screen 2: ", theatre_manager.get_screen("2"))
    print("--------------------------------")

    movie1 = Movie("1", "Movie 1", 120, MovieLanguage.ENGLISH, 
                MovieGenre.ACTION, 9.0, "2021-01-01", "Director 1", 
                    "Cast 1", "Trailer 1")
    movie2 = Movie("2", "Movie 2", 120, MovieLanguage.ENGLISH, 
                MovieGenre.ACTION, 9.0, "2021-01-01", "Director 2", 
                "Cast 2", "Trailer 2")

    print("--------------------------------")
    print("Fetching movie 1: ", movie1)
    print("--------------------------------")
    print("Fetching movie 2: ", movie2)
    print("--------------------------------")

    show_time_1 = datetime.now().replace(hour=14, minute=30, second=0, microsecond=0)
    show_date_1 = datetime.now().date()
    show1 = Show(
        show_id="SH001",
        movie=movie1,
        screen=screen1,
        show_time=show_time_1,
        show_duration=152,
        price_multiplier=1.2
    )

    show_time_2 = datetime.now().replace(hour=14, minute=30, second=0, microsecond=0)
    show_date_2 = datetime.now().date()
    show2 = Show("2", "Show 2", screen2, movie2, "10:00", "12:00", "100", "10")


