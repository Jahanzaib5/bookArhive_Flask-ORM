import os
import csv

from flask import Flask, session, render_template, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *

app = Flask(__name__)

# Tell Flask what SQLAlchemy database to use.
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vfooqegoqbccjs:e04d0b9e1addba9715696c93cbfbe566bd3f56fd36fa2b72bf7a9e6272ea876b@ec2-3-223-21-106.compute-1.amazonaws.com:5432/d92pfdtb7oefek"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))


# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")


#signup page
@app.route('/signup')
def signup():
	return render_template('signup.html')

#to add user to the database
@app.route("/add_user", methods=["POST"])
def add_user():
	#get information from the form
	username = request.form.get('username')
	email = request.form.get('email')
	password = request.form.get('password')

	#check if they are not null
	if(username=='' or email=='' or password==''):
		return render_template('error.html', message="Please fill all the details")


	#check if username is already taken
	check = Users.query.filter_by(username=username).count()
	if(check > 0):
		flash("this user name is already taken")
		return render_template('error.html', message="The user name is already taken, kindly choose another")

	#try:
	#	name = str(request.form.get('name'))
	#	email = str(request.form.get('email'))
	#except:
	#	return render_template('error.html', message="please fill in the form to signup!")
	
	#adding user to the database
	user = Users(username=username, email=email, password=password)
	db.session.add(user)
	db.session.commit()
	return render_template("success.html", message="you have been registred, successfully!")
		

#to login the user
@app.route('/sign_in', methods=['POST'])
def sign_in():
	username = request.form.get('username')
	password = request.form.get('password')
	







def main():
# Create tables based on each table definition in `models`
  db.create_all()

def main_2():
	#to import the data from csv file to the database
  f=open('books.csv')
  reader=csv.reader(f)
  count=0
  for isbn, title, author, year in reader:
  	archive = BookArchive(isbn=isbn, title=title, author=author, year=year)
  	db.session.add(archive)
  	count+=1
  	print(count)
  	db.session.commit()




if __name__ == "__main__":
  # Allows for command line interaction with Flask application
  with app.app_context():
    main()
    #main_2()