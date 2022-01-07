import psycopg2 as dbapi2
from psycopg2.extras import RealDictCursor

from movie import Movie, MovieShort
from person import Person, PersonShort
from review import Review
from user import User


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_movie_new(self, movie):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            i = 0
            while(True):
                query = "SELECT imdb_title_id FROM movies WHERE imdb_title_id = '{}'".format(i)
                cursor.execute(query)
                row = cursor.fetchone()
                if row is None:
                    break
                else:
                    i += 1
            
            query = "INSERT INTO movies (imdb_title_id, original_title, year, avg_vote) VALUES ('{}','{}',{},{})".format(i, movie.original_title, movie.year, movie.avg_vote)
            cursor.execute(query)
            return i

    def insert_review(self, username, review, imdb_title_id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO reviews (imdb_title_id, username, review) VALUES ('{}','{}','{}')".format(imdb_title_id, username, review)
            cursor.execute(query)

    def get_reviews(self, imdb_title_id):
        with dbapi2.connect(self.dbfile,cursor_factory=RealDictCursor) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM reviews WHERE imdb_title_id = '{}'".format(imdb_title_id)
            reviews = []
            cursor.execute(query)

            rows = cursor.fetchall()

            for row in rows:
                review = Review(row["username"], row["review"])
                reviews.append(review)

            return reviews



    def add_person(self, person):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            i = 0
            while(True):
                query = "SELECT imdb_name_id FROM names WHERE imdb_name_id = '{}'".format(i)
                cursor.execute(query)
                row = cursor.fetchone()
                if row is None:
                    break
                else:
                    i += 1
            
            query = "INSERT INTO names (imdb_name_id, name, birth_name, height) VALUES ('{}','{}','{}',{})".format(i, person.name, person.birth_name, person.height)
            cursor.execute(query)
            return i

    def add_casting(self, imdb_title_id, imdb_name_id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            i = 1
            while(True):
                query = "SELECT * FROM title_principals WHERE imdb_title_id = '{}' AND ordering = {}".format(imdb_title_id, i)
                cursor.execute(query)
                row = cursor.fetchone()
                if row is None:
                    break
                else:
                    i += 1

            query = "INSERT INTO title_principals (imdb_title_id, imdb_name_id, ordering) VALUES ('{}','{}',{})".format(imdb_title_id, imdb_name_id, i)
            cursor.execute(query)
            return i

    def delete_from_casting(self, imdb_title_id, imdb_name_id, ordering):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM title_principals WHERE imdb_title_id = '{}' AND imdb_name_id = '{}' AND ordering = {}".format(imdb_title_id, imdb_name_id, ordering)
            cursor.execute(query)
            return True


    def update_category(self, imdb_title_id, imdb_name_id, ordering, category):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE title_principals SET category = '{}' WHERE imdb_title_id = '{}' AND imdb_name_id = '{}' AND ordering = {}".format(category, imdb_title_id, imdb_name_id, ordering)
            cursor.execute(query)
            connection.commit()


    def delete_person(self, imdb_name_id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM names WHERE imdb_name_id = '{}'".format(imdb_name_id)
            cursor.execute(query)
            connection.commit()

    def update_height(self, imdb_name_id, height):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE names SET height = {} WHERE imdb_name_id = '{}'".format(height, imdb_name_id)
            cursor.execute(query)
            connection.commit()

    def delete_movie_new(self, imdb_title_id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM movies WHERE imdb_title_id = '{}'".format(imdb_title_id)
            cursor.execute(query)
            connection.commit()

    def update_avg_vote(self, imdb_title_id, avg_vote):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE movies SET avg_vote = {} WHERE imdb_title_id = '{}'".format(avg_vote, imdb_title_id)
            cursor.execute(query)
            connection.commit()


    def get_movie_new(self, imdb_id):
        with dbapi2.connect(self.dbfile,cursor_factory=RealDictCursor) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM movies WHERE imdb_title_id = '{}'".format(imdb_id)
            cursor.execute(query)
            row = cursor.fetchone()

            if row is None:
                return None

            movie = Movie(row["imdb_title_id"], row["original_title"], row["year"], row["date_published"], row["genre"], row["duration"], row["country"], row["language"], row["director"], row["actors"], row["description"], row["avg_vote"], row["votes"])
            return movie

    def get_persons(self, imdb_id):
        with dbapi2.connect(self.dbfile,cursor_factory=RealDictCursor) as connection:
            cursor = connection.cursor()

            query = """select names.imdb_name_id, name, category, characters, ordering from 
	                    movies join title_principals on movies.imdb_title_id = title_principals.imdb_title_id 
	                    join names on title_principals.imdb_name_id = names.imdb_name_id
	                    where movies.imdb_title_id = '{}'
	                    order by ordering""".format(imdb_id)

            cursor.execute(query)
            rows = cursor.fetchall()


            personshorts = []


            moviedict = {
                "imdb_name_id": "",
                "name": "",
                "category": "",
                "characters": "",
                "ordering": ""
                }


            for row in rows:
                for column in row:
                    if(not row[str(column)] is None):
                        moviedict[str(column)] = row[str(column)]

                person = PersonShort(moviedict["imdb_name_id"],moviedict["name"],moviedict["category"],moviedict["characters"],moviedict["ordering"])
                personshorts.append(person)

                for key in moviedict:
                    moviedict[key] = ""
            
        return personshorts

    def get_person(self, imdb_name_id):
        with dbapi2.connect(self.dbfile,cursor_factory=RealDictCursor) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM names WHERE imdb_name_id = '{}'".format(imdb_name_id)
            cursor.execute(query)
            row = cursor.fetchone()
            if row is None:
                return None
            person = Person(row["imdb_name_id"], row["name"], row["birth_name"], row["height"], row["bio"], row["date_of_birth"], row["place_of_birth"], row["date_of_death"], row["place_of_death"])
            return person
        

    def get_user(self, username):
        with dbapi2.connect(self.dbfile, cursor_factory=RealDictCursor) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username = '{}'".format(username)
            cursor.execute(query)

            row = cursor.fetchone()

            if row is None:
                return None
            else:
                username = row["username"]
                password = row["password"]
                bio = row["bio"]
                file_extension = row["file_extension"]
                if not row["pp"] is None:
                    self.read_pp(username, "static/pps/")

                user_ = User(username, password, bio, file_extension)
                return user_

    def get_all_users(self):
        with dbapi2.connect(self.dbfile, cursor_factory=RealDictCursor) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM users ORDER by username ASC"
            cursor.execute(query)

            rows = cursor.fetchall()

            users = []

            for row in rows:
                user_ = (User(row["username"], row["password"], row["bio"], row["file_extension"]))
                self.get_user(row["username"]) ##for profile pictures
                users.append(user_)

            return users

    def insert_user(self, username, password):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO users (username,password) VALUES ('{}','{}')".format(username, password)
            cursor.execute(query)

    def update_bio(self, username, bio):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE users SET bio = '{}'WHERE username = '{}'".format(bio, username)
            cursor.execute(query) 
           


    def delete_user(self, username):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM users WHERE username = '{}'".format(username)
            cursor.execute(query)


    def read_pp(self, username, path_to_dir):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT username,file_extension,pp FROM users WHERE username = '{}'".format(username)
            cursor.execute(query)

            blob = cursor.fetchone()
            open(path_to_dir + str(blob[0]) + str(blob[1]), 'wb').write(blob[2])

    def write_pp(self, username, path_to_file, file_extension):
        with dbapi2.connect(self.dbfile) as connection:
            image = open(path_to_file, 'rb').read()
            cursor = connection.cursor()
            query = "UPDATE users SET file_extension = '{}', pp = {} WHERE username = '{}'".format(file_extension, dbapi2.Binary(image), username) 
            cursor.execute(query)
                

    def search_movie(self, title, score, language, genre_list):
        with dbapi2.connect(self.dbfile,cursor_factory=RealDictCursor) as connection:
            cursor = connection.cursor()

            query = "SELECT imdb_title_id, original_title, year, director FROM movies WHERE avg_vote >= {}".format(score)

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

            moviedict = {
                "imdb_title_id": "Unknown",
                "original_title": "Unknown",
                "year": "Unknown",
                "director": "Unknown"
                }

            cursor.execute(query)
            rows = cursor.fetchall()


            movies = []


            for row in rows:
                for column in row:
                    if(not row[str(column)] is None):
                        moviedict[str(column)] = row[str(column)]

                movie = MovieShort(moviedict["imdb_title_id"],moviedict["original_title"],moviedict["year"],moviedict["director"])
                movies.append(movie)

                for key in moviedict:
                    moviedict[key] = "Unknown"

            
        return movies
    
        
        

       


    
            



