from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
      _tablename_ = "users"
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String, nullable = False)
      password = db.Column(db.String, nullable = False)

class Books(db.Model):
      _tablename_ = "books"
      id = db.Column(db.Integer, primary_key=True)
      isbn = db.Column(db.String, nullable = False)
      title = db.Column(db.String, nullable = False)
      author = db.Column(db.String, nullable = False)
      year = db.Column(db.Integer, nullable = False)
      reviews = db.Column(db.Integer,db.ForeignKey("reviews.id"), nullable = False)

class Reviews(db.Model):
      _tablename_ = "reviews"
      id = db.Column(db.Integer, primary_key=True)
      rating = db.Column(db.Integer, nullable = False)
      review = db.Column(db.String, nullable = False)
      user = db.Column(db.Integer,db.ForeignKey("users.id"), nullable = False)
