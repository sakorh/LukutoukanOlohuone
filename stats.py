from db import db
from sqlalchemy.sql import text

def loan_stats():
    sql = """SELECT COUNT(s.book_id), b.id, b.name, b.author FROM stats s 
    JOIN books b ON s.book_id=b.id GROUP BY s.book_id, b.id, b.name, b.author"""
    result = db.session.execute(text(sql))
    stats = result.fetchall()
    return stats

def rating_stats():
    sql = """SELECT AVG(r.stars), b.id, b.name, b.author FROM stats s
    JOIN books b ON s.book_id=b.id JOIN reviews r ON s.reviews_id=r.id
    GROUP BY s.book_id, b.id, b.name, b.author"""
    result = db.session.execute(text(sql))
    stats = result.fetchall()
    return stats
