import os
import requests
from models import *
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

#res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "o817W0fo5miGG9X1d18tzQ", "isbns": "9781632168146"})
#print(res.json())
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
#Session(app)

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

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
            return render_template("books.html", user=user)
    except ValueError:
        return "Login Failed"

@app.route("/search", methods=["POST"])
def search():
    search = request.form.get("book")

    try:
        # Category.query.filter_by(title=Category.title.like("category_param_value %"))
        result = Books.query.filter(or_(Books.title.ilike(f"%{search}%"), Books.isbn.ilike(f"%{search}%"),
        Books.author.ilike(f"%{search}%")))
        return render_template("books.html", result=result)
    except ValueError:
        return "Search Failed"

@app.route("/search/<isbn>", methods=["GET"])
def book(isbn):
    try:
        # Category.query.filter_by(title=Category.title.like("category_param_value %"))
        result = Books.query.filter_by(isbn=isbn).first()
        review = Reviews.query.filter_by(book=9)
        print(result)
        return render_template("details.html", result=result, review=review)
    except ValueError:
        return "Select Failed"

@app.route("/review", methods=["POST"])
def review():
    review = request.form.get("review")
    rating = request.form.get("rating")
    bookId = request.form.get("bookId")

    new_review = Reviews(rating, review, 1, bookId)
    db.session.add(new_review)
    db.session.commit()
    return render_template("books.html")


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
