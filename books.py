from db import db
from sqlalchemy.sql import text
from flask import session
import users

def get_books(wish):
    if wish == 0:
        sql = "SELECT id, name, author, year, available FROM books WHERE wish=:wish ORDER BY id"
        result = db.session.execute(text(sql), {"wish":wish})
        books = result.fetchall()
    if wish == 1:
        sql = """SELECT b.id, b.name, b.author, b.year, COUNT(w.id) FROM books b 
        JOIN wishes w ON b.id=w.book_id GROUP BY b.id"""
        result = db.session.execute(text(sql), {"wish":wish})
        books = result.fetchall()
    return books
    

def loan_book(book_id, user_id):
    sql = "UPDATE books SET user_id=:user_id WHERE id=:id"
    db.session.execute(text(sql), {"id":int(book_id), "user_id":user_id})
    db.session.commit()
    sql = "UPDATE books SET available=1 WHERE id=:id"
    db.session.execute(text(sql), {"id":int(book_id)})
    db.session.commit()

def my_books():
    sql = "SELECT id, name, author, year, available FROM books WHERE user_id=:user_id ORDER BY id"
    result = db.session.execute(text(sql), {"user_id":users.user_id()})
    books = result.fetchall()
    return books

def return_book(book_id):
    sql = "UPDATE books SET user_id=null WHERE id=:id"
    db.session.execute(text(sql), {"id":int(book_id)})
    db.session.commit()
    sql = "UPDATE books SET available=0 WHERE id=:id"
    db.session.execute(text(sql), {"id":int(book_id)})
    db.session.commit()

def add_book(name, author, year):
    sql = "INSERT INTO books (name, author, year, available, wish) VALUES (:name, :author, :year, 0, 0)"
    db.session.execute(text(sql), {"name":name, "author":author, "year":year})
    db.session.commit()

def remove_book(book_id):
    sql = "DELETE FROM books WHERE id=:id"
    db.session.execute(text(sql), {"id":int(book_id)})
    db.session.commit()

def search(query):
        if session.get("author"):
            author = session["author"]
            sql = """SELECT id, name, author, year, available FROM books WHERE (UPPER(name) 
            LIKE UPPER(:query) AND author LIKE :author AND wish=0)"""
            result = db.session.execute(text(sql), {"query":"%"+query+"%", "author":author})
            books = result.fetchall()
        else:
            sql = "SELECT id, name, author, year, available FROM books WHERE (UPPER(name) LIKE UPPER(:query) AND wish=0)"
            result = db.session.execute(text(sql), {"query":"%"+query+"%"})
            books = result.fetchall()
        return books

def add_review(stars, comment, book_id, user_id):
    sql = "INSERT INTO reviews (stars, comment, book_id, user_id) VALUES (:stars, :comment, :book_id, :user_id)"
    db.session.execute(text(sql), {"stars":stars, "comment":comment, "book_id":book_id, "user_id":user_id})
    db.session.commit()

def get_book(id):
    sql = "SELECT id, name, author, year FROM books WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    book = result.fetchone()
    return book

def get_reviews(id):
    sql = "SELECT id, stars, comment, book_id, user_id FROM reviews WHERE book_id=:book_id"
    result = db.session.execute(text(sql), {"book_id":id})
    reviews = result.fetchall()
    return reviews

def get_authors():
    sql = "SELECT DISTINCT author FROM books WHERE wish=0"
    result = db.session.execute(text(sql))
    authors = result.fetchall()
    authors = [str(author).strip("(',)") for author in authors]
    if not session.get("author"):
        authors.insert(0, "Valitse kirjailija")
    else:
        authors.remove(session["author"])
        authors.insert(0, session["author"])
    return authors

def filter_by_author(author):
    session["author"] = author
    sql = "SELECT id, name, author, year, available FROM books WHERE author LIKE :author"
    result = db.session.execute(text(sql), {"author":author})
    book_list = result.fetchall()
    return book_list

def add_wish(name, author, year):
    sql = "INSERT INTO books (name, author, year, available, wish) VALUES (:name, :author, :year, 0, 1)"
    db.session.execute(text(sql), {"name":name, "author":author, "year":year})
    db.session.commit()
    sql = "SELECT MAX(id) FROM books"
    result = db.session.execute(text(sql))
    book_id = result.fetchone()[0]
    add_vote(book_id)

def add_vote(book_id):
    user_id = users.user_id()
    sql = "INSERT INTO wishes (book_id, user_id) VALUES (:book_id, :user_id)"
    db.session.execute(text(sql), {"book_id":book_id, "user_id":user_id})
    db.session.commit()

def save(book_id):
    user_id = users.user_id()
    sql = "INSERT INTO saved (book_id, user_id) VALUES (:book_id, :user_id)"
    db.session.execute(text(sql), {"book_id":book_id, "user_id":user_id})
    db.session.commit()

def get_saved():
    user_id = users.user_id()
    sql = """SELECT b.id, b.name, b.author, b.year, b.available FROM books b 
    JOIN saved s ON b.id=s.book_id WHERE s.user_id=:user_id"""
    result = db.session.execute(text(sql), {"user_id":user_id})
    books = result.fetchall()
    return books

def remove_saved(book_id):
    user_id = users.user_id()
    sql = "DELETE FROM saved WHERE book_id=:book_id AND user_id=:user_id"
    db.session.execute(text(sql), {"book_id":book_id, "user_id":user_id})
    db.session.commit()