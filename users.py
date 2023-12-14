from db import db
from flask import session, abort, request
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import secrets


def login(username, password):
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["user_role"] = user[2]
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False
        
def user_id():
    return session.get("user_id", 0)

def logout():
    del session["user_id"]
    del session["username"]
    del session["user_role"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, role) VALUES (:username, :password, 1)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return True

def is_admin():
    return session.get("user_role", 0) == 2

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)