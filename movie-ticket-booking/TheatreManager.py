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
    
    def get_screen(self, theatre_id: str, screen_id: str) -> Optional[Screen]:
        """Get screen by ID."""
        theatre = self.get_theatre(theatre_id)
        if not theatre:
            return None
        
        return theatre.get_screen_by_id(screen_id)
    
    def remove_screen(self, theatre_id: str, screen_id: str) -> bool:
        """Remove a screen from a theatre."""
        theatre = self.get_theatre(theatre_id)
        if not theatre:
            return False
        
        screen = theatre.get_screen_by_id(screen_id)
        if not screen:
            return False
        
        # Check if screen has active shows
        active_shows = [s for s in theatre.shows if 
            s.screen.screen_id == screen_id and 
                        s.status == ShowStatus.SCHEDULED]
        if active_shows:
            return False  # Cannot remove screen with active shows
        
        theatre.remove_screen(screen)
        return True
    
    # Show Management
    def add_show(self, theatre_id: str, show: Show) -> bool:
        """Add a show to a theatre."""
        theatre = self.get_theatre(theatre_id)
        print("Getting the Theatre with id: ", theatre_id, " : ", theatre)
        if not theatre or not show:
            return False
        
        theatre.add_show(show)
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
        theatres = [self.get_theatre(theatre_id)] if theatre_id else
                    self._theatres.values()
        
        for theatre in theatres:
            if not theatre:
                continue
            for show in theatre.shows:
                if show.status == ShowStatus.SCHEDULED:
                    shows.append(show)
        return shows
    
    # Show Status Management (delegated to ShowManager - demonstrates abstraction)
    def start_show(self, theatre_id: str, show_id: str) -> bool:
        """Start a show."""
        show = self.get_show(theatre_id, show_id)
        if not show or not self._show_manager.can_start_show(show):
            return False
        show.set_status(ShowStatus.RUNNING)
        return True
    
    def cancel_show(self, theatre_id: str, show_id: str) -> bool:
        """Cancel a show."""
        show = self.get_show(theatre_id, show_id)
        if not show or not self._show_manager.can_cancel_show(show):
            return False
        show.set_status(ShowStatus.CANCELLED)
        return True


if __name__ == "__main__":
    theatre_manager = TheatreManager()
    print("--------------------------------")
    print("Theatre manager: ", theatre_manager)
    print("--------------------------------")
    # Create theatres
    print("--------------------------------")
    print("Creating theatre 1: ")
    theatre1 = Theatre("1", "Theatre 1", "Location 1", "Address 1", "Contact 1", "Email 1")
    print("--------------------------------")
    print("Adding theatre 1: ", theatre1)
    theatre_manager.add_theatre(theatre1)
    print("--------------------------------")
    print("Creating theatre 2: ")
    theatre2 = Theatre("2", "Theatre 2", "Location 2", "Address 2", "Contact 2", "Email 2")
    print("--------------------------------")
    print("Adding theatre 2: ", theatre2)
    theatre_manager.add_theatre(theatre2)
    print("--------------------------------")

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

    # Create screens
    print("--------------------------------")
    screen1 = IMAXScreen("1", "Screen 1", 100, 2, [10, 10])
    print("Created screen 1: ", screen1)
    
    print("--------------------------------")
    screen2 = ThreeD("2", "Screen 2", 100, 2, [10, 10])
    print("Created screen 2: ", screen2)
    print("--------------------------------")

    # Add screens to theatres
    print("--------------------------------")
    print("Adding screen 1: ", screen1)
    theatre_manager.add_screen("1", screen1)
    print("--------------------------------")
    print("Adding screen 2: ", screen2)
    theatre_manager.add_screen("1", screen2)
    print("--------------------------------")
    print("Fetching screen 1: ", theatre_manager.get_screen("1", "1"))
    print("--------------------------------")
    print("Fetching screen 2: ", theatre_manager.get_screen("1", "2"))
    print("--------------------------------")

    # Create movies
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

    # Create shows
    show_time_1 = datetime.now().replace(hour=14, minute=30, second=0, microsecond=0)
    show_date_1 = datetime.now().date()
    print("--------------------------------")
    print("Creating show 1: ", show_time_1)
    print("--------------------------------")
    show1 = Show(
        show_id="SH001",
        movie=movie1,
        screen=screen1,
        show_time=show_time_1,
        show_duration=152,
        pricing_strategy=PricingStrategyFactory.create_holiday_strategy(
            holiday_surcharge=0.2)
    )
    print("Created show 1: ", show1)
    print("--------------------------------")
    show_time_2 = datetime.now().replace(hour=14, minute=30, second=0, microsecond=0)
    show_date_2 = datetime.now().date()
    print("--------------------------------")
    print("Creating show 2: ", show_time_2)
    print("--------------------------------")
    show2 = Show(
        show_id="SH002",
        movie=movie2,
        screen=screen2,
        show_time=show_time_2,
        show_duration=152,
        pricing_strategy=PricingStrategyFactory.create_student_discount_strategy(
            discount_rate=0.2)
    )
    print("Created show 2: ", show2)
    print("--------------------------------")

    # Add shows to theatres
    print("--------------------------------")
    print("Adding show 1: ", show1)
    theatre_manager.add_show("1", show1)
    print("--------------------------------")
    print("Adding show 2: ", show2)
    theatre_manager.add_show("2", show2)
    print("--------------------------------")

    print("--------------------------------")
    print("Theatre 1shows: ", theatre_manager.get_shows_by_theatre("1"))
    print("--------------------------------")
    print("Theatre 2 shows: ", theatre_manager.get_shows_by_theatre("2"))
    print("--------------------------------")

    print("--------------------------------")
    show1 = theatre_manager.get_show("1", "SH001")
    print("Show 1: ", show1)
    print("--------------------------------")
    print("Show 1 price for seat : ", show1.calculate_seat_price(1, 5))
    print("--------------------------------")
    show2 = theatre_manager.get_show("2", "SH002")
    print("Show 2: ", show2)
    print("--------------------------------")
    print("Show 2 price for seat : ", show2.calculate_seat_price(1, 5))
    print("--------------------------------")