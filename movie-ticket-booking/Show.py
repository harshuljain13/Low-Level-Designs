from datetime import datetime, timedelta
from enum import Enum
import copy
from Movie import Movie
from Screen import Screen
from SeatLayout import SeatLayout
from SeatPricingStrategy import PricingStrategy, DefaultPricingStrategy


class ShowStatus(Enum):
    """Enum for show status."""

    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Show:
    """
    Show class - Represents a movie screening with its own screen copy.

    OOP Principles:
    - Encapsulation: Encapsulates show data and its own screen copy
    - Single Responsibility: Only manages show data and its screen
    - Composition: Contains its own Screen instance
    - Strategy Pattern: Uses pricing strategy for seat pricing

    Why own screen copy?
    - Multiple shows can use the same screen template
    - Each show needs independent screen state (including seat layout)
    - Booking in one show shouldn't affect other shows
    - Complete independence from original screen
    """

    def __init__(
        self,
        show_id: str,
        movie: Movie,
        screen: Screen,
        show_time: datetime,
        show_duration: int,
        pricing_strategy: PricingStrategy = None,
    ):
        """
        Initialize a show with basic information and its own screen copy.

        Args:
            show_id: Unique identifier for the show
            movie: Movie object to be screened
            screen: Screen object where movie will be shown (template)
            show_time: Time when show starts
            show_duration: Duration of the show in minutes
            pricing_strategy: Strategy for calculating seat prices
                             (defaults to DefaultPricingStrategy)
        """
        self._show_id = show_id
        self._movie = movie
        self._show_time = show_time
        self._show_duration = show_duration
        self._pricing_strategy = pricing_strategy or DefaultPricingStrategy()
        self._status = ShowStatus.SCHEDULED

        # Create a deep copy of the entire screen for this show
        # This ensures each show has its own independent screen state
        self._screen = copy.deepcopy(screen)
        self._screen.prepare_seat_layout()

    # Simple properties
    @property
    def show_id(self) -> str:
        return self._show_id

    @property
    def movie(self) -> Movie:
        return self._movie

    @property
    def screen(self) -> Screen:
        return self._screen

    @property
    def show_time(self) -> datetime:
        return self._show_time

    @property
    def show_duration(self) -> int:
        return self._show_duration

    @property
    def pricing_strategy(self) -> PricingStrategy:
        return self._pricing_strategy

    @pricing_strategy.setter
    def pricing_strategy(self, pricing_strategy: PricingStrategy) -> None:
        self._pricing_strategy = pricing_strategy

    @property
    def status(self) -> ShowStatus:
        return self._status

    @property
    def seat_layout(self) -> SeatLayout:
        return self._screen.seat_layout

    @status.setter
    def status(self, status: ShowStatus) -> None:
        self._status = status

    def get_show_end_time(self) -> datetime:
        """Get the end time of the show."""
        return self._show_time + timedelta(minutes=self._show_duration)

    def calculate_seat_price(self, seat_row_num: int, seat_col_num: int) -> float:
        """
        Calculate the price for a specific seat using the show's pricing strategy.

        OOP Principles:
        - Strategy Pattern: Delegates pricing to the show's pricing strategy
        - Encapsulation: Pricing logic is encapsulated in the strategy
        - Single Responsibility: Show handles show logic, strategy handles pricing

        Args:
            seat_id: ID of the seat to calculate price for

        Returns:
            float: Calculated price for the seat
        """
        seat = self._find_seat_by_row_col(seat_row_num, seat_col_num)
        print("seat: ", seat)
        if seat:
            return seat.calculate_price(self._pricing_strategy)
        return 0.0

    def _find_seat_by_row_col(self, seat_row_num: int, seat_col_num: int):
        """Find a seat in the show's screen layout by seat ID."""

        return self._screen.seat_layout.get_seat(seat_row_num, seat_col_num)

    def __str__(self) -> str:
        return (
            f"Show({self._show_id}, {self._movie.movie_name}, "
            f"{self._show_time}, {self._status})"
        )


if __name__ == "__main__":
    # Example usage
    from Movie import Movie, MovieLanguage, MovieGenre
    from Screen import IMAXScreen
    from SeatPricingStrategy import PricingStrategyFactory

    # Create a movie
    movie = Movie(
        movie_id="M001",
        movie_name="The Dark Knight",
        movie_duration=152,
        movie_language=MovieLanguage.ENGLISH,
        movie_genre=MovieGenre.ACTION,
        movie_rating=9.0,
        movie_release_date="2008-07-18",
        movie_director="Christopher Nolan",
        movie_cast="Christian Bale, Heath Ledger, Aaron Eckhart",
        movie_trailer_url="https://www.youtube.com/watch?v=EXeTwQWrcwY",
    )

    # Create a screen
    screen = IMAXScreen(
        screen_id="S001",
        screen_name="IMAX Screen 1",
        screen_capacity=10,
        num_rows=2,
        seats_per_row=[5, 5],
    )

    # Create a show with default pricing strategy
    show_time = datetime.now().replace(hour=14, minute=30, second=0, microsecond=0)

    show = Show(
        show_id="SH001",
        movie=movie,
        screen=screen,
        show_time=show_time,
        show_duration=152,
        pricing_strategy=PricingStrategyFactory.create_default_strategy(),
    )

    print("--------------------------------")
    print("Show: ", show)
    print("--------------------------------")
    print("Show seat layout: ", show.screen.seat_layout)
    print("--------------------------------")
    print("Show price for seat 1: ", show.calculate_seat_price(1, 1))
    print("--------------------------------")
    # Change to holiday pricing strategy
    holiday_strategy = PricingStrategyFactory.create_holiday_strategy()
    show.pricing_strategy = holiday_strategy
    print(f"Updated pricing strategy: {show.pricing_strategy}")
    print("--------------------------------")
    print("Show price for seat 1: ", show.calculate_seat_price(1, 1))
    print("--------------------------------")
