from flask import * 
import sqlite3
import os
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

conn = sqlite3.connect("library.db")
c = conn.cursor()

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///library.sqlite3'

app.config["FILE_UPLOAD"] = f"{os.getcwd()}/files/"
db = SQLAlchemy(app)


class libraryfiles(db.Model):
  _id = db.Column("id", db.Integer, primary_key = True)
  bookname = db.Column("bookname", db.String(100))
  filename = db.Column("filename", db.String(255))
  author = db.Column("author", db.String(75))
  
  def __init__(self, bookname, filename, author):
    self.bookname = bookname
    self.filename = filename
    self.author = author


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/admin/add_content")
def add_content():
  return render_template("add_content.html")

@app.route("/admin/upload", methods = ["POST"])
def upload():
  booktitle = request.form["Bookname"]
  file_name = request.form["Filename"].replace(" ", "-")
  author = request.form["Author"]
  addFile = libraryfiles(booktitle, file_name, author)
  db.session.add(addFile)
  db.session.commit()
  print(request.files)
  file = request.files["File"]
  file.save(os.path.join(app.config["FILE_UPLOAD"], file.filename.replace(" ", "-")))
  return redirect(url_for("index"))


@app.route("/search", methods = ["GET", "POST"])
def search():
  if request.method == "GET":
    return render_template("search.html")
  elif request.method == "POST":
    search = f"%{request.form['search']}%"
    file = libraryfiles.query.filter(libraryfiles.bookname.like(search)).all()
    
    
    return render_template("search_result.html", search = search, file = file)
  
@app.route("/download/<path:path>")
def download(path):
  try:
    return send_from_directory(app.config["FILE_UPLOAD"], path=path, as_attachment = True)
  except FileNotFoundError:
    abort(404)

@app.route("/view/<path:path>")
def view(path):
  return render_template("view.html", filename = f"{path}")


if __name__ == "__main__":
  app.run(debug = True)
  #db.create_all()
