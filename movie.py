class Movie:
    def __init__(self, title, year=None):
        self.title = title
        self.year = year
    

class MovieNew:
    def __init__(self, imdb_title_id, original_title, year, date_published, genre, duration, country, language, director, actors, description, avg_vote, votes):
        self.imdb_title_id = imdb_title_id
        self.original_title = original_title
        self.year = year
        self.date_published = date_published
        self.genre = genre
        self.duration = duration
        self.country = country
        self.language = language
        self.director = director
        self.actors = actors
        self.description = description
        self.avg_vote = avg_vote
        self.votes = votes


class MovieShort:
    def __init__(self, imdb_title_id, original_title, year, director):
        self.imdb_title_id = imdb_title_id
        self.original_title = original_title
        self.year = year
        self.director = director