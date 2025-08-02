from typing import List
from enum import Enum
from Screen import Screen
from Show import Show


class TheatreStatus(Enum):
    """Enum for theatre status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    CLOSED = "closed"


class Theatre:
    """
    Theatre class - Pure data model for a movie theatre.

    OOP Principles:
    - Encapsulation: Encapsulates theatre data
    - Single Responsibility: Only holds theatre data, no business logic
    - Composition: Contains screens and shows as data
    """

    def __init__(
        self,
        theatre_id: str,
        theatre_name: str,
        theatre_location: str,
        theatre_address: str,
        theatre_contact: str,
        theatre_email: str,
    ):
        """
        Initialize a theatre with basic information.

        Args:
            theatre_id: Unique identifier for the theatre
            theatre_name: Name of the theatre
            theatre_location: Location/city of the theatre
            theatre_address: Full address of the theatre
            theatre_contact: Contact phone number
            theatre_email: Contact email address
        """
        self._theatre_id = theatre_id
        self._theatre_name = theatre_name
        self._theatre_location = theatre_location
        self._theatre_address = theatre_address
        self._theatre_contact = theatre_contact
        self._theatre_email = theatre_email
        self._status = TheatreStatus.ACTIVE
        self._screens: List[Screen] = []
        self._shows: List[Show] = []

    # Properties for data access (read-only)
    @property
    def theatre_id(self) -> str:
        return self._theatre_id

    @property
    def theatre_name(self) -> str:
        return self._theatre_name

    @property
    def theatre_location(self) -> str:
        return self._theatre_location

    @property
    def theatre_address(self) -> str:
        return self._theatre_address

    @property
    def theatre_contact(self) -> str:
        return self._theatre_contact

    @property
    def theatre_email(self) -> str:
        return self._theatre_email

    @property
    def status(self) -> TheatreStatus:
        return self._status

    @property
    def screens(self) -> List[Screen]:
        return self._screens.copy()

    @property
    def shows(self) -> List[Show]:
        return self._shows.copy()

    @property
    def total_screens(self) -> int:
        return len(self._screens)

    @property
    def total_shows(self) -> int:
        return len(self._shows)

    # Simple data setters (no business logic)
    def set_status(self, status: TheatreStatus) -> None:
        """Set theatre status."""
        self._status = status

    def add_screen(self, screen: Screen) -> None:
        """Add a screen to the theatre."""
        if screen not in self._screens:
            self._screens.append(screen)

    def remove_screen(self, screen: Screen) -> None:
        """Remove a screen from the theatre."""
        if screen in self._screens:
            self._screens.remove(screen)

    # Data access methods (read-only)
    def get_screen_by_id(self, screen_id: str) -> Screen:
        """Get a screen by ID."""
        for screen in self._screens:
            if screen.screen_id == screen_id:
                return screen
        return None

    def get_shows_by_screen_id(self, screen_id: str) -> List[Show]:
        """Get all shows that reference a specific screen ID."""
        return [
            show for show in self._shows 
            if show.screen.screen_id == screen_id
        ]

    def get_show_by_id(self, show_id: str) -> Show:
        """Get a show by ID."""
        for show in self._shows:
            if show.show_id == show_id:
                return show
        return None

    # Internal methods for TheatreManager use only
    def add_show(self, show: Show) -> None:
        """Internal method to add a show (used by TheatreManager)."""
        if show not in self._shows:
            self._shows.append(show)

    def remove_show(self, show: Show) -> None:
        """Internal method to remove a show (used by TheatreManager)."""
        if show in self._shows:
            self._shows.remove(show)

    def __str__(self) -> str:
        return f"Theatre({self._theatre_id}, {self._theatre_name}, {self._theatre_location}, {self._status})"

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == "__main__":
    theatre = Theatre(
        "1", "Theatre 1", "Location 1", "Address 1", "Contact 1", "Email 1"
    )
    print("theatre: ", theatre)
    print("theatre_id: ", theatre.theatre_id)
    print("theatre_name: ", theatre.theatre_name)
    print("theatre_location: ", theatre.theatre_location)
    print("theatre_address: ", theatre.theatre_address)
    print("theatre_contact: ", theatre.theatre_contact)
    print("theatre_email: ", theatre.theatre_email)
