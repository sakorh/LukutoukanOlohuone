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


INSERT INTO books (name, author, year, available) VALUES ('Elolliset', 'Iida Turpeinen', 2023, 0);
INSERT INTO books (name, author, year, available) VALUES ('Talo taivaansinisellä merellä', 'TJ Klune', 2021, 0);
INSERT INTO books (name, author, year, available) VALUES ('Mitä tekoäly on?', 'Hannu Toivonen', '2023', 0);
