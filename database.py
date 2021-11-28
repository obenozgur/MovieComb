import sqlite3 as dbapi2

from movie import Movie


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_movie(self, movie):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO MOVIE (TITLE, YR) VALUES (?, ?)"
            cursor.execute(query, (movie.title, movie.year))
            connection.commit()
            movie_key = cursor.lastrowid
        return movie_key

    def update_movie(self, movie_key, movie):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE MOVIE SET TITLE = ?, YR = ? WHERE (ID = ?)"
            cursor.execute(query, (movie.title, movie.year, movie_key))
            connection.commit()

    def delete_movie(self, movie_key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM MOVIE WHERE (ID = ?)"
            cursor.execute(query, (movie_key,))
            connection.commit()

    def get_movie(self, movie_key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT TITLE, YR FROM MOVIE WHERE (ID = ?)"
            cursor.execute(query, (movie_key,))
            title, year = cursor.fetchone()
        movie_ = Movie(title, year=year)
        return movie_

    def get_movies(self):
        movies = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, TITLE, YR FROM MOVIE ORDER BY ID"
            cursor.execute(query)
            for movie_key, title, year in cursor:
                movies.append((movie_key, Movie(title, year)))
        return movies