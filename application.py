import os
import requests
from models import *
from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'key'

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name")
    password = request.form.get("password")

    try:
        user = Users.query.filter_by(username=name).first()
        if user is not None and password == user.password:
            session['user_id'] = user.id
            return render_template("books.html", user=user)
    except ValueError:
        return "Login Failed"

@app.route("/logout")
def logout():
    user = session.get('user_id')

    if user:
        session.pop('user_id')
        return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    search = request.form.get("book")

    try:
        result = Books.query.filter(or_(Books.title.ilike(f"%{search}%"), Books.isbn.ilike(f"%{search}%"),
        Books.author.ilike(f"%{search}%")))
        return render_template("books.html", result=result)
    except ValueError:
        return "Search Failed"

@app.route("/search/<isbn>", methods=["GET"])
def book(isbn):
    x = isbn
    print("isbn: " + x)
    list = [isbn]
    api = requests.get("https://www.goodreads.com/book/review_counts.json",
    params={"key": "B30LyGpK2OdNTH7HQlEpA", "isbns": list})

    json = api.json()
    average_rating = json['books'][0]['average_rating']
    ratings_count = json['books'][0]['ratings_count']
    print(json)
    print("??????????????????????????????????????")
    try:
        result = Books.query.filter_by(isbn=isbn).first()
        review = Reviews.query.filter_by(book=result.id)
        print("FUCK SHIT" + isbn)

        return render_template("details.html", result=result, review=review, average_rating=average_rating, ratings_count=ratings_count)
    except ValueError:
        return "Select Failed"

@app.route("/review", methods=["POST"])
def review():
    bookId = request.form.get("bookId")
    can_review = Reviews.query.filter_by(user=1, book=bookId).first()
    print(can_review)

    if not can_review:
        user = session.get('user_id')
        review = request.form.get("review")
        rating = request.form.get("rating")

        new_review = Reviews(rating, review, user, bookId)
        db.session.add(new_review)
        db.session.commit()
        return render_template("books.html")
    else:
        return "User already submitted review"


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    password = request.form.get("password")

    if name is not None and password is not None:
        new_user = Users(name, password)
        db.session.add(new_user)
        db.session.commit()
        #return "Register successful"
        return  name + " " + password
    return "Invalid Credentials"

if __name__ == "__main__":
    with app.app_context():
        main()
