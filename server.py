from flask import Flask
from flask_login import LoginManager
from passlib.hash import pbkdf2_sha256 as hasher
import os

import views
from database import Database
from user import get_user

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
      

    app.add_url_rule("/", view_func=views.home_page, methods=["GET", "POST"])
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/signup", view_func=views.signup_page, methods=["GET", "POST"])
    app.add_url_rule("/profile", view_func=views.profile_page)
    app.add_url_rule("/add_movie", view_func=views.add_movie_new_page, methods=["GET", "POST"])
    app.add_url_rule("/delete_movie/<string:imdb_title_id>", view_func=views.delete_movie_page)
    app.add_url_rule("/update_movie/<string:imdb_title_id>", view_func=views.update_avg_vote_page, methods=["GET", "POST"])
    app.add_url_rule("/add_person", view_func=views.add_person_page, methods=["GET", "POST"])
    app.add_url_rule("/delete_person/<string:imdb_name_id>", view_func=views.delete_person_page)
    app.add_url_rule("/update_person/<string:imdb_name_id>", view_func=views.update_height_page, methods=["GET", "POST"])
    app.add_url_rule("/bio", view_func=views.bio_page, methods = ["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/users", view_func=views.users_page)
    app.add_url_rule("/delete_user", view_func=views.delete_profile_page)
    app.add_url_rule("/movie/<string:imdb_id>", view_func=views.movie_new)
    app.add_url_rule("/movie/<string:imdb_id>/casting", view_func=views.casting_page)
    app.add_url_rule("/casting_delete/<string:imdb_title_id>/<string:imdb_name_id>/<int:ordering>", view_func=views.delete_from_casting_page)
    app.add_url_rule("/update_category/<string:imdb_title_id>/<string:imdb_name_id>/<int:ordering>", view_func=views.update_category_page, methods=["GET","POST"])
    app.add_url_rule("/add_casting", view_func=views.add_casting_page, methods=["GET", "POST"])
    app.add_url_rule("/person/<string:imdb_name_id>", view_func=views.person_page)
    app.add_url_rule("/search", view_func=views.search_movies_page) 
    app.add_url_rule("/upload", view_func=views.upload_page, methods=["GET", "POST"])

    lm.init_app(app)
    lm.login_view = "login_page"

    """db = Database()
    db.add_movie(Movie("Slaughterhouse-Five", year=1972))
    db.add_movie(Movie("The Shining"))
    app.config["db"] = db"""

    """current_directory = os.getcwd()
    print(current_directory)
    db = Database(os.path.join(current_directory, "database.sqlite"))
    app.config["db"] = db"""


    
    db = Database("host='localhost' user='postgres' password='password' dbname='DBProject'")
    app.config["db"] = db
   
    return app


app = create_app()

if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)