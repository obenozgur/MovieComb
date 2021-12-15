import psycopg2 as dbapi2
from psycopg2.extras import RealDictCursor

from movie import Movie, MovieNew, MovieShort
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

            """ab = row["username"]
            print(ab)
            print("---")
            if(row["password"] is None):
                print("NONEEE")
            print("---")"""


            if(row is None):
                print("yok") #CHECK THAT
                return User(None, None)
            else:
                username = row["username"]
                password = row["password"]
                print("Hey" + str(username) + " " + str(password))
                user_ = User(username, password)
                return user_

    
        """def search_movie(self, title, score, language, genre_list):
        with dbapi2.connect(self.dbfile,cursor_factory=RealDictCursor) as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM movies WHERE avg_vote >= {}".format(score)

            if language == "en":
                query = query + " AND language LIKE '%English%'"
            elif language == "tr":
                query = query + " AND language LIKE '%Turkish%'"

            if title != "":
                query = query + " AND original_title LIKE '%{}%'".format(title)

            if genre_list:
                query = query + " AND ("
                for genre in genre_list:
                    query = query + "genre LIKE '%{}%' AND ".format(genre)
                
                query = query[:-4]
                query = query + ")"


            print(query)

            moviedict = {
                "imdb_title_id": "Unknown",
                "title": "Unknown",
                "original_title": "Unknown",
                "year": "Unknown",
                "date_published": "Unknown",
                "genre": "Unknown",
                "duration": "Unknown",
                "country": "Unknown",
                "language": "Unknown",
                "director": "Unknown",
                "actors": "Unknown",
                "description": "Unknown",
                "avg_vote": "Unknown",
                "votes": "Unknown"
                }

            cursor.execute(query)
            rows = cursor.fetchall()

            #print(len(rows))

            MoviesNew = []

            #for i in rows:
                #print(i["original_title"])

            for row in rows:
                for column in row:
                    if(not row[str(column)] is None):
                        moviedict[str(column)] = row[str(column)]
                        #print(moviedict[str(column)])

                movie = MovieNew(moviedict["imdb_title_id"],moviedict["title"],moviedict["original_title"],moviedict["year"],moviedict["date_published"],moviedict["genre"],moviedict["duration"],moviedict["country"],moviedict["language"],moviedict["director"],moviedict["actors"],moviedict["description"],moviedict["avg_vote"],moviedict["votes"])
                MoviesNew.append(movie)

                for key in moviedict:
                    moviedict[key] = "Unknown"

            print((MoviesNew[0].original_title))
                

            #for movie in MoviesNew:
                #print(movie.original_title)




                    





            #query = "SELECT TITLE, YR FROM MOVIE WHERE (ID = {})".format(movie_key)
            #cursor.execute(query)
            #title, year = cursor.fetchone()
        #movie_ = Movie(title, year=year)
        #return movie_

        return 1"""
    
    def search_movie(self, title, score, language, genre_list):
        with dbapi2.connect(self.dbfile,cursor_factory=RealDictCursor) as connection:
            cursor = connection.cursor()

            query = "SELECT imdb_title_id, title, original_title, year, director FROM movies WHERE avg_vote >= {}".format(score)

            if language == "en":
                query = query + " AND language LIKE '%English%'"
            elif language == "tr":
                query = query + " AND language LIKE '%Turkish%'"

            if title != "":
                query = query + " AND original_title ILIKE '%{}%'".format(title)

            if genre_list:
                query = query + " AND ("
                for genre in genre_list:
                    query = query + "genre LIKE '%{}%' AND ".format(genre)
                
                query = query[:-4]
                query = query + ")"

            query = query + " ORDER BY year DESC"

            print(query)

            moviedict = {
                "imdb_title_id": "Unknown",
                "title": "Unknown",
                "original_title": "Unknown",
                "year": "Unknown",
                "director": "Unknown"
                }

            cursor.execute(query)
            rows = cursor.fetchall()

            #print(len(rows))

            movies = []

            #for i in rows:
                #print(i["original_title"])

            for row in rows:
                for column in row:
                    if(not row[str(column)] is None):
                        moviedict[str(column)] = row[str(column)]
                        #print(moviedict[str(column)])

                movie = MovieShort(moviedict["imdb_title_id"],moviedict["title"],moviedict["original_title"],moviedict["year"],moviedict["director"])
                movies.append(movie)

                for key in moviedict:
                    moviedict[key] = "Unknown"

            #print(len(movies))
            
        return movies

    


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
        
        

       


    
            



