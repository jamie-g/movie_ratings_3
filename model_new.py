db = None

class User(object):
    def __init__(self, age, occupation, gender):
        self.age = age
        self.occupation = occupation
        self.gender = gender

    @staticmethod
    def get(user_id):
        user = db.users.find_one({"_id": user_id})
        return User(user['age'], user['occupation'].capitalize(),
                user['gender'])

    def __str__(self):
        return "%s %s, age %d"%(self.gender,
                self.occupation, self.age)

class Movie(object):
    def __init__(self, id, title, genres):
        self.id = id
        self.title = title
        self.genres = genres


    def ratings(self):
        """In memory, ratings dictionary looks like this:
        {"_id": ..., "movie_id": x, "user_id": y, "rating": z }

        Returns:  list of rating objects [ Rating(), Rating(), Rating() ]
        """
        ratings_records = db.ratings.find({"movie_id": self.id})
        rating_objs = []
        for record in ratings_records:
            r = Rating(record["rating"], self.id, record["user_id"])
            rating_objs.append(r)

        return rating_objs

    
    def get_average(self):
        """[ Rating(), Rating() ]"""
        rating_list = self.ratings()
        rating_values = []
        for rating in rating_list:
            rating_values.append(rating.value)

        numerator = sum(rating_values)
        denominator = len(rating_list)

        return float(numerator)/denominator

    @staticmethod
    def get(movie_id):
        """
        {"_id": xxxx, "title": x, ...}
        """
        movie = db.movies.find_one({"_id": movie_id})

        return Movie(movie['_id'], movie['title'], movie['genres'])

    def __str__(self):
        return "%s, %s, %s"%(self.id, self.title, ', '.join(self.genres))

class Rating(object):
    def __init__(self, value, movie_id, user_id):
        self.value = value
        self.movie_id = movie_id
        self.user_id = user_id

    @staticmethod
    def get(movie_id, user_id):
        # rating db is a list of dictionaries
        rating_result = db.ratings.find_one({"user_id": user_id, "movie_id": movie_id})
        return rating_result['rating']

    def __str__(self):
        return "<Rating movie_id:%d, user_id:%d, value: %d>"%(self.movie_id, self.user_id, self.value)