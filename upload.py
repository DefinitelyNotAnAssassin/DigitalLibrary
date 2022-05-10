import flask
from flask import * 
import sqlite3
import os
from sqlalchemy import and_, or_,desc
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_bcrypt import Bcrypt
from flask_session import Session
from datetime import timedelta
from form import CourseForm

app = Flask(__name__)
app.secret_key = "ThisIsSupposedToBeSecured"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.permanent_session_lifetime=timedelta(minutes=60)
Session(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["FILE_UPLOAD"] = f"{os.getcwd()}/files/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.sqlite3"
app.config["SQLALCHEMY_BINDS"] = {
    'admin':        'sqlite:///admin.sqlite3',
    'libraryfiles':      'sqlite:///library.sqlite3'
}

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
secretKey = "012:09#910@81!0;73!1{}*9$0384/?31"


class Category(db.Model):
  __bind_key__ = "libraryfiles"
  _id = db.Column("id", db.Integer, primary_key = True)
  book_category = db.Column("book_category", db.String)
  booklist = db.relationship('Books', backref = "book_category")
  def __init__(self, book_category):
    self.book_category = book_category



class Books(db.Model):
  __bind_key__ = "libraryfiles"
  _id = db.Column("id", db.Integer, primary_key = True)
  bookname = db.Column("bookname", db.String)
  filename = db.Column("filename", db.String)
  category = db.Column(db.Integer, db.ForeignKey('category.book_category'))
  def __init__(self, bookname,filename):
    self.bookname = bookname
    self.filename = filename


class user(db.Model):
  __bind_key__ = "admin"
  _id = db.Column("id", db.Integer, primary_key = True)
  username = db.Column("username", db.String(100))
  password =db.Column("password", db.String(255))
  
  def __init__(self, username, password):
    self.username = username
    self.password = password
class access(db.Model):
  __bind_key__ = "admin"
  _id = db.Column("id", db.Integer, primary_key = True)
  key = db.Column("key",db.String(100))
  
  def __init__(self, key):
    self.key = key

def verification(filename):
  decision = input(f"A user is trying to upload {filename} Accept(Y) or Reject(N) : ")
  
  return decision 

@app.route("/add_content")
def add_content():
  if "is_logged" in session:
    return render_template("add_content.html")
  elif "is_logged" not in session:
    return redirect(url_for('login'))



@app.route("/test", methods = ["GET", "POST"])
def testing():
  form = CourseForm()
  return render_template("test.html", form=form, uuid = f"{uuid.uuid4()}")
    
    
@app.route("/send", methods = ["POST"])
def send():
  form = CourseForm()
  if form.validate_on_submit():
    addBook = Books(form.Bookname.data, f"{form.Filename.data}.pdf")
    decision = verification(form.Bookname.data)
    if decision.lower() == "y":
      db.session.add(addBook)
      ctgry = Category.query.filter(Category.book_category == form.Category.data).first()
      ctgry.booklist.append(addBook)
      db.session.commit()
      file = form.File.data
      file.save(os.path.join(app.config["FILE_UPLOAD"], f"{form.Filename.data}.pdf"))
      return "Uploaded!"
    elif decision.lower() == "n":
      return "Upload Denied"
    return "hello"
  

  return "!!!"
    
@app.route("/register")
def register():
  return render_template("register.html")

@app.route("/register_user", methods = ["POST"])
def register_user():
  username = request.form["username"]
  encryptedpass = bcrypt.generate_password_hash(request.form["password"])
  addUser = user(username, encryptedpass)
  db.session.add(addUser)
  db.session.commit()
  print(encryptedpass)
  return redirect(url_for("login"))
  
@app.route("/")
def login():
  if "is_logged" in session:
    return redirect(url_for("add_content"))
  elif "is_logged" not in session:
    return render_template("login.html")
  
@app.route("/verify_login", methods = ["POST"])
def verify_login():
  username = request.form["username"]
  key = request.form["key"]
  data = user.query.filter(user.username == username).first()
  if data:
    checkpass = bcrypt.check_password_hash(data.password, request.form["password"])
    if checkpass:
      accesskey = access.query.order_by(access._id.desc()).first()
      if accesskey.key == key:
        db.session.delete(accesskey)
        db.session.commit()
        session["is_logged"] = True
        return redirect(url_for("add_content"))
      elif accesskey.key != key:
        return "INVALID ACCESS KEY"
    elif not checkpass:
      return "INVALID USERNAME PASSWORD"
    
    
    
  elif not data:
    return "INVALID USERNAME PASSWORD"
  
  keys = access.query.order_by(access._id.desc()).first()
  
  
@app.route("/generate_key", methods = ["POST"])
def generate_key():
  if request.get_json():
    data = request.get_json()
    accesskey = uuid.uuid4()
    addkey = access(f"{accesskey}")
    print(f"The access key is: {accesskey}")
    db.session.add(addkey)
    db.session.commit()
    return "Hey"

@app.route("/check_valid")
def check_valid():
  form = CourseForm()
  if form.validate():
    data = True
  else:
    data = False
  return {"data": data}

@app.route("/playground")
def playground():
  
  return "hi"
if __name__ == "__main__":
  app.run(debug = True)
  db.create_all(bind = ['libraryfiles'])