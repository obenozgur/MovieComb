from movie import Movie


class Database:
    def __init__(self):
        self.movies = {}
        self._last_movie_key = 0

    def add_movie(self, movie):
        self._last_movie_key += 1
        self.movies[self._last_movie_key] = movie
        return self._last_movie_key

    def delete_movie(self, movie_key):
        if movie_key in self.movies:
            del self.movies[movie_key]

    def get_movie(self, movie_key):
        movie = self.movies.get(movie_key)
        if movie is None:
            return None
        movie_ = Movie(movie.title, year=movie.year)
        return movie_

    def get_movies(self):
        movies = []
        for movie_key, movie in self.movies.items():
            movie_ = Movie(movie.title, year=movie.year)
            movies.append((movie_key, movie_))
        return movies
