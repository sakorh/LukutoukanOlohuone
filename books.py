from db import db
from sqlalchemy.sql import text
import users

def get_books():
    sql = "SELECT id, name, author, year, available FROM books ORDER BY id"
    result = db.session.execute(text(sql))
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
    sql = "INSERT INTO books (name, author, year, available) VALUES (:name, :author, :year, 0)"
    db.session.execute(text(sql), {"name":name, "author":author, "year":year})
    db.session.commit()

def remove_book(book_id):
    sql = "DELETE FROM books WHERE id=:id"
    db.session.execute(text(sql), {"id":int(book_id)})
    db.session.commit()

def search(query):
        sql = "SELECT id, name, author, available FROM books WHERE UPPER(name) LIKE UPPER(:query)"
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
    
