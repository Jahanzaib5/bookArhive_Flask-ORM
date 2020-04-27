from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#creating the class for each database tables using ORM
class Users(UserMixin, db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)

  def set_password(self, password ):
  	'''create hash password for the user'''
  	self.password = generate_password_hash(password, method='sha256')


  def check_password(self, password):
  	'''unhash the hashed password and checks it---returns bool value'''
  	return check_password_hash(self.password, password)

  def get_user_id(self):
    return self.id


  def __repr__(self):
  	return 'Welcome {}!'.format(self.username)




class BookReview(db.Model):
	__tablename__="bookreview"
	id=db.Column(db.Integer, primary_key=True)
	rating = db.Column(db.Integer, nullable=True)
	review_isbn = db.Column(db.String, db.ForeignKey("bookarchive.isbn"), nullable=False)



class BookArchive(db.Model):
	__tablename__="bookarchive"
	id = db.Column(db.Integer, primary_key=True)
	isbn = db.Column(db.String, unique=True, nullable=False)
	title = db.Column(db.String, nullable=False)
	author = db.Column(db.String, nullable=False)
	year = db.Column(db.Text, nullable=False)

