class Person:
    def __init__(self, imdb_name_id, name, birth_name, height, bio, date_of_birth, place_of_birth, date_of_death, place_of_death):
        self.imdb_name_id = imdb_name_id
        self.name = name
        self.birth_name = birth_name
        self.height = height
        self.bio = bio
        self.date_of_birth = date_of_birth
        self.place_of_birth = place_of_birth
        self.date_of_death = date_of_death
        self.place_of_death = place_of_death


class PersonShort:
    def __init__(self, imdb_name_id, name, category, character):
        self.imdb_name_id = imdb_name_id
        self.name = name
        self.category = category
        self.character = character