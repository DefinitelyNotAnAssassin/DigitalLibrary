from flask import * 
import sqlite3
import os
from sqlalchemy import and_, or_, inspect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
import time
from flask_caching import Cache
from flask_talisman import Talisman
import uuid
from form import SearchForm
import random
import json
import time
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

class Category(db.Model):
  _id = db.Column("id", db.Integer, primary_key = True)
  book_category = db.Column("book_category", db.String)
  booklist = db.relationship('Books',lazy='dynamic', backref=db.backref('book_category', lazy='joined'))
  def __init__(self, book_category):
    self.book_category = book_category
    
class Books(db.Model):
  _id = db.Column("id", db.Integer, primary_key = True)
  bookname = db.Column("bookname", db.String)
  filename = db.Column("filename", db.String)
  category = db.Column(db.Integer, db.ForeignKey('category.book_category'))
  def __init__(self, bookname,filename):
    self.bookname = bookname
    self.filename = filename

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
    result = Category.query.filter(Category.book_category == category).first()
    
    return render_template("accordion_result.html", file = result.booklist.filter(Books.bookname.like(search)).limit(15))
  

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
  comment = messages.query.filter(messages.bookname == bookname).all()
  return render_template("review.html", bookname = bookname, comment = comment)
  


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
  a = session["read_later"]
  a.append(bookname)
  session["read_later"] = a
  print(f"{bookname} Added to the session")
    
  return redirect(redirect_url())
  
@app.route("/readlist")
def readlist():
  if "read_later" in session:
    data = Books.query.filter(Books.bookname.in_(session["read_later"])).all()
    return render_template("readlist.html", data = data)
   
  elif "read_later" not in session:
    return redirect(redirect_url())




@app.route("/faq")
@cache.cached(timeout = 0)
def faq():
  return render_template("faq.html")


    
    
@app.route("/get_title", methods = ["POST"])
def send_title():
  start = time.time()
  data = request.get_json()
  qry = Category.query.filter(Category.book_category == data['category']).first()
  qry = [(i.bookname) for i in qry.booklist.filter(Books.bookname.like(data["search"])).limit(10)]
  end = time.time()
  print(f"Transaction done: {end-start} s")
  
  return json.dumps(qry)
  
  
  
@app.route("/test")
def test():
  #for i in range(100000):
  #  data = Books(f"{uuid.uuid4()}", f"{uuid.uuid4()}")
  #  db.session.add(data)
 #   qry = Category.query.get(random.randint(1,10))
 #   qry.booklist.append(data)
#    db.session.commit()
  start = time.time()
  result = Category.query.filter(Category.book_category == "Science").first()
  data = result.booklist.filter(Books.bookname.like("%Book%")).limit(50)
  end = time.time()
  print(end-start)
  return "Hello"
  
  
@app.route("/anothertest")
def anothertest():
  python_string_list = "1,2,3,4"
  return render_template("helping.html", python_string_list = python_string_list)
  
 
if __name__ == "__main__":
  app.run(debug = True)
  
