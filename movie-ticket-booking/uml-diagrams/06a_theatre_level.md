# Theatre Level UML Diagram

## Theatre Management

```mermaid
classDiagram
    direction LR
    
    class Theatre {
        -_theatre_id: str
        -_theatre_name: str
        -_theatre_location: str
        -_status: TheatreStatus
        -_screens: List[Screen]
        -_shows: List[Show]
        +theatre_id: str
        +theatre_name: str
        +theatre_location: str
        +status: TheatreStatus
        +total_screens: int
        +total_shows: int
        +add_screen(screen: Screen): void
        +remove_screen(screen: Screen): void
        +add_show(show: Show): void
        +remove_show(show: Show): void
    }
    
    class TheatreStatus {
        <<enumeration>>
        ACTIVE
        INACTIVE
        MAINTENANCE
        CLOSED
    }
    
    class Screen {
        -_screen_id: str
        -_screen_name: str
        -_capacity: int
        +screen_id: str
        +screen_name: str
        +capacity: int
    }
    
    class Show {
        -_show_id: str
        -_show_time: datetime
        -_status: ShowStatus
        +show_id: str
        +show_time: datetime
        +status: ShowStatus
    }
    
    Theatre *-- TheatreStatus : has
    Theatre *-- Screen : contains
    Theatre *-- Show : contains
```

## Description
This diagram shows the Theatre-level view focusing on theatre management. The Theatre contains multiple Screens and Shows, with a status indicating its operational state. Simplified to show only essential theatre-level operations and relationships. 