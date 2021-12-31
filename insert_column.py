import psycopg2 as dbapi2
import pandas as pd
from database import Database
from psycopg2.extras import RealDictCursor


ratings_small = pd.read_csv('ratings_small.csv')

print(len(ratings_small))
db = Database("host='localhost' user='postgres' password='password' dbname='DBProject'")

with dbapi2.connect(db.dbfile) as connection:
    cursor = connection.cursor()
    for i in range(len(ratings_small)):
        print(ratings_small["imdb_title_id"][i], ratings_small["mean_vote"][i])
        id = ratings_small["imdb_title_id"][i]
        mean_vote = ratings_small["mean_vote"][i]

        query = "UPDATE title_principals SET mean_vote = {} WHERE imdb_title_id = '{}'".format(mean_vote, id)
        cursor.execute(query)
        connection.commit()