from abc import ABC, abstractmethod
from typing import List
from Seat import Seat, PremiumSeat, RegularSeat, ReclinerSeat
from enum import Enum
from SeatLayout import SeatLayout


class ScreenType(Enum):
    IMAX = "IMAX"
    THREE_D = "3D"
    REGULAR = "Regular"


class Screen(ABC):
    def __init__(self, screen_id: str, screen_name: str, screen_type: str, screen_capacity: int, 
                 num_rows: int, seats_per_row: List[int]):
        self.screen_id = screen_id
        self.screen_name = screen_name
        self.screen_type = screen_type
        self.screen_capacity = screen_capacity
        self.num_rows = num_rows
        self.seats_per_row = seats_per_row
        self.seat_layout = SeatLayout(num_rows, seats_per_row)

    @property
    def screen_id(self) -> str:
        return self._screen_id
    
    @property
    def screen_name(self) -> str:
        return self._screen_name
    
    @property
    def screen_type(self) -> ScreenType:
        return self._screen_type
    
    @property
    def screen_capacity(self) -> int:
        return self._screen_capacity
    
    @property
    def seats(self) -> List[Seat]:
        return self._seats

    @abstractmethod
    def prepare_seat_layout(self) -> None:
        pass


class IMAXScreen(Screen):
    def __init__(self, screen_id: str, screen_name: str, screen_capacity: int, 
                 num_rows: int, seats_per_row: List[int]):
        super().__init__(screen_id, screen_name, 
                         ScreenType.IMAX, screen_capacity, 
                         num_rows, seats_per_row)

    def prepare_seat_layout(self) -> None:
        # first 5 rows are premium seats
        # last 5 rows are regular seats
        for row in range(self.num_rows//2):
            for col in range(self.seats_per_row[row]):
                self.seat_layout.add_seat(PremiumSeat(f"R{row}C{col}", 200), row, col)

        for row in range(self.num_rows//2, self.num_rows):
            for col in range(self.seats_per_row):
                self.seat_layout.add_seat(RegularSeat(f"R{row}C{col}", 100), row, col)

class ThreeD(Screen):
    def __init__(self, screen_id: str, screen_name: str, screen_capacity: int, 
                 num_rows: int, seats_per_row: List[int]):
        super().__init__(screen_id, screen_name, 
                         ScreenType.THREE_D, screen_capacity, 
                         num_rows, seats_per_row)

    def prepare_seat_layout(self) -> None:
        for row in range(self.num_rows//2):
            for col in range(self.seats_per_row[row]):
                self.seat_layout.add_seat(PremiumSeat(f"R{row}C{col}", 200), row, col)

        for row in range(self.num_rows//2, self.num_rows):
            for col in range(self.seats_per_row):
                self.seat_layout.add_seat(ReclinerSeat(f"R{row}C{col}", 100), row, col)