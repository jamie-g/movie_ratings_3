import flask
from flask import Flask, url_for, render_template, request, g
import model
from model import Movie
from model import User
from model import Rating
import movies

app = Flask(__name__)

@app.before_request
def before_request():
	g.db = movies.connect()

@app.route("/")
def home():

	return render_template("movie_web.html")

@app.route("/movie", methods=["POST"])
def movie_details():
	movie_id = request.form['movie_id']
	movie = Movie.get(int(movie_id))
	return render_template("movie_details.html", movie=movie)

@app.route("/user", methods=["POST"])
def user_details():
	user_id = request.form['user_id']
	user = User.get(int(user_id))
	return render_template("user_details.html", user=user)

@app.route("/rating", methods=["POST"])
def average_rating():
	movie_id = request.form['movie_id']
	average = Movie.get_average(str(movie_id))
	return render_template("average_rating.html", average=average)
	pass


if __name__ == '__main__':
    app.run(debug=True)
