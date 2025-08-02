# Movie System UML Diagram

## Step 1: Movie System Classes and Enums

```mermaid
classDiagram
    direction LR
    
    class Movie {
        -_movie_id: str
        -_movie_name: str
        -_movie_duration: int
        -_movie_language: MovieLanguage
        -_movie_genre: MovieGenre
        -_movie_rating: float
        +movie_id: str
        +movie_name: str
        +movie_duration: int
        +movie_language: MovieLanguage
        +movie_genre: MovieGenre
        +movie_rating: float
        +__str__(): str
    }
    
    class MovieLanguage {
        <<enumeration>>
        ENGLISH
        HINDI
        MARATHI
        TAMIL
        TELUGU
    }
    
    class MovieGenre {
        <<enumeration>>
        ACTION
        COMEDY
        DRAMA
        HORROR
        ROMANCE
        SCI_FI
    }
    
    Movie *-- MovieLanguage : has
    Movie *-- MovieGenre : has
```

## Description
This diagram shows the simplified Movie class with its core properties and the associated enums for language and genre. The Movie class focuses on essential movie information needed for the booking system: ID, name, duration, language, genre, and rating. Additional details like director, cast, release date, and trailer URL have been removed to keep the diagram clean and focused. The layout is arranged horizontally for better readability. 