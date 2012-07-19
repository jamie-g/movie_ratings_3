import pymongo
from collections import defaultdict

class Ratings(object):
	#movie list
	#user_id and ratings[{}]
	#ratings is a list of dictionaries
	def rating_dict():
		new_dict = {}
		ratings = db.ratings 
		for i  in ratings:
			new_dict.get(i[movie_id], {i[user_id]:rating})
		print new_dict


def main():
	global db
	db = movies.connect_db("dbh36.mongolab.com", 27367, "movie_user", "password", "movies")
	rating_dict()

if __name__ == "__main__":
    main()



