CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    name TEXT,
    author TEXT,
    year INTEGER,
    available INTEGER,
    user_id INTEGER REFERENCES users
); 

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    stars INTEGER,
    comment TEXT,
    book_id INTEGER REFERENCES books,
    user_id INTEGER REFERENCES users
);

INSERT INTO books (name, author, year, available) VALUES ('Elolliset', 'Iida Turpeinen', 2023, 0);
INSERT INTO books (name, author, year, available) VALUES ('Talo taivaansinisellä merellä', 'TJ Klune', 2021, 0);
INSERT INTO books (name, author, year, available) VALUES ('Mitä tekoäly on?', 'Hannu Toivonen', '2023', 0);
INSERT INTO users (username, password, role) VALUES ('admin', 'scrypt:32768:8:1$lVh3Iz3BMFPz60xv$60593b30b2c52e397a4ab8bfb2b33ec6a1ec3b8308e95f25e79df38373751bd8f25da7ffd20c65a7296ebdffecb269e426723beb5fe96ca7c3e0039e22f2e8b0', 2);
