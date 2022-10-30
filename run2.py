from flask import Flask,render_template, request
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DB = SQLAlchemy(app)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:////{}".format(os.path.join(project_dir, "my.db"))


class Book(DB.Model):
    title = DB.Column(DB.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)




def add_book(title):
        book = Book(title=title)
        db.session.add(book)
        db.session.commit()

def one_book_by_title(title):
    pass

def create():
    db.create_all()
    db.commit()

def all_books():
    return Book.query.all()



@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        print(request.form['title'])
    return render_template("home.html")

@app.route("/b", methods=["GET", "POST"])
def homes():
    if request.form:
        add_book(request.form['title'])
    return render_template("home.html")

@app.route("/a", methods=["GET", "POST"])
def creator():
    create()

@app.route("/g", methods=["GET", "POST"])
def all_books():
    books = all_books()
    return render_template("home2.html", books=books)



if __name__ == "__main__":
    app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.run(host='0.0.0.0', debug=True)