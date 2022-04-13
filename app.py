from flask import * 
import sqlite3
import os
from sqlalchemy import and_, or_
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
import time
from flask_caching import Cache


app = Flask(__name__)
app.config["CACHE_TYPE"] = "simple"
cache = Cache(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///library.sqlite3'

app.config["FILE_UPLOAD"] = f"{os.getcwd()}/files/"

app.secret_key = "ThisIsSupposedToBeSecured"
app.permanent_session_lifetime = timedelta(minutes=60)


db = SQLAlchemy(app)


class libraryfiles(db.Model):
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


booktitles = libraryfiles.query.all()
titulo = []
for i in booktitles:
  titulo.append(i.bookname)

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)
           
@app.route("/")
@cache.cached(timeout=1800)
def index():
  return render_template("index.html", autosuggest = booktitles)





@app.route("/search", methods = ["GET", "POST"])
def search():
  if request.method == "GET":
    return redirect(url_for("index"))
  elif request.method == "POST":
    search = f"%{request.form['search']}%"
    category = f"{request.form['category']}" 
    
    file = libraryfiles.query.filter(and_(libraryfiles.bookname.like(search),libraryfiles.category == category)).all()
    rating = messages.query.filter(messages.bookname.like(search)).all()
    autosuggest = libraryfiles.query.all()
    return render_template("accordion_result.html", search = search, file = file, rating = rating, autosuggest = booktitles)
  
@app.route("/download/<path:path>")
def download(path):
  try:
    return send_from_directory(app.config["FILE_UPLOAD"], path=path, as_attachment = True)
  except FileNotFoundError:
    abort(404)

@app.route("/view/<path:path>")
def view(path):
  return render_template("view.html", filename = f"{path}")


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
  currentdate = date.today()
  addMsg = messages(bookname, comment, currentdate.strftime("%m/%d/%Y"), sender, rating)
  db.session.add(addMsg)
  db.session.commit()
  return redirect(url_for('index'))
  
  
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


if __name__ == "__main__":
  app.run(debug = True)
  db.create_all()
