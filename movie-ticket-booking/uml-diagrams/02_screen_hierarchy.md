# Screen Hierarchy UML Diagram

## Step 2: Screen System with Inheritance

```mermaid
classDiagram
    class Screen {
        <<abstract>>
        -_screen_id: str
        -_screen_name: str
        -_screen_type: ScreenType
        -_screen_capacity: int
        -_num_rows: int
        -_seats_per_row: List[int]
        -_seat_layout: SeatLayout
        +screen_id: str
        +screen_name: str
        +screen_type: ScreenType
        +screen_capacity: int
        +seat_layout: SeatLayout
        +seats: List[Seat]
        +prepare_seat_layout()*: void
    }
    
    class IMAXScreen {
        +prepare_seat_layout(): void
    }
    
    class ThreeD {
        +prepare_seat_layout(): void
    }
    
    class ScreenType {
        <<enumeration>>
        IMAX
        THREE_D
        REGULAR
    }
    
    Screen <|-- IMAXScreen
    Screen <|-- ThreeD
    Screen *-- ScreenType : has
```

## Description
This diagram shows the Screen abstract class with its concrete implementations (IMAXScreen and ThreeD). The abstract class defines the interface for all screen types, and each concrete class implements its own seat layout preparation logic. The ScreenType enum defines the different types of screens available. 