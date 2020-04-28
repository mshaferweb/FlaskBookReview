import argparse
import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', action='store_true',
                            default=False,
                            dest='force',
                            help='Reset all tables.  If not included import just truncates users and reviews')

    cmd_args = parser.parse_args()
    if cmd_args.force:
        dropTables()
        createTables()
        loadBooks()
    else:
        truncateReviewsUsers()
        # queryDB()

def createTables():
    sql_books = """CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);"""
    sql_users = """CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    session_id INTEGER NOT NULL
);"""
    sql_reviews = """CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books,
    review VARCHAR NOT NULL,
    rating INTEGER NOT NULL
);"""
    db.execute(sql_books)
    db.execute(sql_users)
    db.execute(sql_reviews)
    db.commit()

def dropTables():
    for table in ['users','reviews','books']:
        sql = 'DROP TABLE IF EXISTS '+table+' CASCADE;'
        db.execute(sql)
        db.commit()

def truncateReviewsUsers():
    for table in ['reviews','users']:
        sql = 'TRUNCATE ' + table + ' CASCADE;'
        db.execute(sql)
        db.commit()
    print("done")

def loadBooks():
    # isbn,title,author,year
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        if isbn.__eq__('isbn'):
            continue
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added Book: {isbn}  {title}")
    db.commit()
    print(f"Done")

def queryDB():
    book_id = "HELLOSOSDF"
    user_id = 2

    # existing_review_count = db.execute("SELECT * FROM reviews WHERE book_id = :book_id && user_id = user_id",
    #                              {"book_id": book_id,"user_id": user_id}).fetchone()
    existing_review_count = db.execute("select * from books where title like :bookname OR author like :bookname or isbn like :bookname",
        {"bookname": book_id})

    db.commit()
    print(existing_review_count[0])

def request1():
    import requests

    isbn = "9781632168146"
    key = "47rkiBSFHxWjMgqGv6pd3A"
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": key, "isbns": isbn})

    out = res.json()

    good_reads = out["books"][0]
    rating = good_reads["average_rating"]
    print(rating)

if __name__ == "__main__":
    main()
