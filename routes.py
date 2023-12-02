from app import app
from flask import render_template, request, redirect

import users
import books

@app.route("/")
def index():
    book = books.get_books()
    return render_template("index.html", books=book) 


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut. Tunnus on jo käytössä.")

@app.route("/loan", methods=["GET", "POST"])
def loan():
    user_id = users.user_id()
    book_id = int(request.args.get("id"))
    books.loan_book(book_id, user_id)

    return redirect("/")

@app.route("/my", methods=["GET","POST"])
def my():
    book = books.my_books()
    return render_template("my.html", books=book) 

@app.route("/return_book", methods=["GET", "POST"])
def return_book():
    book_id = int(request.args.get("id"))
    books.return_book(book_id)
    
    return redirect("/my")

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    allow = False
    if users.is_admin():
        allow = True
    if allow:
        if request.method == "GET":
            return render_template("add_book.html")
        if request.method == "POST":
            name = request.form["name"]
            author = request.form["author"]
            year = int(request.form["year"])
            books.add_book(name, author, year)
        return redirect("/add_book")
    else:
        return redirect("/")
    
@app.route("/remove", methods=["POST"])
def remove_book():
    allow = False
    if users.is_admin():
        allow = True
    if allow:
        book_id = int(request.args.get("id"))
        books.remove_book(book_id)
    return redirect("/")


@app.route("/stats", methods=["GET", "POST"])
def stats():
    return redirect("/")