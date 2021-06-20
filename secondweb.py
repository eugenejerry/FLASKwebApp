#importing neccessary modules or libraries to connect python flask to database
from enum import unique
from flask import Flask
import os
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
#create an instance of flask
secondweb = Flask(__name__)

#This finds the current location of your python file (flask python app).It works on all Operating systems (os).
project_dir = os.path.dirname(os.path.abspath(__file__))

#This creates a database file (.db file) in the above found directory or path
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

#connecting the database file (bookdatabase.db) to the sqlalchemy dependency.
secondweb.config["SQLALCHEMY_DATABASE_URI"] = database_file

# connecting this secondweb.py file to the sqlalchemy
db = SQLAlchemy(secondweb)
@secondweb.before_first_request
def create_table():
    db.create_all()


# creating a model for the book table
class Book(db.Model):
    title = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(80), unique = True, nullable = False, primary_key = True)
    address = db.Column(db.String(80), unique = True, nullable = False)
    # message = db.Column(db.String(80), unique = True, nullable = False)
    def __repr__(self):
        return "<Title: {}>".format(self.title), "<Email: {}>".format(self.email), "<Address: {}>".format(self.address)
    
    
#create a route decorator
@secondweb.route("/", methods=["GET", "POST"])
def home():
# validating the content of the form. This condition shall be false if the request.form list is empty
    if request.form:
        title_from_form = request.form.get("title") # assigns the content of the title field to the variable
        email_from_form = request.form.get("email") # assigns the content of the email field to the variable
        address_from_form = request.form.get("address") # assigns the content of the address field to the variable

                
        book = Book(title=title_from_form, email=email_from_form, address=address_from_form) # instance of the Book class. assigned to the 'book' variable
        
        db.session.add(book) # adds the data to the session
        db.session.commit() # this commits the data to the database
    books = Book.query.all() # this retrieves all the contents of the book table.
    return render_template("home.html", books = books) # rendering the html page alongside the queried books to the browser.


#create a route decorator#
# @secondweb.route("/", methods=["GET", "POST"])
# def home():
#     #print(project_dir)
#     if request.form:
#         print(request.form)
#         print(request.form.get("title"))
#         #print("i have something")
#     return render_template("home.html")


# @secondweb.route ("/bootstore")
# def bookstore():
#     return render_template("home.html")

