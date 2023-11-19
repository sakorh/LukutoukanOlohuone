from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    sql = "SELECT id, name, author, year, available FROM books ORDER BY id"
    result = db.session.execute(text(sql))
    books = result.fetchall()
    return render_template("index.html", books=books) 

@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return render_template("error.html", message="Väärä tunnus tai salasana")
    else:
        hash_value = user.password
    if not check_password_hash(hash_value, password):
        return render_template("error.html", message="Väärä tunnus tai salasana")

    session["username"] = username
    session["user_id"] = user[0]
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
        return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/loan", methods=["GET", "POST"])
def loan():
    user_id = session.get("user_id", 0)
    book_id = int(request.args.get("id"))
    sql = "UPDATE books SET user_id=:user_id WHERE id=:id"
    db.session.execute(text(sql), {"id":int(book_id), "user_id":user_id})
    db.session.commit()
    sql = "UPDATE books SET available=1 WHERE id=:id"
    db.session.execute(text(sql), {"id":int(book_id)})
    db.session.commit()
    return redirect("/")

@app.route("/my", methods=["GET","POST"])
def my():
    user_id = session.get("user_id", 0)
    sql = "SELECT id, name, author, year, available FROM books WHERE user_id=:user_id ORDER BY id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    books = result.fetchall()

    return render_template("my.html", books=books) 

@app.route("/return_book", methods=["GET", "POST"])
def return_book():
    user_id = session.get("user_id", 0)
    book_id = int(request.args.get("id"))
    sql = "UPDATE books SET user_id=null WHERE id=:id"
    db.session.execute(text(sql), {"id":int(book_id)})
    db.session.commit()
    sql = "UPDATE books SET available=0 WHERE id=:id"
    db.session.execute(text(sql), {"id":int(book_id)})
    db.session.commit()
    return redirect("/my")