#!/usr/bin/env python

import sys
from correlation import pearson_similarity as pearson
import pymongo
from collections import defaultdict
import traceback
import model
from model import User
from model import Movie
from model import Rating 

global db

def movie_details(movie_id):
    movie = get_movie(movie_id)

    if not movie:
        print "No movie with id %d"%movie_id

    print movie
    

def error(msg = "Unknown command"):
    print "Error:", msg

def quit():
    print "Goodbye!"
    sys.exit(0)

def average_rating(movie_id):
    movie = Movie.get(movie_id)
    avg = movie.get_average()
    print "%.1f stars"%(avg)
    # rating_records = get_ratings(movie_id=movie_id)
    # ratings = [ rec['rating'] for rec in rating_records ]
    # avg = float(sum(ratings))/len(ratings)

    # print "%.2f"%(avg)

def user_details(user_id):
    user = User.get(user_id)
    print user

def user_rating(movie_id, user_id):
    rating = get_rating(movie_id, user_id)
    if not rating:
        print "Sorry, user %d has not rated movie %d"%(user_id, movie_id)
        return
    movie = get_movie(movie_id)
    print "User %d rated movie %d (%s) at %d stars"%(\
            user_id, movie_id, movie.title,
            rating)

def rate_movie(movie_id, value):
    movie = get_movie(movie_id)
    # rating = Rating(movie_id, value, 0)
    # print rating, '$'*10
    # print get_rating(movie_id, 0)
    update = Rating.update_rating(movie_id, value)

    # db.ratings.update({"movie_id": movie_id, "user_id": 0},
    #         {"$set": {"rating": rating}}, upsert=True)
    print "You rated movie %d: %s at %d stars."%(\
            movie_id, movie.title,
            value)

def get_movie(movie_id):
    return Movie.get(movie_id)

def get_ratings(movie_id=None, user_id=None):
    movie = get_movie(movie_id)
    records = Movie.ratings(movie) 
    query = {}
    if movie_id is not None:
        query['movie_id'] = movie_id
    if user_id is not None:
        query['user_id'] = user_id

    return [ rec for rec in records ]

    # records = #find either movie ratings or list of user ratings

    # query = {}

    # if movie_id is not None:
    #     query['movie_id'] = movie_id
    # if user_id is not None:
    #     query['user_id'] = user_id

    # records = Movie.ratings(query)
    # print records
    # return [ rec for rec in records ]

def get_rating(movie_id, user_id):
    record = Rating.get(movie_id, user_id)
    if record:
        return record

def predict(movie_id):
    target_movie_id = get_movie(movie_id)
    ratings = get_ratings(movie_id=movie_id)

    for movie in rated_movies:
        similarities = [ (pearson({}, {}), rating) for target_movie_id, rating in movie_pairs]
        top_five = sorted(similarities)
        top_five.reverse()
        top_five = top_five[:5]
        num = 0.0
        den = 0.0
    # Use a weighted mean rather than a strict top similarity
    for sim, m in top_five:
        num += (float(sim) * m)
        den += sim

    rating = num/den
    print "Best guess for movie %d: %s is %.2f stars"%\
            (movie_id, target_movie['title'], rating)


def parse(line, dispatch):
    tokens = line.split()
    if not tokens:
        return error()

    cmd = tokens[0]
    command = dispatch.get(cmd)

    if not command:
        return error()
     
    if len(tokens) != len(command):
        return error("Invalid number of arguments")

    function = command[0]

    if len(command) == 1:
        return function()

    try:
        type_tuples = zip(command[1:], tokens[1:])
        typed_arguments = [ _type(arg) for _type, arg in type_tuples ]
        return function(*typed_arguments)

    except Exception, e:
        traceback.print_exc()
        return error("Invalid argument to %s"%(cmd))

def connect_db(host, port, user, password, db_name):
    connect_string = "mongodb://%s:%s@%s:%d/%s" % \
            (user, password, host, port, db_name)

    c = pymongo.connection.Connection(connect_string)
    return c[db_name]

def main():
    connect()
    #db = pymongo.connection.Connection("localhost")

    dispatch = {
            "movie": (movie_details, int),
            "q": (quit,),
            "avg": (average_rating, int),
            "user": (user_details, int),
            "rating": (user_rating, int, int),
            "rate": (rate_movie, int, int),
            "predict": (predict, int)
            }

    while True:
        line = raw_input("> ")
        parse(line, dispatch)
   
def connect():
    global db
    db = connect_db("dbh36.mongolab.com", 27367, "movie_user", "password", "movies")
    db = db['movies']
    model.db = db
    return db

if __name__ == "__main__":
    main()
