import os
import requests
from models import *
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
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
    return "Hi"

if __name__ == "__main__":
    with app.app_context():
        main()
