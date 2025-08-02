# Movie System UML Diagram

## Step 1: Movie System Classes and Enums

```mermaid
classDiagram
    class Movie {
        -_movie_id: str
        -_movie_name: str
        -_movie_duration: int
        -_movie_language: MovieLanguage
        -_movie_genre: MovieGenre
        -_movie_rating: float
        -_movie_release_date: str
        -_movie_director: str
        -_movie_cast: str
        -_movie_trailer_url: str
        +movie_id: str
        +movie_name: str
        +movie_duration: int
        +movie_language: MovieLanguage
        +movie_genre: MovieGenre
        +movie_rating: float
        +movie_release_date: str
        +movie_director: str
        +movie_cast: str
        +movie_trailer_url: str
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
This diagram shows the Movie class with its properties and the associated enums for language and genre. The Movie class encapsulates all movie-related data and provides read-only access through properties. 