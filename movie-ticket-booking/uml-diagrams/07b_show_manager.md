# Show Manager UML Diagram

## Show Scheduling & Lifecycle Management

```mermaid
classDiagram
    direction LR
    
    class ShowManager {
        -_buffer_time: timedelta
        +can_schedule_show(new_show: Show, theatre: Theatre): Dict
        +find_available_slots(theatre: Theatre, screen_id: str, date: datetime, duration: int): List[Dict]
        +get_show_schedule(theatre: Theatre, screen_id: str, date: datetime): List[Show]
        +validate_show_transition(show: Show, new_status: ShowStatus): bool
        +can_start_show(show: Show): bool
        +can_cancel_show(show: Show): bool
        +can_complete_show(show: Show): bool
        +start_show(show: Show): bool
        +cancel_show(show: Show): bool
        +complete_show(show: Show): bool
        +_check_time_conflicts(new_show: Show, existing_shows: List[Show]): List[str]
    }
    
    class Show {
        -_show_id: str
        -_movie: Movie
        -_screen: Screen
        -_show_time: datetime
        -_show_duration: int
        -_status: ShowStatus
        +show_id: str
        +movie: Movie
        +screen: Screen
        +show_time: datetime
        +show_duration: int
        +status: ShowStatus
        +get_show_end_time(): datetime
    }
    
    class ShowStatus {
        <<enumeration>>
        SCHEDULED
        RUNNING
        COMPLETED
        CANCELLED
    }
    
    class Theatre {
        -_theatre_id: str
        -_theatre_name: str
        -_screens: List[Screen]
        -_shows: List[Show]
        +theatre_id: str
        +theatre_name: str
        +screens: List[Screen]
        +shows: List[Show]
    }
    
    class Screen {
        -_screen_id: str
        -_screen_name: str
        -_capacity: int
        +screen_id: str
        +screen_name: str
        +capacity: int
    }
    
    class Movie {
        -_movie_id: str
        -_movie_name: str
        -_movie_duration: int
        +movie_id: str
        +movie_name: str
        +movie_duration: int
    }
    
    ShowManager ..> Show : manages lifecycle
    ShowManager ..> Theatre : checks availability
    ShowManager ..> ShowStatus : validates transitions
    Show *-- ShowStatus : has
    Show *-- Movie : has
    Show *-- Screen : uses
    Theatre *-- Screen : contains
    Theatre *-- Show : contains
```

## Description
This diagram shows the ShowManager's responsibilities for show scheduling, validation, and lifecycle management. It handles time conflict checking, show status transitions, and scheduling operations. The ShowManager ensures proper show scheduling and manages the complete lifecycle of shows from scheduling to completion. 