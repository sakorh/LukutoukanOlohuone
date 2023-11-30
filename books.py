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