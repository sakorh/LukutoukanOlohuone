from app import app
from flask import render_template, request, redirect, session

import users
import books

@app.route("/")
def index():
    if session.get("author"):
        del session["author"]
    book = books.get_books(0)
    authors = books.get_authors()
    return render_template("index.html", books=book, authors=authors) 


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

@app.route("/search", methods=["GET","POST"])
def search():
    query = request.args["query"]
    result = books.search(query)
    authors = books.get_authors()
    return render_template("index.html", books=result, authors=authors)
    
@app.route("/add_review", methods=["POST"])
def add_review():
    book_id = int(request.args.get("id"))
    result = books.get_book(book_id)
    return render_template("add_review.html", book=result)

@app.route("/post_review", methods=["POST"])
def post_review():
    book_id = int(request.args.get("id"))
    comment = request.form["comment"]
    stars = request.form["stars"]
    books.add_review(stars, comment, book_id, users.user_id())
    return redirect("/my")

@app.route("/reviews", methods=["POST"])
def get_reviews():
    book_id = int(request.args.get("id"))
    book = books.get_book(book_id)
    reviews = books.get_reviews(book_id)
    return render_template("reviews.html", book=book, reviews=reviews)

@app.route("/select_author", methods=["POST"])
def select_author():
    selected_author = request.form.get("selected_author")
    result = books.filter_by_author(selected_author)
    authors = books.get_authors()
    return render_template("index.html", books=result, authors=authors)

@app.route("/add_wish", methods=["GET","POST"])
def add_wish():
    wishes = books.get_books(1)
    if request.method == "GET":
        return render_template("wishes.html", wishes=wishes)
    if request.method == "POST":
        name = request.form["name"]
        author = request.form["author"]
        year = int(request.form["year"])
        books.add_wish(name, author, year)
        return redirect("/add_wish")
    
@app.route("/add_vote", methods=["POST"])
def add_vote():
    book_id = request.form["vote"]
    books.add_vote(book_id)
    return redirect("/add_wish")
    
@app.route("/stats", methods=["GET", "POST"])
def stats():
    return redirect("/")