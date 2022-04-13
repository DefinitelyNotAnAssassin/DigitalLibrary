import flask
from flask import * 
import sqlite3
import os
from sqlalchemy import and_, or_
from flask_sqlalchemy import SQLAlchemy
import uuid
import flask_bcrypt
app = Flask(__name__)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["FILE_UPLOAD"] = f"{os.getcwd()}/files/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.sqlite3"
app.config["SQLALCHEMY_BINDS"] = {
    'admin':        'sqlite:///admin.sqlite3',
    'libraryfiles':      'sqlite:///library.sqlite3'
}

db = SQLAlchemy(app)


class libraryfiles(db.Model):
  __bind_key__ = "libraryfiles"
  _id = db.Column("id", db.Integer, primary_key = True)
  bookname = db.Column("bookname", db.String(100))
  filename = db.Column("filename", db.String(255))
  author = db.Column("author", db.String(75))
  category = db.Column("category", db.String(75))
  def __init__(self, bookname, filename, author, category):
    self.bookname = bookname
    self.filename = filename
    self.author = author
    self.category = category
    
class messages(db.Model):
  __bind_key__ = "libraryfiles"
  _id = db.Column("id", db.Integer, primary_key= True)
  bookname = db.Column("bookname", db.String(100))
  content = db.Column("content", db.String(1000))
  date = db.Column("date", db.String(100))
  sender = db.Column("sender", db.String(100))
  rating = db.Column("rating", db.String(25))

  def __init__(self, bookname, content, date, sender, rating):
    self.bookname = bookname
    self.content = content
    self.date = date
    self.sender = sender
    self.rating = rating
class user(db.Model):
  __bind_key__ = "admin"
  _id = db.Column("id", db.Integer, primary_key = True)
  username = db.Column("username", db.String(100))
  password =db.Column("password", db.String(255))
class access(db.Model):
  _id = db.Column("id", db.Integer, primary_key = True)
  key = db.Column("key",db.String(100))
  



def verification(filename):
  __bind_key__ = "admin"
  decision = input(f"A user is trying to upload {filename} Accept(Y) or Reject(N) : ")
  return decision 

@app.route("/")
def add_content():
  return render_template("add_content.html")

@app.route("/admin/upload", methods = ["POST"])
def upload():
  booktitle = request.form["Bookname"]
  file_name = request.form["Filename"].replace(" ", "-")
  category = request.form["Category"]
  author = request.form["Author"]
  addFile = libraryfiles(booktitle, file_name, author, category)
  decision = verification(file_name)
  
  if decision.lower() == "y":
    db.session.add(addFile)
    db.session.commit()
    print(request.files)
    file = request.files["File"]
    file.save(os.path.join(app.config["FILE_UPLOAD"], file.filename.replace(" ", "-")))
    return redirect(url_for("add_content"))
  elif decision.lower() == "n":
    return "<h1>File Upload Request Rejected</h1>"


@app.route("/register")
def register():
  return render_template("register.html")


  
if __name__ == "__main__":
  app.run(debug = True)
  #db.create_all(bind = ['admin'])