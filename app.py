import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *

app = Flask(__name__)

# Tell Flask what SQLAlchemy databas to use.
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


@app.route("/")
def index():
    return render_template("index.html")
#the signup page
@app.route("/signup")
def signup():
	return render_template("signup.html")


# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)

def main():
  # Create tables based on each table definition in `models`
  db.create_all()

if __name__ == "__main__":
  # Allows for command line interaction with Flask application
  with app.app_context():
    main()