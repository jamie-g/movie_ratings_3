db = None

class User(object):
    def __init__(self, age, occupation, gender):
        self.age = age
        self.occupation = occupation
        self.gender = gender

    @staticmethod
    def get(user_id):
        user = db.users.find_one({"_id": user_id})
        return User(user['age'], user['occupation'],
                user['gender'])

    def __str__(self):
        return "%s %s, age %d"%(self.gender,
                self.occupation, self.age)

class Movie(object):
    def __init__(self, title, genres):
        self.title = title
        self.genres = genres

    @staticmethod
    def get(movie_id):
        movie = db.movies.find_one({"_id": movie_id})
        return Movie(movie['title'], movie['genres'])

    def __str__(self):
        return "%s, %s"%(self.title, ', '.join(self.genres))

class Rating(object):
    def __init__(self, rating):
        self.rating = rating

    # def movie_list():
    # # list of movie ids

    # def user_ratings():
    #     #list of dictionaries user:rating
    # [ {toy story: {user:rating, user: rating, user:rating}]

    # @staticmethod
    # def rating_dict():
        # # new_dict = {}
        # ratings = db.ratings
        # print ratings
        # for i  in ratings:
        #     new_dict.get(i[movie_id], {i[user_id]:rating})
        # print new_dict

    @staticmethod
    def get(movie_id, user_id):
        # rating db is a list of dictionaries
        rating_result =  db.ratings.find_one({"user_id": user_id, "movie_id": movie_id})
        print rating_result, '*'*10
        return Rating(rating_result['rating'])

    def __str__(self):
        return "%s, "%self.rating