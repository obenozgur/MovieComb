from datetime import datetime
from flask import current_app, render_template, request, redirect, url_for, flash, abort
from flask_login.utils import login_required
from movie import Movie
from person import Person
from passlib.hash import pbkdf2_sha256 as hasher
from user import get_user, User
from forms import LoginForm, SignupForm
from flask_login import login_user, logout_user, current_user
import os
import re



def home_page():
    db = current_app.config["db"]
    if request.method == "GET":
        return render_template("movies_search.html")
    else:
        title = request.form["title"]
        score = request.form["score"]
        lang = request.form["answer"]
        genres = request.form.getlist("genres")

        movies = db.search_movie(title, score, lang, genres)
        return render_template("search.html", movies=movies) 

def profile_page():
    db = current_app.config["db"]
    username = current_user.username
    user = db.get_user(username)

    if not user.file_extension is None:
        folder = os.path.join('static', 'pps')
        full_filename = os.path.join(folder, str(username) + user.file_extension)
    else:
        full_filename = os.path.join('static', 'empty.png')

    return render_template("profile.html", user=user, image=full_filename)

def delete_profile_page():
    db = current_app.config["db"]
    username = current_user.username
    logout_user()
    db.delete_user(username)

    return redirect(url_for("home_page"))

@login_required
def add_movie_new_page():
    if not current_user.is_admin:
        abort(401)
    else:
        if request.method == "GET":
            values = {"title": "", "year": "", "avg_vote": ""}
            return render_template(
                "add_movie.html",
                values=values,
            )
        else:
            valid = validate_movie_form_new(request.form)
            if not valid:
                return render_template(
                    "add_movie.html",
                    min_year=1887,
                    max_year=datetime.now().year,
                    values=request.form,
                    min_score = 0,
                    max_score = 10
                )
            title = request.form.data["title"]
            year = request.form.data["year"]
            avg_vote = request.form.data["avg_vote"]
            movie = Movie("", title, year, "", "", "", "", "", "Unknown", "", "", avg_vote, 0)
            db = current_app.config["db"]
            imdb_title_id = db.add_movie_new(movie)
            return redirect(url_for("movie_new", imdb_id = imdb_title_id))

@login_required
def add_person_page():
    if not current_user.is_admin:
        abort(401)
    else:
        if request.method == "GET":
            values = {"name": "", "birth_name": "", "height": ""}
            return render_template(
                "add_person.html",
                values=values,
            )
        else:
            valid = validate_person_form(request.form)
            if not valid:
                return render_template(
                    "add_person.html",
                    min_height=20,
                    max_height=1000,
                    values=request.form,
                )
            name = request.form.data["name"]
            birth_name = request.form.data["birth_name"]
            height = request.form.data["height"]
            person = Person("", name, birth_name, height, "", "", "", "", "")
            db = current_app.config["db"]
            imdb_name_id = db.add_person(person)
            return redirect(url_for("person_page", imdb_name_id = imdb_name_id))


@login_required
def add_casting_page():
    if not current_user.is_admin:
        abort(401)
    else:
        if request.method == "GET":
            values = {"movie_id": "", "person_id": ""}
            return render_template(
                "add_casting.html",
                values=values
            )
        else:
            valid = validate_casting_form(request.form)
            if not valid:
                return render_template(
                    "add_casting.html",
                    values=request.form,
                )
            imdb_title_id = request.form.data["movie_id"]
            imdb_name_id = request.form.data["person_id"]
            db = current_app.config["db"]
            db.add_casting(imdb_title_id, imdb_name_id)
            return redirect(url_for("casting_page", imdb_id = imdb_title_id))

@login_required
def update_category_page(imdb_title_id, imdb_name_id, ordering):
    if not current_user.is_admin:
        abort(401)
    else:
        if request.method == "GET":
            values = {"category": ""}
            return render_template(
                "update_category.html",
                values=values
            )
        else:
            valid = validate_category_form(request.form)
            if not valid:
                return render_template(
                    "update_category.html",
                    values=request.form,
                )

            category = request.form.data["category"]
            db = current_app.config["db"]
            db.update_category(imdb_title_id, imdb_name_id, ordering, category)
            return redirect(url_for("casting_page", imdb_id = imdb_title_id))
    


def users_page():
    db = current_app.config["db"]
    users = db.get_all_users()
    images  = []
    contents = []

    for user in users:
        if not user.file_extension is None:
            folder = os.path.join('static', 'pps')
            full_filename = os.path.join(folder, str(user.username) + user.file_extension)
        else:
            full_filename = os.path.join('static', 'empty.png')
        
        images.append(full_filename)

    for i in range(len(images)):
        contents.append((users[i], images[i]))


    return render_template("users.html", contents = contents)

@login_required
def add_review_page(imdb_title_id):
    db = current_app.config["db"]

    if request.method == "GET":
        db = current_app.config["db"]
        movie = db.get_movie_new(imdb_title_id)
        values = {"review": ""}
        return render_template("review.html", movie=movie, values=values)
    else:
        valid = validate_review_form(request.form)
        if not valid:
            return render_template("review.html", values = request.form)
        
        review = request.form.data["review_content"]
        db.insert_review(current_user.username, review, imdb_title_id)
        #db.update_bio(current_user.username, bio)
        return redirect(url_for("movie_new", imdb_id = imdb_title_id))



def movie_new(imdb_id):
    db = current_app.config["db"]
    movie = db.get_movie_new(imdb_id)
    reviews = db.get_reviews(imdb_id)
    return render_template("movie_new.html", movie=movie, imdb_id=imdb_id, reviews=reviews)

def delete_movie_page(imdb_title_id):
    db = current_app.config["db"]
    db.delete_movie_new(imdb_title_id)
    return redirect(url_for("home_page"))

def delete_person_page(imdb_name_id):
    db = current_app.config["db"]
    db.delete_person(imdb_name_id)
    return redirect(url_for("home_page"))


@login_required
def update_height_page(imdb_name_id):
    if not current_user.is_admin:
        abort(401)
    else:
        db = current_app.config["db"]
        person = db.get_person(imdb_name_id)

        if request.method == "GET":
            values = {"height": ""}
            return render_template(
                "update_height.html",
                values=values,
                person=person
            )
        else:
            valid = validate_height_form(request.form)
            if not valid:
                return render_template(
                    "update_height.html",
                    values=request.form,
                    min_height = 20,
                    max_height = 1000,
                    person=person
                )
            height = request.form.data["height"]
            db.update_height(imdb_name_id, height)
            return redirect(url_for("person_page", imdb_name_id = imdb_name_id))

    

@login_required
def update_avg_vote_page(imdb_title_id):
    if not current_user.is_admin:
        abort(401)
    else:
        db = current_app.config["db"]
        movie = db.get_movie_new(imdb_title_id)

        if request.method == "GET":
            values = {"avg_vote": ""}
            return render_template(
                "update_avg_vote.html",
                values=values,
                movie=movie
            )
        else:
            valid = validate_score_form(request.form)
            if not valid:
                return render_template(
                    "update_avg_vote.html",
                    values=request.form,
                    min_score = 0,
                    max_score = 10,
                    movie=movie
                )
            avg_vote = request.form.data["avg_vote"]
            db.update_avg_vote(imdb_title_id, avg_vote)
            return redirect(url_for("movie_new", imdb_id = imdb_title_id))

def casting_page(imdb_id):
    db = current_app.config["db"]
    persons = db.get_persons(imdb_id)
    movie = db.get_movie_new(imdb_id)
    return render_template("casting_page.html", imdb_id = imdb_id, movie = movie, persons = persons)

@login_required
def delete_from_casting_page(imdb_title_id, imdb_name_id, ordering):
    if not current_user.is_admin:
        abort(401)
    db = current_app.config["db"]
    db.delete_from_casting(imdb_title_id, imdb_name_id, ordering)
    return redirect(url_for("casting_page", imdb_id = imdb_title_id))

def person_page(imdb_name_id):
    db = current_app.config["db"]
    person = db.get_person(imdb_name_id)
    return render_template("person.html", person = person)

@login_required
def bio_page():
    db = current_app.config["db"]
    
    if request.method == "GET":
        values = {"bio": ""}
        return render_template("bio.html", values = values)
    else:
        valid = validate_bio_form(request.form)
        if not valid:
            return render_template("bio.html", values = request.form)
        
        bio = request.form.data["bio"]
        db.update_bio(current_user.username, bio)
        return(redirect(url_for("profile_page")))

def validate_bio_form(form):
    form.data = {}
    form.errors = {}

    form_bio = form.get("bio")

    if len(form_bio) > 240:
        form.errors["bio"] = "Bio can not be longer than 240 characters."
    else:
        form.data["bio"] = form_bio

    return len(form.errors) == 0

def validate_review_form(form):
    form.data = {}
    form.errors = {}

    form_review = form.get("review_content")

    if len(form_review) > 240:
        form.errors["review_content"] = "Review can not be longer than 240 characters."
    else:
        form.data["review_content"] = form_review

    return len(form.errors) == 0

def validate_movie_form_new(form):
    form.data = {}
    form.errors = {}

    form_title = form.get("title", "").strip()
    #form_director = form.get("director", "").strip()
    if len(form_title) == 0:
        form.errors["title"] = "Title can not be blank."
    else:
        form.data["title"] = form_title
    

    form_avg_vote = form.get("avg_vote")
    if not form_avg_vote:
        form.data["avg_vote"] = 0
    elif (not form_avg_vote.isdigit()) and (re.match(r'^-?\d+(?:\.\d+)$', str(form_avg_vote)) is None):
        form.errors["avg_vote"] = "Average Vote must consist of digits only."
    else:
        avg_vote = float(form_avg_vote)
        if (avg_vote < 0) or (avg_vote > 10):
            form.errors["avg_vote"] = "Average vote not in valid range."
        else:
            form.data["avg_vote"] = avg_vote

    form_year = form.get("year")
    if not form_year:
        form.data["year"] = None
    elif not form_year.isdigit():
        form.errors["year"] = "Year must consist of digits only."
    else:
        year = int(form_year)
        if (year < 1887) or (year > datetime.now().year):
            form.errors["year"] = "Year not in valid range."
        else:
            form.data["year"] = year

    return len(form.errors) == 0


def validate_score_form(form):
    form.data = {}
    form.errors = {}

    form_avg_vote = form.get("avg_vote")
    if not form_avg_vote:
        form.data["avg_vote"] = 0
    elif (not form_avg_vote.isdigit()) and (re.match(r'^-?\d+(?:\.\d+)$', str(form_avg_vote)) is None):
        form.errors["avg_vote"] = "Average Vote must consist of digits only."
    else:
        avg_vote = float(form_avg_vote)
        if (avg_vote < 0) or (avg_vote > 10):
            form.errors["avg_vote"] = "Average vote not in valid range."
        else:
            form.data["avg_vote"] = avg_vote

    return len(form.errors) == 0


def validate_person_form(form):
    form.data = {}
    form.errors = {}

    form_name = form.get("name", "").strip()
    if len(form_name) == 0:
        form.errors["name"] = "Name can not be blank."
    else:
        form.data["name"] = form_name

    
    form_birth_name = form.get("birth_name", "").strip()
    if len(form_name) == 0:
        form.errors["birth_name"] = "Birth name can not be blank."
    else:
        form.data["birth_name"] = form_birth_name
    

    height = form.get("height")
    if not height:
        form.data["height"] = None
    elif not height.isdigit():
        form.errors["height"] = "Height must consist of digits only."
    else:
        height = int(height)
        if (height < 20) or (height > 1000):
            form.errors["height"] = "Height not in valid range."
        else:
            form.data["height"] = height

    return len(form.errors) == 0


def validate_casting_form(form):
    form.data = {}
    form.errors = {}
    db = current_app.config["db"]

    form_movie_id = form.get("movie_id", "").strip()
    if len(form_movie_id) == 0:
        form.errors["movie_id"] = "Movie ID can not be blank."
    else:
        movie = db.get_movie_new(form_movie_id)
        if movie is None:
            form.errors["movie_id"] = "Movie ID does not exist."
        else: 
            form.data["movie_id"] = form_movie_id

    
    form_person_id = form.get("person_id", "").strip()
    if len(form_person_id) == 0:
        form.errors["person_id"] = "Person ID name can not be blank."
    else:
        person = db.get_person(form_person_id)
        if person is None:
            form.errors["person_id"] = "Person ID does not exist."
        else:
            form.data["person_id"] = form_person_id
    

    
    return len(form.errors) == 0


def validate_category_form(form):
    form.data = {}
    form.errors = {}

    form_category = form.get("category", "").strip()
    if len(form_category) == 0:
        form.errors["category"] = "Category can not be blank."
    else:
        form.data["category"] = form_category

    return len(form.errors) == 0




def validate_height_form(form):
    form.data = {}
    form.errors = {}

    height = form.get("height")
    if not height:
        form.data["height"] = None
    elif not height.isdigit():
        form.errors["height"] = "Height must consist of digits only."
    else:
        height = int(height)
        if (height < 20) or (height > 1000):
            form.errors["height"] = "Height not in valid range."
        else:
            form.data["height"] = height

    return len(form.errors) == 0



def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))

def signup_page():
    form = SignupForm()
    db = current_app.config["db"]
    if form.validate_on_submit():
        username = form.data["username"]
        search_user = get_user(username)
        if search_user is not None:
            flash("Username taken.")
        else:
            password = form.data["password"]
            if len(password) < 5:
                flash("Password must be longer than 5 characters.")
            else:
                hashed_password = hasher.hash(password)
                db.insert_user(username, hashed_password)
                user_ = User(username, password, None, None)
                flash("You have signed up and logged in.")
                login_user(user_)
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
    return render_template("signup.html", form=form)


def movies_new_page():
    db = current_app.config["db"]
    if request.method == "GET":
        return render_template("movies_search.html")
    else:
        title = request.form["title"]
        score = request.form["score"]
        lang = request.form["answer"]
        genres = request.form.getlist("genres")

        movies = db.search_movie(title, score, lang, genres)

        return render_template("search.html", movies=movies) 


def search_movies_page(movies):
    return render_template("search.html", movies=movies) 



@login_required
def upload_page():
    db = current_app.config["db"]
    if request.method == "GET":
        return render_template("file_upload.html")
    else:
        uploaded_file = request.files['file']
        extensions = ['.jpg', '.png', '.gif']
        path = 'uploads' 
        if uploaded_file.filename != '':
            filename = uploaded_file.filename
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in extensions:
                abort(400)
            uploaded_file.save(os.path.join(path, uploaded_file.filename))
            username = current_user.username
            db.write_pp(str(username), os.path.join(path, uploaded_file.filename), file_ext)
        return redirect(url_for("profile_page"))






