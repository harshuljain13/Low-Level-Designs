'''
This module contains the Movie class, which represents a movie.
'''
from enum import Enum


class MovieLanguage(Enum):
    '''
    This enum represents the language of a movie.
    '''
    ENGLISH = "English"
    HINDI = "Hindi"
    MARATHI = "Marathi"
    TAMIL = "Tamil"
    TELUGU = "Telugu"


class MovieGenre(Enum):
    '''
    This enum represents the genre of a movie.
    '''
    ACTION = "Action"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    HORROR = "Horror"
    ROMANCE = "Romance"
    SCI_FI = "Sci-Fi"


class Movie:
    """
    Movie class for movie ticket booking system.

    OOP Principles:
    - Encapsulation: Encapsulates movie data.
    - Inheritance: Inherits from Movie class.
    - Polymorphism: Polymorphic behavior for movie data.
    - Abstraction: Abstracts movie data.
    """

    def __init__(
        self,
        movie_id: str,
        movie_name: str,
        movie_duration: int,
        movie_language: MovieLanguage,
        movie_genre: str,
        movie_rating: float,
        movie_release_date: str,
        movie_director: str,
        movie_cast: str,
        movie_trailer_url: str,
    ):
        self._movie_id = movie_id
        self._movie_name = movie_name
        self._movie_duration = movie_duration
        self._movie_language = movie_language
        self._movie_genre = movie_genre
        self._movie_rating = movie_rating
        self._movie_release_date = movie_release_date
        self._movie_director = movie_director
        self._movie_cast = movie_cast
        self._movie_trailer_url = movie_trailer_url

    @property
    def movie_id(self) -> str:
        '''
        This method returns the ID of the movie.
        '''
        return self._movie_id

    @property
    def movie_name(self) -> str:
        '''
        This method returns the name of the movie.
        '''
        return self._movie_name

    @property
    def movie_duration(self) -> int:
        '''
        This method returns the duration of the movie.
        '''
        return self._movie_duration

    @property
    def movie_language(self) -> str:
        '''
        This method returns the language of the movie.
        '''
        return self._movie_language

    @property
    def movie_genre(self) -> str:
        '''
        This method returns the genre of the movie.
        '''
        return self._movie_genre

    @property
    def movie_rating(self) -> float:
        '''
        This method returns the rating of the movie.
        '''
        return self._movie_rating

    @property
    def movie_release_date(self) -> str:
        '''
        This method returns the release date of the movie.
        '''
        return self._movie_release_date

    @property
    def movie_director(self) -> str:
        '''
        This method returns the director of the movie.
        '''
        return self._movie_director

    @property
    def movie_cast(self) -> str:
        '''
        This method returns the cast of the movie.
        '''
        return self._movie_cast

    @property
    def movie_trailer_url(self) -> str:
        '''
        This method returns the trailer URL of the movie.
        '''
        return self._movie_trailer_url

    def __str__(self) -> str:
        return (
            "Movie("
            f"movie_id={self._movie_id}, "
            f"movie_name={self._movie_name}, "
            f"movie_duration={self._movie_duration}, "
            f"movie_language={self._movie_language}, "
            f"movie_genre={self._movie_genre}, "
            f"movie_rating={self._movie_rating}, "
            f"movie_release_date={self._movie_release_date}, "
            f"movie_director={self._movie_director}, "
            f"movie_cast={self._movie_cast}, "
            f"movie_trailer_url={self._movie_trailer_url}"
            ")"
        )


if __name__ == "__main__":
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
    print(movie)
