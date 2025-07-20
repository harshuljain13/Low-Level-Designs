from typing import List
from Seat import Seat


class SeatLayout:
    def __init__(self, num_rows: int, seats_per_row: List[int]):
        self.num_rows = num_rows
        self.seats_per_row = seats_per_row
        self.seats = [[] for _ in range(num_rows)]
        
    @property
    def num_rows(self) -> int:
        return self._num_rows
    
    @property
    def seats_per_row(self) -> List[int]:
        return self._seats_per_row
    
    @property
    def seats(self) -> List[List[Seat]]:
        return self._seats
    
    def add_seat(self, seat: Seat, row: int, col: int) -> None:
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.seats_per_row[row]:
            raise ValueError("Invalid row or column")
        print(f"Adding seat {seat} to row {row} and column {col}")
        self.seats[row][col] = seat
    
    def remove_seat(self, row: int, col: int) -> None:
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.seats_per_row[row]:
            raise ValueError("Invalid row or column")
        print(f"Removing seat at row {row} and column {col}")
        self.seats[row][col] = None
    
    def get_seat(self, row: int, col: int) -> Seat:
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.seats_per_row[row]:
            raise ValueError("Invalid row or column")
        return self.seats[row][col]
