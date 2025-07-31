from typing import List
from Seat import Seat
from SeatPricingStrategy import SeatType
from Seat import SeatFactory


class SeatLayout:
    """
    Manages the arrangement and access of seats on a screen.

    OOP Principles Demonstrated:
    1. ENCAPSULATION: Encapsulates seat grid and seat access logic.
    2. SINGLE RESPONSIBILITY: Only manages seat layout, not seat pricing or booking.
    3. OPEN/CLOSED: Can extend with new seat arrangement logic.

    Responsibilities:
    - Holds seat grid for a screen
    - Provides methods to add, remove, and get seats
    - Validates row and column indices
    """

    def __init__(self, num_rows: int, seats_per_row: List[int]):
        self._num_rows = num_rows
        self._seats_per_row = seats_per_row
        self._seats = [[] for _ in range(self._num_rows)]
        for i in range(self._num_rows):
            for j in range(self._seats_per_row[i]):
                self._seats[i].append(None)

    @property
    def num_rows(self) -> int:
        return self._num_rows

    @property
    def seats_per_row(self) -> List[int]:
        return self._seats_per_row

    @property
    def seats(self) -> List[List[Seat]]:
        return self._seats

    # add seat to the seat layout
    def add_seat(self, seat: Seat, row: int, col: int) -> None:
        if (
            row < 0
            or row >= self._num_rows
            or col < 0
            or col >= self.seats_per_row[row]
        ):
            raise ValueError("Invalid row or column")
        print(f"Adding seat {seat} to row {row} and column {col}")
        self._seats[row].append(seat)
        self._seats[row][col] = seat

    # remove seat from the seat layout
    def remove_seat(self, row: int, col: int) -> None:
        if (
            row < 0
            or row >= self._num_rows
            or col < 0
            or col >= self.seats_per_row[row]
        ):
            raise ValueError("Invalid row or column")
        print(f"Removing seat at row {row} and column {col}")
        self._seats[row][col] = None

    # get seat from the seat layout
    def get_seat(self, row: int, col: int) -> Seat:
        if (
            row < 0
            or row >= self._num_rows
            or col < 0
            or col >= self.seats_per_row[row]
        ):
            raise ValueError("Invalid row or column")
        return self._seats[row][col]

    def __str__(self):
        return f"SeatLayout(num_rows={self._num_rows}, seats_per_row={self._seats_per_row})"


if __name__ == "__main__":
    # create a seat layout
    seat_layout = SeatLayout(
        num_rows=10, seats_per_row=[10, 10, 10, 10, 10, 10, 5, 5, 5, 5]
    )
    # add a seat to the seat layout
    seat_layout.add_seat(
        SeatFactory.create_seat(SeatType.PREMIUM, "TEST001", "S1", base_price=100.0),
        row=1,
        col=1,
    )
    seat_layout.add_seat(
        SeatFactory.create_seat(SeatType.REGULAR, "TEST002", "S2", base_price=100.0),
        row=2,
        col=2,
    )

    # remove a seat from the seat layout
    seat_layout.remove_seat(row=1, col=1)
    # get a seat from the seat layout
    seat_1 = seat_layout.get_seat(row=2, col=2)
    print("Seat at row 2, col 2: ", seat_1)
    seat_2 = seat_layout.get_seat(row=1, col=1)
    print("Seat at row 1, col 1: ", seat_2)

    print("Seat layout: ", seat_layout.seats)
