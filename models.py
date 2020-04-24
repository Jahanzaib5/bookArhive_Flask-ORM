from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#creating the class for each database tables using ORM
class Users(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)


class BookArchive(db.Model):
	__tablename__="bookarchive"
	id = db.Column(db.Integer, primary_key=True)
	isbn = db.Column(db.Integer,unique=True, nullable=False)
	title = db.Column(db.String, nullable=False)
	author = db.Column(db.String, nullable=False)
	same_isbn = db.relationship('BookArchive', backref='bookreview', lazy=True)

class BookReview(db.Model):
	__tablename__="bookreview"
	id = db.Column(db.Integer, primary_key=True)
	rating = db.Column(db.Integer, nullable=True)
	review_isbn = db.Column(db.Integer, db.ForeignKey("bookarchive.isbn"), nullable=False)
