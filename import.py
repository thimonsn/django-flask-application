import os
import csv
from flask import Flask, session
from models import *

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def dbimport():
    file = open("books.csv")
    reader = csv.reader(file)

    for isbn,title,author,year in reader:
        book = Books(isbn, title, author, year)
        db.session.add(book)
        print(book.title)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        dbimport()
