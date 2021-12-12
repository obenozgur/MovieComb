import psycopg2 as dbapi2
from psycopg2.extras import RealDictCursor

from movie import Movie, MovieNew
from user import User


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_movie(self, movie):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO MOVIE (TITLE, YR) VALUES('{}', {}) RETURNING ID".format(movie.title, movie.year)
            cursor.execute(query)
            movie_key = cursor.fetchone()[0]
            connection.commit()
        return movie_key

    def update_movie(self, movie_key, movie):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE MOVIE SET TITLE = '{}', YR = {} WHERE (ID = {})".format(movie.title, movie.year, movie_key)
            cursor.execute(query)
            connection.commit()

    def delete_movie(self, movie_key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM MOVIE WHERE (ID = {})".format(movie_key)
            cursor.execute(query)
            connection.commit()

    def get_movie(self, movie_key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT TITLE, YR FROM MOVIE WHERE (ID = {})".format(movie_key)
            cursor.execute(query)
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

    def get_user(self, user_id):
        with dbapi2.connect(self.dbfile,cursor_factory=RealDictCursor) as connection:
            cursor = connection.cursor()
            query = "SELECT USERNAME, PASSWORD FROM users WHERE USERNAME = '{}'".format(user_id)
            cursor.execute(query)
            
            """if number_of_rows > 0:
                print("YOK")"""
            
            row = cursor.fetchone()


            if(row is None):
                print("yok")
                return User(None, None)
            else:
                username = row["username"]
                password = row["password"]
                print("Hey" + str(username) + " " + str(password))
                user_ = User(username, password)
                return user_

    
    def search_movie(self, title, score, language, genre_list):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()


            

            query = "SELECT imdb_title_id, title, original_title, year FROM movies WHERE avg_vote >= {}".format(score)

            if language == "en":
                query = query + " AND language LIKE '%English%'"
            elif language == "tr":
                query = query + " AND language LIKE '%Turkish%'"

            if title != "":
                query = query + " AND original_title LIKE '%{}%'".format(title)

            if genre_list:
                query = query + " AND ("
                for genre in genre_list:
                    query = query + "genre LIKE '%{}%' OR ".format(genre)
                
                query = query[:-4]
                query = query + ")"


            print(query)


            #query = "SELECT TITLE, YR FROM MOVIE WHERE (ID = {})".format(movie_key)
            #cursor.execute(query)
            #title, year = cursor.fetchone()
        #movie_ = Movie(title, year=year)
        #return movie_

        return 1


    def write_blob(self, part_id, path_to_file, file_extension):
        with dbapi2.connect(self.dbfile) as connection:
            image = open(path_to_file, 'rb').read()
            cursor = connection.cursor()
            query = "INSERT INTO blobum(id,file_extension,data) VALUES({},'{}',{})".format(part_id, file_extension, dbapi2.Binary(image)) 
            cursor.execute(query)


    def read_blob(self, part_id, path_to_dir):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT id,file_extension,data FROM blobum WHERE id = {}".format(part_id)
            cursor.execute(query)

            blob = cursor.fetchone()
            open(path_to_dir + str(blob[0]) + '.' + str(blob[1]), 'wb').write(blob[2])
        
        

       


    
            



