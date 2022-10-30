from flask import Flask,render_template, request
import crud


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        print(request.form['title'])
    return render_template("home.html")

@app.route("/b", methods=["GET", "POST"])
def homes():
    if request.form:
        crud.add_book(request.form['title'])
    return render_template("home.html")

@app.route("/a", methods=["GET", "POST"])
def creator():
    crud.create()

@app.route("/g", methods=["GET", "POST"])
def all_books():
    books = crud.all_books()
    return render_template("home2.html", books=books)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)