import os
import csv

from flask import Flask, session, render_template, request, flash, redirect, url_for, g
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import login_required, logout_user, current_user, login_user ,LoginManager, UserMixin


from models import *

app = Flask(__name__)
app.secret_key = "MynameiskhanandIamnotaterrorist"

#login_manager = LoginManager()

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


login_manager = LoginManager()
login_manager.init_app(app)


#to return the user object with just the user_id for the purpose of logging in
@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))


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
		return render_template('error.html', message="Please fill in all the details")


	#check if username is already taken
	check = Users.query.filter_by(username=username).count()
	if(check > 0):
		flash("this user name is already taken")
		return render_template('error.html', message="The user name is already taken, kindly choose another")


	#check if the email is already taken
	check_email = Users.query.filter_by(email=email).first()
	if check_email is None:
		#adding user to the database
		user = Users(username=username, email=email, password=password)
		user.set_password(password)#to create hash password
		db.session.add(user)
		db.session.commit()
		#login_user(user) #login as newly create user
		return render_template("success.html", message="you have been registred, successfully!")
	else:
		return render_template('error.html', message="This email is already registered!")
			


#to login the user
@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
	#if current_user.is_authenticated:
	#	return render_template('dashboard.html', message='You are already logged in!')

	#creating empty list to store the user for the session
	#if session.get('username') == None:
	#	session['username']=[]

	#checkin the credentials and logging the user in
	if request.method == "POST":

		session.pop('user_id', None)

		username = request.form.get('username')
		password = request.form.get('password')

		#session['username'].append(username)

		if (username=='' or password=='') == False:
			user = Users.query.filter_by(username=username).first() #cehck if user exist in the database
			if (user):
				passw = user.check_password(password)#method we build to check the password and return bool
				if (passw):
					login_user(user)
					session['user'] = user
					return render_template('dashboard.html', message=user.__repr__())
					#return redirect(url_for('dashboard'))
		return render_template('error.html', message="Invalid login details")
	else:
		if 'user' in session:
			return render_template("dashboard.html")
		return render_template('error.html', message="Please fill in the details")
	return render_template('error.html', message="Please fill in the details")


@app.route('/dashboard')
@login_required
def dashboard():
	if 'user' in session:
		user = session['user']
		return render_template("dashboard.html", message=user.__repr__())
	else:
		return render_template('error.html', message="Login failed")



@app.route('/logout')
@login_required
def logout():
	logout_user()
	session.pop('user ', None)
	return redirect(url_for('index'))




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
    #main()
    main_2()