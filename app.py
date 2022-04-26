from flask import * 
import sqlite3
import os
from sqlalchemy import and_, or_
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
import time
from flask_caching import Cache
from flask_talisman import Talisman
import uuid
from form import SearchForm

app = Flask(__name__)

app.config["CACHE_TYPE"] = "simple"
cache = Cache(app)
#talisman = Talisman(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///library.sqlite3'

app.config["FILE_UPLOAD"] = f"{os.getcwd()}/files/"

app.secret_key = "ThisIsSupposedToBeSecured"
app.permanent_session_lifetime = timedelta(minutes=60)
secretKey = "012:09#910@81!0;73!1{}*9$0384/?31"



db = SQLAlchemy(app)
class libraryfiles(db.Model):
  _id = db.Column("id", db.Integer, primary_key = True)
  bookname = db.Column("bookname", db.String(255))
  filename = db.Column("filename", db.String(255))
  author = db.Column("author", db.String(255))
  category = db.Column("category", db.String(75))
  def __init__(self, bookname, filename, author, category):
    self.bookname = bookname
    self.filename = filename
    self.author = author
    self.category = category
class messages(db.Model):
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
class accesscode(db.Model):
  _id = db.Column("id", db.Integer, primary_key = True)
  accesskey = db.Column("accesskey", db.String)
  
  def __init__(self, accesskey):
    self.accesskey = accesskey
  
def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)
           
@app.route("/")
def index():
    form = SearchForm()
    return render_template("index.html", form = form)

@app.route("/search", methods = ["GET", "POST"])
def search():
  if request.method == "GET":
    return redirect(url_for("index"))
  
  elif request.method == "POST":
    search = f"%{request.form['Title']}%"
    category = f"{request.form['Category']}"
    result = libraryfiles.query.filter(and_(libraryfiles.bookname.like(search), libraryfiles.category == category)).all()
    print(result)
    return render_template("accordion_result.html", file = result)
  

@app.route("/download/<path:path>")
def download(path):
  try:
    return send_from_directory(app.config["FILE_UPLOAD"], path=path, as_attachment = True)
  except FileNotFoundError:
    abort(404)

@app.route("/view")
def view():
  return render_template("view.html")

@app.route("/feedback/<bookname>")
def feedback(bookname):
  if bookname in titulo:
    comment = messages.query.filter(messages.bookname == bookname).all()
    return render_template("review.html", bookname = bookname, comment = comment)
  elif bookname not in titulo:
    abort(404)


@app.route("/addfeedback", methods = ["POST"])
def addfeedback():
  sender = request.form["username"]
  comment = request.form["feedback"]
  rating = request.form["rate"]
  bookname = request.form["bookname"]
  ratings = ["1", "2", "3", "4", "5"]
  if rating in ratings:
    currentdate = date.today()
    addMsg = messages(bookname, comment, currentdate.strftime("%m/%d/%Y"), sender, rating)
    db.session.add(addMsg)
    db.session.commit()
    return redirect(url_for('index'))
  elif rating not in ratings:
    return "Rating Rejected"
  
@app.route("/addreadlist/<bookname>")
def addreadlist(bookname):
  if "read_later" not in session:
    session["read_later"] = []
  
  if bookname not in titulo:
    return redirect(redirect_url())
  elif bookname in titulo and bookname not in session["read_later"]:
    a = session["read_later"]
    a.append(bookname)
    session["read_later"] = a
    print(f"{bookname} Added to the session")
    
    return redirect(redirect_url())
  else:
    return redirect(redirect_url())
  
@app.route("/readlist")
def readlist():
  if "read_later" in session:
   return render_template("readlist.html", bookname = session["read_later"], file = booktitles)
  elif "read_later" not in session:
    return redirect(redirect_url())




@app.route("/faq")
@cache.cached(timeout = 0)
def faq():
  return render_template("faq.html")


    
    
@app.route("/get_title", methods = ["POST"])
def send_title():
  data = request.get_json()
  print(data)
  result = libraryfiles.query.with_entities(libraryfiles.bookname, libraryfiles.category).filter(libraryfiles.category == data["category"]).all()
  dictor = dict(result)

  return dictor
if __name__ == "__main__":
  app.run(debug = True)
  
