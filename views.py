from datetime import datetime

from flask import current_app, render_template


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def movies_page():
    db = current_app.config["db"]
    movies = db.get_movies()
    return render_template("movies.html", movies=sorted(movies))

    